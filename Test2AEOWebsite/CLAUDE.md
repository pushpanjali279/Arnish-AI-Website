# WebsiteAgent

This project is a website-building agent. It interviews the client (onboarding), builds a static website in `site/` modeled on their reference screenshots, writes all copy through an AEO/EEAT content skill, and deploys to Hostinger over SSH.

## First run

If `client/profile.md` does not exist, run the `onboarding` skill before anything else. Every other skill depends on the profile it produces. Greet the user, explain the four steps below in one short paragraph, then start the onboarding questions.

## Workflow

1. **`onboarding` skill** — collects the business story, the money keyword, EEAT proof, and reference screenshots. Writes `client/profile.md`.
2. **`build-website` skill** — builds a static site in `site/`, matching the layout of the reference screenshots in `client/references/`.
3. **`aeo-content-writer` skill** — writes ALL site copy. Never write or edit copy in `site/` without loading this skill first.
4. **`deploy-hostinger` skill** — publishes `site/` to the domain in `.env` via `scripts/deploy.sh`.

## Layout

- `client/` — onboarding output: `profile.md` plus `references/` (screenshots of sites to model)
- `site/` — the website source. Static HTML/CSS/JS with root-relative URLs only; never hard-code a domain.
- `scripts/build.py` — copies `site/` to `dist/` and fills in absolute canonical/schema URLs plus `sitemap.xml` from `DOMAIN` in `.env`. Only `dist/` gets deployed.
- `scripts/deploy.sh` — one-command deploy: builds, then rsyncs `dist/`. Refuses to run while `.env` holds template values.
- `client/pending-regulatory/` — IRDAI/DPDP material held back until the client verifies it. Never publish it unasked.
- `.env` — SSH credentials and target domain. Never commit it. Never print `SSH_PASSWORD`.

## Commands

`/onboard` · `/build` · `/write` · `/deploy`

## Hard rules

- Every line of site copy must pass `.claude/skills/aeo-content-writer/writing-rules.md`. No exceptions.
- EEAT facts (years, numbers, awards, reviews, credentials) come from `client/profile.md` exactly as recorded. Never invent them.
- Never echo, log, or paste the contents of `SSH_PASSWORD`. Scripts read it from `.env`.
- No regulatory or compliance claims (IRDAI, DPDP) on the site until the client verifies them.
- Deploy only the built `dist/` (generated from `site/`). Verify every deploy with `curl -s https://$DOMAIN/` and report the result.
- After building or editing pages, run the `site-reviewer` agent before offering to deploy.
