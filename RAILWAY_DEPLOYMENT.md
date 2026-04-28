# Railway Deployment Guide for Vitalis AI

## Quick Deploy Steps

### 1. Prerequisites
- Railway account (sign up at https://railway.app)
- Git repository (GitHub, GitLab, or Bitbucket)

### 2. Push Your Code to Git
```bash
cd vitalis-ai
git init
git add .
git commit -m "Initial commit for Railway deployment"
git remote add origin <your-repo-url>
git push -u origin main
```

### 3. Deploy on Railway

#### Option A: Deploy from GitHub (Recommended)
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect the Python app and deploy

#### Option B: Deploy with Railway CLI
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

### 4. Configure Environment Variables

In Railway dashboard, add these environment variables:

**Required:**
- `SECRET_KEY` - Your Flask secret key (generate a strong random string)
- `GEMINI_API_KEY` - Your Google Gemini API key
- `DATABASE_URL` - Railway will auto-set this if you add PostgreSQL, or use `sqlite:///vitalis.db`

**Optional:**
- `FLASK_ENV` - Set to `production`
- `PORT` - Railway sets this automatically

### 5. Add PostgreSQL Database (Optional but Recommended)

For production, use PostgreSQL instead of SQLite:

1. In Railway dashboard, click "New" → "Database" → "Add PostgreSQL"
2. Railway will automatically set `DATABASE_URL` environment variable
3. Update your `requirements.txt` to include:
   ```
   psycopg2-binary==2.9.9
   ```
4. Redeploy

### 6. Domain Setup

Railway provides a free domain automatically. To use a custom domain:
1. Go to your service settings
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Update DNS records as instructed

## Files Created for Railway

- `nixpacks.toml` - Build configuration
- `Procfile` - Process configuration
- `runtime.txt` - Python version specification
- `requirements.txt` - Already exists with dependencies

## Important Notes

1. **Database**: SQLite works for development but use PostgreSQL for production
2. **Static Files**: Ensure `static/uploads` directory is writable
3. **Environment Variables**: Never commit `.env` file to git
4. **Logs**: View logs in Railway dashboard under "Deployments"

## Troubleshooting

### Build Fails
- Check `requirements.txt` for correct package versions
- Verify Python version in `runtime.txt`

### App Crashes
- Check Railway logs for errors
- Verify all environment variables are set
- Ensure database migrations are run

### Database Issues
- For SQLite: Data persists in Railway volumes
- For PostgreSQL: Use Railway's managed database

## Post-Deployment

1. Test all endpoints
2. Monitor logs for errors
3. Set up health checks
4. Configure auto-scaling if needed

## Useful Commands

```bash
# View logs
railway logs

# Open app in browser
railway open

# Run commands in Railway environment
railway run python migrate_db.py

# Link to existing project
railway link
```

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
