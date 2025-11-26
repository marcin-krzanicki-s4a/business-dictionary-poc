# 🚀 Deployment Guide - GitHub Pages

## Quick Start

### Option 1: Using the Helper Script (Recommended)

```bash
./deploy-to-github.sh
```

This script will:
- Initialize git repository (if needed)
- Add all files
- Create initial commit
- Push to GitHub
- Display next steps

### Option 2: Manual Setup

1. **Initialize Git Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: S4A Business Dictionary POC"
   ```

2. **Add Remote and Push**
   ```bash
   git remote add origin https://github.com/marcin-krzanicki-s4a/business-dictionary-poc.git
   git branch -M main
   git push -u origin main
   ```

3. **Configure GitHub Pages**
   - Go to: https://github.com/marcin-krzanicki-s4a/business-dictionary-poc/settings/pages
   - Under **Source**, select **GitHub Actions**
   - Save

4. **Wait for Deployment**
   - Go to the **Actions** tab
   - Wait for the workflow to complete (usually 1-2 minutes)
   - Your site will be live at: `https://marcin-krzanicki-s4a.github.io/business-dictionary-poc/`

## 🔄 Updating the Site

After the initial setup, any push to the `main` branch will automatically trigger a new deployment:

```bash
git add .
git commit -m "Update: description of changes"
git push
```

## 🛠️ Workflow Details

The GitHub Actions workflow (`.github/workflows/hugo.yml`) does the following:

1. **Build Job**
   - Installs Hugo Extended v0.152.2
   - Checks out the repository
   - Builds the site with `hugo --minify`
   - Uploads the built site as an artifact

2. **Deploy Job**
   - Takes the artifact from the build job
   - Deploys it to GitHub Pages

## 🌐 Custom Domain (Optional)

To use a custom domain:

1. Add a `CNAME` file to the `static/` directory:
   ```bash
   echo "dictionary.s4a.com" > static/CNAME
   ```

2. Configure DNS:
   - Add a CNAME record pointing to: `marcin-krzanicki-s4a.github.io`

3. Update `hugo.yaml`:
   ```yaml
   baseURL: https://dictionary.s4a.com/
   ```

4. In GitHub Settings → Pages, add your custom domain

## 🐛 Troubleshooting

### Deployment Fails

1. Check the **Actions** tab for error messages
2. Ensure Hugo version matches (v0.152.2)
3. Verify all files are committed and pushed

### Site Shows 404

1. Wait 2-3 minutes after first deployment
2. Check GitHub Pages settings are correct
3. Verify the workflow completed successfully

### Links Don't Work

1. Ensure `baseURL` in `hugo.yaml` matches your GitHub Pages URL
2. The workflow automatically sets the correct baseURL during build

## 📊 Monitoring

- **Build Status**: Check the Actions tab for workflow runs
- **Site Status**: Visit the Pages settings to see deployment status
- **Logs**: Click on any workflow run to see detailed logs

## 🔒 Security

- The workflow uses `GITHUB_TOKEN` which is automatically provided
- No additional secrets needed for basic deployment
- Permissions are minimal (read contents, write pages)

## 📝 Notes

- First deployment may take 5-10 minutes
- Subsequent deployments are faster (1-2 minutes)
- The `public/` directory is ignored in git (built on GitHub)
- Local development uses `http://localhost:1313/`
- Production uses the GitHub Pages URL automatically
