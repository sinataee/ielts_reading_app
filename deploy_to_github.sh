#!/bin/bash
# IELTS Reading App - GitHub Deployment Script
# This script helps you push the application to GitHub

echo "=========================================="
echo "IELTS Reading App - GitHub Deployment"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed!"
    echo "Please install Git from: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Check if this is a git repository
if [ ! -d .git ]; then
    echo "📁 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

echo ""
echo "Please enter your GitHub repository URL:"
echo "Example: https://github.com/fatemehsarmadi/ielts-project-LLM.git"
read -p "Repository URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ No repository URL provided!"
    exit 1
fi

echo ""
echo "Setting up remote repository..."

# Check if remote already exists
if git remote get-url origin &> /dev/null; then
    echo "Remote 'origin' already exists. Updating URL..."
    git remote set-url origin "$REPO_URL"
else
    echo "Adding remote 'origin'..."
    git remote add origin "$REPO_URL"
fi

echo "✅ Remote repository configured"
echo ""

# Rename README for GitHub
if [ -f README_GITHUB.md ]; then
    echo "📝 Preparing GitHub README..."
    if [ -f README.md ]; then
        mv README.md README_LOCAL.md
        echo "   Renamed README.md to README_LOCAL.md"
    fi
    mv README_GITHUB.md README.md
    echo "   Renamed README_GITHUB.md to README.md"
    echo "✅ README prepared for GitHub"
fi

echo ""
echo "Checking Git configuration..."

# Check if user name is set
if [ -z "$(git config user.name)" ]; then
    read -p "Enter your name: " USER_NAME
    git config user.name "$USER_NAME"
fi

# Check if user email is set
if [ -z "$(git config user.email)" ]; then
    read -p "Enter your email: " USER_EMAIL
    git config user.email "$USER_EMAIL"
fi

echo "✅ Git configured"
echo "   Name: $(git config user.name)"
echo "   Email: $(git config user.email)"
echo ""

# Stage all files
echo "📦 Adding files to staging area..."
git add .
echo "✅ Files staged"
echo ""

# Show status
echo "📋 Files to be committed:"
git status --short
echo ""

# Commit
read -p "Enter commit message (or press Enter for default): " COMMIT_MSG
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Initial commit: IELTS Reading Test Application v1.2"
fi

echo "💾 Creating commit..."
git commit -m "$COMMIT_MSG"
echo "✅ Commit created"
echo ""

# Ask about branch
echo "Which branch do you want to push to?"
echo "1) main (recommended)"
echo "2) master"
read -p "Choice (1 or 2): " BRANCH_CHOICE

if [ "$BRANCH_CHOICE" = "2" ]; then
    BRANCH="master"
else
    BRANCH="main"
fi

# Check if branch exists
if ! git show-ref --verify --quiet refs/heads/$BRANCH; then
    echo "Creating branch: $BRANCH"
    git branch -M $BRANCH
fi

echo ""
echo "🔄 Attempting to pull existing changes..."
git pull origin $BRANCH --allow-unrelated-histories || echo "No existing changes to pull"

echo ""
echo "🚀 Pushing to GitHub..."
echo "You may be asked for your GitHub username and password/token"
echo ""

if git push -u origin $BRANCH; then
    echo ""
    echo "=========================================="
    echo "✅ SUCCESS! Code pushed to GitHub!"
    echo "=========================================="
    echo ""
    echo "Visit your repository at:"
    echo "$REPO_URL"
    echo ""
    echo "Next steps:"
    echo "1. Visit the repository URL above"
    echo "2. Verify all files are uploaded"
    echo "3. Check that README displays correctly"
    echo "4. Create a release (optional)"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ Push failed!"
    echo "=========================================="
    echo ""
    echo "Common solutions:"
    echo "1. Check your GitHub credentials"
    echo "2. Generate a Personal Access Token:"
    echo "   https://github.com/settings/tokens"
    echo "3. Use the token as your password when prompted"
    echo "4. Or set up SSH keys for authentication"
    echo ""
    echo "See GITHUB_DEPLOYMENT.md for detailed help"
    echo ""
    exit 1
fi
