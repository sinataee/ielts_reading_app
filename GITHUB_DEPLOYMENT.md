# GitHub Deployment Guide

This guide will walk you through pushing the IELTS Reading Test Application to GitHub.

## Prerequisites

1. **Git installed** on your computer
   - Download from: https://git-scm.com/downloads
   - Verify installation: `git --version`

2. **GitHub account**
   - Create one at: https://github.com/signup
   - Already have one? Great!

3. **Repository created on GitHub**
   - Go to: https://github.com/new
   - Or use the repository you showed me: https://github.com/fatemehsarmadi/ielts-project-LLM

## Step-by-Step Instructions

### Option 1: Push to Existing Repository (Recommended for your case)

Since you already have a repository at `https://github.com/fatemehsarmadi/ielts-project-LLM`, follow these steps:

#### 1. Open Terminal/Command Prompt

Navigate to the application folder:
```bash
cd path/to/ielts_reading_app
```

#### 2. Initialize Git (if not already initialized)

```bash
git init
```

#### 3. Configure Git (First time only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### 4. Add Remote Repository

```bash
git remote add origin https://github.com/fatemehsarmadi/ielts-project-LLM.git
```

If you get an error saying remote already exists:
```bash
git remote set-url origin https://github.com/fatemehsarmadi/ielts-project-LLM.git
```

#### 5. Add All Files

```bash
git add .
```

This adds all files to staging. The `.gitignore` file will automatically exclude unnecessary files.

#### 6. Commit Changes

```bash
git commit -m "Initial commit: Complete IELTS Reading Test Application v1.2"
```

Or with more details:
```bash
git commit -m "feat: Complete IELTS Reading Test Application

- Content Editor with rich text editing
- Exam Engine with fullscreen and highlighting
- Result Engine with IELTS band scoring
- Support for all 11 question types
- Visual table and flowchart builders
- Comprehensive documentation"
```

#### 7. Pull Existing Changes (if any)

```bash
git pull origin main --allow-unrelated-histories
```

If your default branch is `master` instead of `main`:
```bash
git pull origin master --allow-unrelated-histories
```

If there are conflicts, resolve them, then:
```bash
git add .
git commit -m "Merge existing repository with new code"
```

#### 8. Push to GitHub

```bash
git push -u origin main
```

Or if using `master` branch:
```bash
git push -u origin master
```

If you get authentication errors, see the Authentication section below.

### Option 2: Fresh Start (Clean Repository)

If you want to start completely fresh:

#### 1. Create New Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `ielts-reading-app` (or your choice)
3. Description: "Comprehensive IELTS Academic Reading test preparation application"
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we have these)
6. Click "Create repository"

#### 2. Follow Steps from Option 1

Use the URL of your new repository in step 4.

## Authentication Methods

### Method 1: Personal Access Token (Recommended)

1. **Generate Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Name: `IELTS App Deployment`
   - Select scopes: `repo` (all sub-scopes)
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again!)

2. **Use Token When Pushing:**
   ```bash
   git push -u origin main
   ```
   - Username: your GitHub username
   - Password: paste the token (not your GitHub password!)

3. **Save Credentials (Optional):**
   ```bash
   git config --global credential.helper store
   ```

### Method 2: SSH Keys

1. **Generate SSH Key:**
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```
   Press Enter to accept default location

2. **Add to SSH Agent:**
   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```

3. **Copy Public Key:**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

4. **Add to GitHub:**
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Paste your public key
   - Click "Add SSH key"

5. **Update Remote URL:**
   ```bash
   git remote set-url origin git@github.com:fatemehsarmadi/ielts-project-LLM.git
   ```

## Verify Upload

After pushing, visit your repository:
```
https://github.com/fatemehsarmadi/ielts-project-LLM
```

You should see:
- ✅ All Python files
- ✅ Documentation files
- ✅ README.md displayed on main page
- ✅ LICENSE file
- ✅ .gitignore file
- ❌ No __pycache__ folders (excluded by .gitignore)
- ❌ No .pyc files (excluded by .gitignore)

## File Structure on GitHub

