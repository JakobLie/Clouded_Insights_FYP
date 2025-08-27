```bash # For formatting only
# Git Workflow Guidelines

This project uses a **branch + merge request workflow**.  
Do **not push directly to `main`**. Always work on your own branch and open a merge request (pull request) into `main`.

---

## 1. Create a Branch for Your Work
Create and switch to a new branch for your feature or fix:
    git checkout -b feature/my-feature

Push branch to the remote:
    git push -u origin feature/my-feature

Note: ONLY work in branches, NEVER push to main

## 2. Keep Your Branch Updated with main

Before starting work (or before pushing a PR), make sure your branch has the latest changes from main.

- # 2a. Get the latest refs from remote:
    git fetch origin

- # 2b. Switch to main
    git checkout main

- # 2c. Pull latest main
    git pull origin main

- # 2d. Switch back to your branch
    git checkout feature/my-feature

- # 2e. Merge main into your branch
    git merge main

If there are conflicts, resolve them locally, then commit the resolved changes:
    git add .
    git commit -m "chore: resolve merge conflicts with main"

## 3. Add, Commit, and Push Your Changes

When you make changes:

- # 3a. Stage changes
    git add .

- # 3b. Commit with a clear message
    git commit -m "Describe what you changed"

- # 3c. Push your branch to remote
    git push origin feature/my-feature

## 4. Open a Merge Request

- 4a. Go to GitHub and open a Pull Request from your branch into main.

- 4b. Request a review if required.

- 4c. Once approved, merge the PR → main will be updated.

# Notes
One feature/fix = one branch.

Never push directly to main.

Always resolve conflicts locally before opening your merge request.

Write clear commit messages that describe the why and what of your changes.