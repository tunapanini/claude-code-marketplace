# Public Repository Agent Guide

## Scope

- This repository is public. Treat every tracked file and Git commit as publicly visible.
- Keep plugins, skills, commands, hooks, scripts, fixtures, and documentation reusable outside a single person or company.

## Sensitive Information

- Never add secrets, tokens, passwords, private keys, cookies, credentials, webhook values, `.env` contents, or authentication headers.
- Never add internal hostnames, private repository URLs, production identifiers, customer data, issue contents, incident details, or non-public company information.
- Reference secrets only by clearly named environment variables such as `$SLACK_WEBHOOK_URL`; never include real or realistic-looking values.
- If a workflow requires private context, place it in a separate private repository instead of weakening this rule.

## Examples And Fixtures

- Do not use personal absolute paths, email addresses, usernames, machine names, real project names, real issue keys, or actual organization data in examples.
- Public repository coordinates and publisher metadata required for installation are allowed; do not reuse those identifiers as sample user data.
- Use neutral placeholders such as `/Users/example`, `owner/repo`, `PROJECT-123`, `example.com`, and `sample-project`.
- Use synthetic fixture data that cannot be mistaken for production or personal data.

## Validation

- Review the full diff for sensitive or identifying information before committing.
- Keep generated files, local caches, and test credentials out of Git.
- Validate plugin and skill metadata after changing manifests or `SKILL.md` files.
