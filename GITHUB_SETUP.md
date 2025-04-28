# Setting Up GitHub Repository and GitHub Pages

This guide will walk you through the process of setting up a GitHub repository for the API License project and enabling GitHub Pages to host the documentation.

## 1. Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in to your account.
2. Click on the "+" icon in the top-right corner and select "New repository".
3. Enter "api-license" as the repository name.
4. Choose whether the repository should be public or private.
5. Click "Create repository".

## 2. Push Your Code to GitHub

After creating the repository, push your code to GitHub:

```bash
# Initialize git repository (if not already done)
git init

# Add the remote repository
git remote add origin https://github.com/YOUR_USERNAME/api-license.git

# Add all files
git add .

# Commit the changes
git commit -m "Initial commit"

# Push to GitHub
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username or organization name.

## 3. Update Configuration Files

Before deploying to GitHub Pages, make sure to update the following files:

1. In `mkdocs.yml`, replace `USERNAME` in the `site_url` with your actual GitHub username or organization name:

```yaml
site_url: https://YOUR_USERNAME.github.io/api-license/
```

2. In `README.md`, replace `USERNAME` in the online documentation link with your actual GitHub username or organization name:

```markdown
[https://YOUR_USERNAME.github.io/api-license/](https://YOUR_USERNAME.github.io/api-license/)
```

## 4. Enable GitHub Pages

1. Go to your repository on GitHub.
2. Click on "Settings" tab.
3. Scroll down to the "Pages" section in the left sidebar.
4. Under "Source", select "Deploy from a branch".
5. Under "Branch", select "gh-pages" and "/(root)" folder, then click "Save".
6. GitHub will display a message saying "Your site is being built" and eventually provide the URL where your site is published.

## 5. Wait for the GitHub Actions Workflow

The GitHub Actions workflow (configured in `.github/workflows/deploy-docs.yml`) will automatically build and deploy the documentation to GitHub Pages whenever you push changes to the main branch.

1. Go to the "Actions" tab in your repository to monitor the workflow.
2. Once the workflow completes successfully, your documentation will be available at:
   `https://YOUR_USERNAME.github.io/api-license/`

## 6. Verify the Deployment

1. Visit your GitHub Pages URL to ensure the documentation is deployed correctly.
2. Check that all links and navigation work as expected.

## Troubleshooting

If you encounter issues with the GitHub Pages deployment:

1. Check the GitHub Actions logs for any errors.
2. Ensure that the repository has the necessary permissions to deploy to GitHub Pages.
   - Go to Settings > Actions > General > Workflow permissions
   - Make sure "Read and write permissions" is selected
3. Verify that the `gh-pages` branch has been created by the workflow.
4. Make sure the `site_url` in `mkdocs.yml` is correctly set.
5. If you're using a custom domain, make sure it's properly configured in the GitHub Pages settings.

For more information on GitHub Pages, see the [official documentation](https://docs.github.com/en/pages).