```
ielts-project-LLM/
├── .gitignore
├── LICENSE
├── README.md (rename README_GITHUB.md to this)
├── CONTRIBUTING.md
├── INSTALL_GUIDE.md
├── QUICK_START.txt
├── QUESTION_TYPES_GUIDE.md
├── UPDATE_NOTES_v1.2.md
├── PROJECT_SUMMARY.md
├── main.py
├── models.py
├── content_editor.py
├── exam_engine.py
├── result_engine.py
├── test_installation.py
└── requirements.txt
```

## Recommended: Rename README

Before pushing, rename the GitHub README:
```bash
mv README.md README_LOCAL.md
mv README_GITHUB.md README.md
```

This ensures the GitHub-specific README is displayed on the repository page.

## Making Updates Later

When you make changes to the code:

```bash
# 1. Check status
git status

# 2. Add changed files
git add .

# 3. Commit with message
git commit -m "fix: Description of what you fixed"

# 4. Push to GitHub
git push
```

## Common Commands

```bash
# Check repository status
git status

# View commit history
git log

# View remote repositories
git remote -v

# Pull latest changes
git pull

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Merge branch
git merge feature-name

# View differences
git diff
```

## Troubleshooting

### Problem: "fatal: not a git repository"
**Solution:**
```bash
git init
```

### Problem: "permission denied"
**Solution:**
Check your authentication (token or SSH key)

### Problem: "conflict" during merge
**Solution:**
1. Open conflicted files
2. Look for `<<<<<<<`, `=======`, `>>>>>>>` markers
3. Edit to resolve conflicts
4. Remove conflict markers
5. `git add .`
6. `git commit -m "Resolve merge conflicts"`

### Problem: "refusing to merge unrelated histories"
**Solution:**
```bash
git pull origin main --allow-unrelated-histories
```

### Problem: Large files won't upload
**Solution:**
Make sure .gitignore is working. Check file size:
```bash
git ls-files -s | awk '{print $4, $2}' | sort -n
```

Files over 100MB need Git LFS or should be excluded.

## Best Practices

1. **Commit often** with clear messages
2. **Pull before you push** to avoid conflicts
3. **Use branches** for new features
4. **Write meaningful commit messages**
5. **Don't commit sensitive data** (passwords, tokens)
6. **Keep commits focused** (one feature/fix per commit)
7. **Test before pushing** (run test_installation.py)

## Creating Releases

Once your code is on GitHub, create releases:

1. Go to repository → Releases → "Create a new release"
2. Tag version: `v1.2.0`
3. Release title: `Version 1.2.0 - Visual Tables and Flowcharts`
4. Description: Copy from UPDATE_NOTES_v1.2.md
5. Attach files if needed (e.g., sample packages)
6. Click "Publish release"

## Additional Features

### Enable GitHub Pages (for documentation)

1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: main → /docs
4. Save

### Add Topics

Add topics to help others find your repository:
- `ielts`
- `reading-test`
- `education`
- `python`
- `tkinter`
- `test-preparation`

### Create Issues Template

Create `.github/ISSUE_TEMPLATE/bug_report.md` for standardized bug reports.

## Repository Settings Recommendations

1. **About section:**
   - Description: "Comprehensive IELTS Academic Reading test preparation application"
   - Website: (your documentation site if any)
   - Topics: ielts, education, python, tkinter

2. **Features:**
   - ✅ Issues
   - ✅ Wikis (for detailed documentation)
   - ✅ Discussions (for community questions)

3. **Branch protection:**
   - Require pull request reviews
   - Require status checks

## Next Steps

After pushing to GitHub:

1. ✅ Verify all files are uploaded
2. ✅ Check README displays correctly
3. ✅ Test clone from another location
4. ✅ Create first release (v1.2.0)
5. ✅ Add repository description and topics
6. ✅ Share with others!

## Need Help?

- GitHub Docs: https://docs.github.com
- Git Documentation: https://git-scm.com/doc
- Create an issue in your repository

---

**Congratulations! Your IELTS Reading App is now on GitHub! 🎉**
