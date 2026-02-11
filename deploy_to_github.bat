@echo off
REM IELTS Reading App - GitHub Deployment Script for Windows
REM This script helps you push the application to GitHub

echo ==========================================
echo IELTS Reading App - GitHub Deployment
echo ==========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo Error: Git is not installed!
    echo Please install Git from: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo Git is installed
echo.

REM Check if this is a git repository
if not exist .git (
    echo Initializing Git repository...
    git init
    echo Git repository initialized
) else (
    echo Git repository already exists
)

echo.
echo Please enter your GitHub repository URL:
echo Example: https://github.com/fatemehsarmadi/ielts-project-LLM.git
set /p REPO_URL="Repository URL: "

if "%REPO_URL%"=="" (
    echo Error: No repository URL provided!
    pause
    exit /b 1
)

echo.
echo Setting up remote repository...

REM Check if remote already exists
git remote get-url origin >nul 2>&1
if errorlevel 0 (
    echo Remote 'origin' already exists. Updating URL...
    git remote set-url origin "%REPO_URL%"
) else (
    echo Adding remote 'origin'...
    git remote add origin "%REPO_URL%"
)

echo Remote repository configured
echo.

REM Rename README for GitHub
if exist README_GITHUB.md (
    echo Preparing GitHub README...
    if exist README.md (
        move README.md README_LOCAL.md >nul
        echo    Renamed README.md to README_LOCAL.md
    )
    move README_GITHUB.md README.md >nul
    echo    Renamed README_GITHUB.md to README.md
    echo README prepared for GitHub
)

echo.
echo Checking Git configuration...

REM Check if user name is set
git config user.name >nul 2>&1
if errorlevel 1 (
    set /p USER_NAME="Enter your name: "
    git config user.name "%USER_NAME%"
)

REM Check if user email is set
git config user.email >nul 2>&1
if errorlevel 1 (
    set /p USER_EMAIL="Enter your email: "
    git config user.email "%USER_EMAIL%"
)

echo Git configured
for /f "delims=" %%i in ('git config user.name') do set GIT_NAME=%%i
for /f "delims=" %%i in ('git config user.email') do set GIT_EMAIL=%%i
echo    Name: %GIT_NAME%
echo    Email: %GIT_EMAIL%
echo.

REM Stage all files
echo Adding files to staging area...
git add .
echo Files staged
echo.

REM Show status
echo Files to be committed:
git status --short
echo.

REM Commit
set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
if "%COMMIT_MSG%"=="" (
    set COMMIT_MSG=Initial commit: IELTS Reading Test Application v1.2
)

echo Creating commit...
git commit -m "%COMMIT_MSG%"
echo Commit created
echo.

REM Ask about branch
echo Which branch do you want to push to?
echo 1) main (recommended)
echo 2) master
set /p BRANCH_CHOICE="Choice (1 or 2): "

if "%BRANCH_CHOICE%"=="2" (
    set BRANCH=master
) else (
    set BRANCH=main
)

REM Check if branch exists and rename
git rev-parse --verify %BRANCH% >nul 2>&1
if errorlevel 1 (
    echo Creating branch: %BRANCH%
    git branch -M %BRANCH%
)

echo.
echo Attempting to pull existing changes...
git pull origin %BRANCH% --allow-unrelated-histories 2>nul
if errorlevel 1 (
    echo No existing changes to pull
)

echo.
echo Pushing to GitHub...
echo You may be asked for your GitHub username and password/token
echo.

git push -u origin %BRANCH%
if errorlevel 0 (
    echo.
    echo ==========================================
    echo SUCCESS! Code pushed to GitHub!
    echo ==========================================
    echo.
    echo Visit your repository at:
    echo %REPO_URL%
    echo.
    echo Next steps:
    echo 1. Visit the repository URL above
    echo 2. Verify all files are uploaded
    echo 3. Check that README displays correctly
    echo 4. Create a release (optional)
    echo.
) else (
    echo.
    echo ==========================================
    echo Push failed!
    echo ==========================================
    echo.
    echo Common solutions:
    echo 1. Check your GitHub credentials
    echo 2. Generate a Personal Access Token:
    echo    https://github.com/settings/tokens
    echo 3. Use the token as your password when prompted
    echo 4. Or set up SSH keys for authentication
    echo.
    echo See GITHUB_DEPLOYMENT.md for detailed help
    echo.
)

pause
