# 🚀 Step-by-Step GitHub Deployment Guide

This guide is designed for beginners with **zero prior experience**. Follow these simple steps to publish your **Swapi Water Tanker** project to GitHub.

---

## 📋 What You Need
1. A free **GitHub Account**: [Sign up at github.com](https://github.com) if you don't have one.
2. Either **GitHub Desktop** (easiest, visual, no terminal needed) OR **Git Command Line** (just 4 copy-paste commands).

---

## 🌟 Method 1: The Easiest Way (Using GitHub Desktop - No Code Needed)

If you have never used the terminal or Git commands, this is the simplest method:

1. **Download GitHub Desktop**:
   - Go to [desktop.github.com](https://desktop.github.com) and install it.
   - Sign in with your GitHub account.

2. **Add Your Existing Folder**:
   - Open GitHub Desktop.
   - Click **File** > **Add Local Repository** (or press `Ctrl + O`).
   - Click **Choose...** and select your project folder:
     `C:\Users\Swapnil\OneDrive\Desktop\swapi_water_tanker`
   - If it says *"This directory does not appear to be a Git repository"*, click the blue link: **"create a repository here"**.
   - Keep the default settings and click **Create Repository**.

3. **Publish to GitHub**:
   - At the top bar, click the blue **Publish repository** button.
   - Name: `swapi_water_tanker`
   - Uncheck *"Keep this code private"* if you want your project to be public (or keep it checked for private).
   - Click **Publish Repository**.

🎉 **Done!** Your project is now live on GitHub!

---

## ⚡ Method 2: Using PowerShell Terminal (4 Quick Commands)

If you prefer using the command line:

### Step 1: Open PowerShell in Project Folder
1. Open PowerShell on Windows.
2. Navigate to your project folder:
   ```powershell
   cd "C:\Users\Swapnil\OneDrive\Desktop\swapi_water_tanker"
   ```

### Step 2: Create a New Empty Repo on GitHub
1. Go to [github.com/new](https://github.com/new).
2. Enter **Repository name**: `swapi_water_tanker`.
3. Choose **Public** (or **Private**).
4. **Important**: Leave "Add a README file", "Add .gitignore", and "Choose a license" **UNCHECKED** (we already have them created in our project!).
5. Click **Create repository**.
6. Copy the repository URL (it looks like `https://github.com/YOUR_USERNAME/swapi_water_tanker.git`).

### Step 3: Initialize Git and Push Your Code
Copy and run these commands one by one in PowerShell (replace `YOUR_USERNAME` with your actual GitHub username):

```powershell
# 1. Initialize git
git init

# 2. Stage all project files
git add .

# 3. Create initial commit
git commit -m "Initial commit: Swapi Water Tanker with CLI, GUI, and unit tests"

# 4. Rename main branch to 'main'
git branch -M main

# 5. Connect to your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/swapi_water_tanker.git

# 6. Upload (push) your code to GitHub
git push -u origin main
```

*(If prompted to log in, a browser window will open asking you to click **Authorize Git Credential Manager**).*

---

## 🔄 How to Push New Updates Later

Whenever you make changes to your project code in the future:
```powershell
git add .
git commit -m "Describe what changed"
git push
```

---

## 🛡️ Included Files for GitHub Best Practices

Your project is already equipped with:
- **`.gitignore`**: Automatically prevents temporary cache files (`__pycache__`) from cluttering your repository.
- **`requirements.txt`**: Clear dependency manifest for Python users.
- **`.github/workflows/tests.yml`**: GitHub Actions automated CI workflow that tests your code automatically on every push!
- **`README.md`**: Beautiful documentation page displayed on your repository's homepage.
