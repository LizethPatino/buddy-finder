# Contributing to Buddy Finder

Welcome to the team. We work like a real company: small steps, open doors, and we help each other. If anything is unclear, ask in the group. No question is too small.

## Setup (once)

Install **Git** and **Docker Desktop**, then:

```bash
git clone https://github.com/LizethPatino/buddy-finder.git
cd buddy-finder
cp .env.example .env      # fill in the values the team shares privately
```

> **Never commit `.env`.** The repo is public: passwords and API keys only go in `.env`, which Git ignores.

## The daily loop

| Step | What you do | Command |
| --- | --- | --- |
| 1 | Start from the latest `main` | `git switch main` then `git pull` |
| 2 | Make a branch for one small feature | `git switch -c feature/login` |
| 3 | Commit small steps | `git add .` then `git commit -m "feat: add login endpoint"` |
| 4 | Push and open a pull request | `git push -u origin feature/login` |
| 5 | A teammate reviews, then **Squash and merge** | The branch deletes itself. Back to step 1. |

**Branch names:** `feature/…`, `fix/…`, `docs/…`, `chore/…`

## Commit messages

Start with a prefix, then say what the change does:

| Prefix | For | Example |
| --- | --- | --- |
| `feat:` | Something new | `feat: add login endpoint` |
| `fix:` | A bug fix | `fix: return 404 for unknown events` |
| `docs:` | Docs and comments | `docs: explain how to run locally` |
| `test:` | Tests | `test: cover opt-in without a ticket` |
| `chore:` | Setup and config | `chore: add docker-compose` |

Not like this: `changes`, `fix stuff`, `asdf`.

We squash when merging, so messy commits inside your branch are fine. **What lands on `main` is the pull request title**, so make that clear and give it a prefix.

## Pull requests

- Keep them small: one thing per PR. Open one as soon as a small piece works. Several a day is great.
- Fill in the template and write `Closes #12` to link the issue.
- Every PR needs one approval and all comments resolved. Nobody can push to `main` directly, including the team lead.
- **Reviewing?** Be kind and specific, ask questions, then **Approve** or **Request changes**. Reviews are for learning, not judging.

## If `main` moved on while you worked

```bash
git switch main && git pull
git switch feature/your-branch
git merge main
```

A **conflict** means two people changed the same lines. Open the files Git lists, keep the right code between the `<<<<<<<` and `>>>>>>>` markers, delete the markers, then `git add .` and `git commit`. Stuck? Ask in the group. Please don't use `git rebase` or `git push --force`.

## Code standards

- A docstring at the top of every file and on every function (part of our mark).
- Follow the API contract in [`docs/api.md`](docs/api.md); if you change it, update the doc in the same PR.
- Errors always use our format: `{ "error": "...", "message": "..." }`.
- Run `pytest` in `backend/` before opening a PR.

## How we meet

- **Tuesday:** daily in the lab, 15–20 minutes: what I did, what's next, anything in my way.
- **Friday afternoon:** the same three questions on WhatsApp.
- **Blocked?** Tell the group straight away.
