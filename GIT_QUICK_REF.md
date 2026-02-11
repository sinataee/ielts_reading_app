# GitHub Quick Reference

## First Time Setup (One-time only)

```bash
# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize repository
cd ielts_reading_app
git init

# Add remote
git remote add origin https://github.com/fatemehsarmadi/ielts-project-LLM.git

# First push
git add .
git commit -m "Initial commit: IELTS Reading Test Application v1.2"
git push -u origin main
```

## Daily Workflow

```bash
# 1. Make changes to your code
# 2. Check what changed
git status

# 3. Stage changes
git add .

# 4. Commit with message
git commit -m "fix: Description of what you changed"

# 5. Push to GitHub
git push
```

## Common Commands

### Status & Info
```bash
git status              # See what's changed
git log                 # View commit history
git diff                # See line-by-line changes
git remote -v           # View remote repositories
```

### Staging & Committing
```bash
git add .               # Stage all changes
git add file.py         # Stage specific file
git commit -m "message" # Commit with message
git commit --amend      # Modify last commit
```

### Pushing & Pulling
```bash
git pull                # Get latest from GitHub
git push                # Upload your commits
git push -u origin main # First push (sets upstream)
```

### Branches
```bash
git branch              # List branches
git branch feature-x    # Create new branch
git checkout feature-x  # Switch to branch
git checkout -b new-br  # Create and switch
git merge feature-x     # Merge branch to current
```

### Undoing Changes
```bash
git restore file.py     # Discard local changes
git reset HEAD~1        # Undo last commit (keep changes)
git reset --hard HEAD~1 # Undo last commit (delete changes)
```

## Commit Message Format

### Good commit messages:
```
feat: Add flowchart graphical rendering
fix: Correct band score for 40 questions
docs: Update installation guide
style: Format code to PEP 8
refactor: Simplify highlighting logic
test: Add tests for table builder
```

### Prefixes:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructure
- `test:` Testing
- `chore:` Maintenance

## Authentication

### Personal Access Token
1. Generate: https://github.com/settings/tokens
2. Use token as password when pushing
3. Save credentials:
   ```bash
   git config --global credential.helper store
   ```

### SSH Keys (Recommended)
```bash
# Generate key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: https://github.com/settings/keys

# Update remote URL
git remote set-url origin git@github.com:fatemehsarmadi/ielts-project-LLM.git
```

## Troubleshooting

### "Permission denied"
→ Check your authentication (token or SSH key)

### "refusing to merge unrelated histories"
```bash
git pull origin main --allow-unrelated-histories
```

### "conflict" during merge
1. Open conflicted files
2. Look for `<<<<<<<` markers
3. Resolve conflicts manually
4. `git add .`
5. `git commit -m "Resolve conflicts"`

### Undo last commit (not pushed)
```bash
git reset --soft HEAD~1
```

### Undo last commit (already pushed)
```bash
git revert HEAD
git push
```

## GitHub Repository URL

Your repository:
```
https://github.com/fatemehsarmadi/ielts-project-LLM
```

Clone command:
```bash
git clone https://github.com/fatemehsarmadi/ielts-project-LLM.git
```

## Quick Deploy Scripts

### Linux/Mac:
```bash
chmod +x deploy_to_github.sh
./deploy_to_github.sh
```

### Windows:
```cmd
deploy_to_github.bat
```

## Resources

- Git Documentation: https://git-scm.com/doc
- GitHub Docs: https://docs.github.com
- Full Guide: See GITHUB_DEPLOYMENT.md

---

**Keep this file handy for quick reference!**
