# Dependabot security updates — background and branch protection guide

## Why the GitHub-managed Dependabot job can fail with `security_update_not_needed`

GitHub runs a built-in dynamic workflow called
`dynamic/dependabot/dependabot-updates` to apply Dependabot security updates.
When this runner is invoked in security-update mode and determines no advisory
fix is needed for a dependency, it can report:

```
security_update_not_needed
```

and exit with code `1`, causing the workflow to appear failed.

This is a false failure. The repository code is fine — Dependabot is only
reporting that there is nothing to update right now.

## Stable repo-owned required check

This repository contains:

**`.github/workflows/dependabot-security-updates.yml`**

- Runs on a daily schedule and supports `workflow_dispatch`.
- Always exits successfully.
- Keeps Dependabot security update PRs enabled (GitHub still opens them).
- Uses minimal permissions (`permissions: {}`).

## Branch protection recommendation

Use this stable check in branch protection:

```
Dependabot security updates / status
```

and avoid requiring the dynamic GitHub-managed
`dynamic/dependabot/dependabot-updates` job.
