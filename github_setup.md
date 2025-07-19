# GitHub Setup Instructions

Follow these steps to push your Coin Counter project to GitHub:

## 1. Create a GitHub Repository

1. Go to [GitHub](https://github.com/) and sign in to your account
2. Click on the "+" icon in the top right corner and select "New repository"
3. Name your repository (e.g., "coin-counter")
4. Add a description (optional): "A Python application for detecting and counting coins in images"
5. Choose "Public" or "Private" visibility
6. Do NOT initialize the repository with a README, .gitignore, or license (we already have these files)
7. Click "Create repository"

## 2. Initialize and Push Your Local Repository

Open a command prompt or terminal in your project directory and run the following commands:

```bash
# Initialize a git repository
git init

# Add all files to the repository (excluding those in .gitignore)
git add .

# Commit the files
git commit -m "Initial commit"

# Add the GitHub repository as a remote
git remote add origin https://github.com/YOUR_USERNAME/coin-counter.git

# Push to GitHub
git push -u origin main
```

Note: If your default branch is named "master" instead of "main", use:
```bash
git push -u origin master
```

## 3. Update README.md

After pushing to GitHub, update the README.md file with your actual GitHub repository URL.

## 4. Additional Tips

- Make sure to replace "YOUR_USERNAME" with your actual GitHub username
- If you encounter authentication issues, you may need to use a personal access token or set up SSH keys
- Consider adding a license file if you want to specify how others can use your code
- You might want to add screenshots of the application to the README.md file