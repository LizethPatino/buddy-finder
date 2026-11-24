"""Checks the rules the database itself enforces: roles, constraints and group size."""
import threading

import psycopg
import pytest
from psycopg import errors


def _new_group(conn, event_id):
    """Create an empty buddy group for the event and return its id."""
    return conn.execute(
        "INSERT INTO buddy_groups (event_id) VALUES (%s) RETURNING id", (event_id,)
    ).fetchone()[0]


def _opt_in(conn, user_id, event_id, group_id=None):
    """Opt a student in, optionally straight into a group."""
    conn.execute(
        "INSERT INTO optins (user_id, event_id, interests, group_id) VALUES (%s, %s, %s, %s)",
        (user_id, event_id, ["music"], group_id),
    )


# --- Database roles -------------------------------------------------------------------------

def test_app_role_can_write_rows_but_not_change_tables(connect, event_with_students):
    event_with_students(1)  # inserts as bf_app
    conn = connect("bf_app")
    with pytest.raises(errors.InsufficientPrivilege):
        conn.execute("CREATE TABLE hack (id int)")
    with pytest.raises(errors.InsufficientPrivilege):
        conn.execute("DROP TABLE users")
    with pytest.raises(errors.InsufficientPrivilege):
        conn.execute("ALTER TABLE users ADD COLUMN hack int")


def test_analytics_role_reads_only_the_stats_view(connect):
    conn = connect("bf_analytics")
    conn.execute("SELECT * FROM event_stats").fetchall()
    for table in ("users", "events", "tickets", "optins", "buddy_groups"):
        with pytest.raises(errors.InsufficientPrivilege):
            conn.execute(f"SELECT 1 FROM {table}")
    with pytest.raises(errors.InsufficientPrivilege):
        conn.execute("INSERT INTO events (title, venue, starts_at) VALUES ('x', 'y', now())")


# --- Constraints ----------------------------------------------------------------------------

def test_email_is_unique_ignoring_case(connect):
    conn = connect()
    conn.execute("INSERT INTO users (name, email, password_hash) VALUES ('A', 'Case@qmul.ac.uk', 'x')")
    with pytest.raises(errors.UniqueViolation):
        conn.execute("INSERT INTO users (name, email, password_hash) VALUES ('B', 'case@QMUL.ac.uk', 'x')")


def test_role_must_be_student_or_staff(connect):
    with pytest.raises(errors.CheckViolation):
        connect().execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES ('A', 'r@q.uk', 'x', 'admin')"
        )


def test_one_ticket_per_user_per_event(connect, event_with_students):
    event_id, (user_id,) = event_with_students(1)
    with pytest.raises(errors.UniqueViolation):
        connect().execute("INSERT INTO tickets (user_id, event_id) VALUES (%s, %s)", (user_id, event_id))


def test_opt_in_needs_a_ticket(connect, event_with_students):
    event_id, _ = event_with_students(0)
    _, (other_user,) = event_with_students(1)  # has a ticket, but for a different event
    with pytest.raises(errors.ForeignKeyViolation):
        _opt_in(connect(), other_user, event_id)


def test_opt_in_needs_at_least_one_interest(connect, event_with_students):
    event_id, (user_id,) = event_with_students(1)
    with pytest.raises(errors.CheckViolation):
        connect().execute(
            "INSERT INTO optins (user_id, event_id, interests) VALUES (%s, %s, '{}')", (user_id, event_id)
        )


def test_deleting_a_user_removes_their_tickets_and_opt_ins(connect, event_with_students):
    conn = connect()
    event_id, (user_id,) = event_with_students(1)
    _opt_in(conn, user_id, event_id)
    conn.execute("DELETE FROM users WHERE id = %s", (user_id,))
    assert conn.execute("SELECT count(*) FROM tickets WHERE user_id = %s", (user_id,)).fetchone()[0] == 0
    assert conn.execute("SELECT count(*) FROM optins WHERE user_id = %s", (user_id,)).fetchone()[0] == 0


# --- Group size -----------------------------------------------------------------------------

def test_group_holds_at_most_four(connect, event_with_students):
    conn = connect()
    event_id, users = event_with_students(5)
    group_id = _new_group(conn, event_id)
    for user_id in users[:4]:
        _opt_in(conn, user_id, event_id, group_id)
    with pytest.raises(errors.CheckViolation, match="is full"):
        _opt_in(conn, users[4], event_id, group_id)


def test_declined_member_frees_a_place(connect, event_with_students):
    conn = connect()
    event_id, users = event_with_students(5)
    group_id = _new_group(conn, event_id)
    for user_id in users[:4]:
        _opt_in(conn, user_id, event_id, group_id)
    conn.execute("UPDATE optins SET membership = 'declined' WHERE user_id = %s", (users[0],))
    _opt_in(conn, users[4], event_id, group_id)


def test_group_must_belong_to_the_same_event(connect, event_with_students):
    conn = connect()
    event_a, (user_a,) = event_with_students(1)
    event_b, _ = event_with_students(0)
    with pytest.raises(errors.CheckViolation, match="not a group for event"):
        _opt_in(conn, user_a, event_a, _new_group(conn, event_b))


def test_two_pods_joining_at_once_cannot_make_a_group_of_five(connect, db_urls, event_with_students):
    """Like two API pods matching at the same moment: exactly one join may succeed."""
    conn = connect()
    event_id, users = event_with_students(5)
    group_id = _new_group(conn, event_id)
    for user_id in users[:3]:
        _opt_in(conn, user_id, event_id, group_id)

    start = threading.Barrier(2)
    results = []

    def join(user_id):
        with psycopg.connect(db_urls["bf_app"]) as pod:  # one transaction per "pod"
            start.wait()
            try:
                _opt_in(pod, user_id, event_id, group_id)
                pod.commit()
                results.append("joined")
            except errors.CheckViolation:
                results.append("full")

    threads = [threading.Thread(target=join, args=(u,)) for u in users[3:]]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert sorted(results) == ["full", "joined"]
    count = conn.execute("SELECT count(*) FROM optins WHERE group_id = %s", (group_id,)).fetchone()[0]
    assert count == 4


# --- Stats view -----------------------------------------------------------------------------

def test_event_stats_counts(connect, event_with_students):
    conn = connect()
    event_id, users = event_with_students(4)
    group_id = _new_group(conn, event_id)
    _opt_in(conn, users[0], event_id, group_id)
    _opt_in(conn, users[1], event_id, group_id)
    _opt_in(conn, users[2], event_id)  # still looking

    row = connect("bf_analytics").execute(
        "SELECT ticket_count, optin_count, looking_count, group_count FROM event_stats WHERE event_id = %s",
        (event_id,),
    ).fetchone()
    assert row == (4, 3, 1, 1)
