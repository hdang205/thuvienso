# Deployment Guide - Thư Viện Số FBU

## Overview

This guide walks through deploying the digital library system to production using:

- **Frontend**: GitHub Pages (free, fast, automatic)
- **Backend**: Railway (Django-friendly, easy deployment)
- **Database**: PostgreSQL (on Railway or another service)

## Prerequisites

Before starting, you need:

- GitHub account with repository access
- Railway account (free tier available)
- PostgreSQL database (can be hosted on Railway)
- A custom domain (optional)

## Step 1: Prepare Backend for Production

### 1.1 Generate Secret Key

```bash
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy this value for use in environment variables.

### 1.2 Create Production Environment

Copy `.env.production.example` to `.env.production` and update:

```bash
cp .env.production.example .env.production
```

Edit `.env.production` with your production settings:

- `SECRET_KEY`: Use the value generated above
- `DEBUG`: Set to False
- `ALLOWED_HOSTS`: Your production domain(s)
- `DATABASE_URL`: Your PostgreSQL connection string
- `CORS_ALLOWED_ORIGINS`: Your frontend URLs

### 1.3 Create PostgreSQL Database

**Option A: Using Railway (Recommended)**

1. Go to [railway.app](https://railway.app)
2. Create new project → Add PostgreSQL
3. Copy the DATABASE_URL from Railway dashboard
4. Update `.env.production` with this URL

**Option B: Using Other Services**

- PlanetScale (MySQL)
- Supabase (PostgreSQL)
- AWS RDS
- DigitalOcean Managed Databases

### 1.4 Update Django Settings

Update `thuvienso_backend/settings.py`:

```python
# Use environment variables
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Database from URL
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# CORS
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
```

## Step 2: Deploy Backend to Railway

### 2.1 Connect Railway to GitHub

1. Go to [railway.app/dashboard](https://railway.app/dashboard)
2. Create new project
3. Select "Deploy from GitHub repo"
4. Select your repository and branch (main)
5. Click Deploy

### 2.2 Configure Railway Environment Variables

In Railway dashboard for your project:

1. Go to Variables tab
2. Add all variables from `.env.production`:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS`
   - `DATABASE_URL` (if using Railway PostgreSQL)
   - `CORS_ALLOWED_ORIGINS`
   - Other settings from `.env.production`

### 2.3 Set up Railway PostgreSQL

1. In Railway project, click "Add Service"
2. Select "PostgreSQL"
3. Railway auto-populates `DATABASE_URL` in your environment
4. Run migrations:
   - Go to Railway dashboard
   - Select your project
   - In Deployments tab, click latest deployment
   - In Shell, run: `python manage.py migrate`
   - Then: `python manage.py createsuperuser` (for admin access)

### 2.4 Get Backend URL

In Railway dashboard, go to your Django service → Settings → Domain
Copy your railway.app domain (or set custom domain)

Example: `https://thuvienso-api.railway.app`

## Step 3: Build & Deploy Frontend to GitHub Pages

### 3.1 Update Backend URL

In `src/config.js`, update production API_BASE:

```javascript
production: {
  API_BASE: 'https://thuvienso-api.railway.app/api', // Your backend URL
  DEBUG: false,
},
```

### 3.2 Build Frontend

```bash
npm run build
```

This creates a `dist/` folder with production-ready files.

### 3.3 Enable GitHub Pages

1. Go to repository Settings → Pages
2. Under "Source", select "Deploy from a branch"
3. Select branch: `gh-pages`
4. Save

### 3.4 Deploy to GitHub Pages

Push to main branch to trigger automatic deployment:

```bash
git add .
git commit -m "feat(deploy): prepare for production deployment"
git push origin main
```

GitHub Actions will:

1. Run all tests
2. Build frontend
3. Deploy to GitHub Pages

Your frontend will be available at: `https://yourusername.github.io/thuvienso`

### 3.5 (Optional) Set Up Custom Domain

If you have a custom domain:

1. Go to repository Settings → Pages
2. Under "Custom domain", enter your domain
3. Click Save
4. GitHub will create a CNAME file automatically
5. Add DNS records to your domain registrar:
   - CNAME: `yourdomain.com` → `yourusername.github.io`
   - (Or use A records if domain registrar supports it)

## Step 4: Configure CORS

Update `thuvienso_backend/settings.py` for your production domains:

```python
CORS_ALLOWED_ORIGINS = [
    'https://yourusername.github.io',
    'https://yourdomain.com',  # if using custom domain
]
```

Deploy backend after updating.

## Step 5: Test Production Deployment

### 5.1 Test Backend API

```bash
curl -X GET https://your-backend-url/api/books/
```

You should get a 401 Unauthorized (expected without authentication).

### 5.2 Test Frontend

1. Open `https://yourusername.github.io/thuvienso` in browser
2. Try to register a new user
3. Try to login
4. Check if books load
5. Test borrow/return functionality

### 5.3 Check Logs

Monitor your deployments:

**Backend (Railway)**:

- Go to Railway dashboard
- Select your project
- Check Deployments tab for errors

**Frontend (GitHub)**:

- Go to GitHub repository
- Check Actions tab for workflow logs

## Step 6: Post-Deployment Checklist

- [ ] Backend API is running and accessible
- [ ] Frontend loads without errors
- [ ] Authentication (login/register) works
- [ ] Books display correctly
- [ ] Loan operations work
- [ ] No console errors in browser
- [ ] HTTPS is working for both frontend and backend
- [ ] Automated tests pass on every push
- [ ] Database backups are configured
- [ ] Error monitoring is set up (optional: Sentry)

## Step 7: Monitoring & Maintenance

### 7.1 Set Up Error Tracking (Optional)

Use Sentry for error tracking:

1. Create [sentry.io](https://sentry.io) account
2. Create new Django project
3. Get your SENTRY_DSN
4. Add to Railway environment variables: `SENTRY_DSN=your-dsn`

### 7.2 Database Backups

**Railway PostgreSQL**: Automatic daily backups included

**Important**: Manually backup critical data regularly

### 7.3 Monitor Deployment Health

- Check GitHub Actions regularly for failed tests
- Monitor Railway logs for backend errors
- Set up alerts (Railway has built-in notifications)

## Troubleshooting

### Issue: Frontend gets 404 errors

**Solution**: Ensure `CORS_ALLOWED_ORIGINS` in backend includes your frontend domain

### Issue: GitHub Pages shows 404

**Solution**: Check that build succeeded in Actions tab, and `.env.production` has correct production values

### Issue: Database connection fails

**Solution**: Verify `DATABASE_URL` is correct on Railway, and migrations have run

### Issue: Changes not updating

**Solution**:

- Clear browser cache (Ctrl+Shift+Del)
- Force push to repo: `git push --force origin main`
- Check GitHub Actions log for deployment errors

## Rollback Procedure

If deployment breaks:

1. **Frontend**: Push previous working commit to main
2. **Backend**: Use Railway's rollback feature (Deployments tab → Previous version)

## Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Django Deployment Guide](https://docs.djangoproject.com/en/6.0/howto/deployment/)
- [PostgreSQL on Railway](https://docs.railway.app/databases/postgresql)

## Support

For issues or questions:

1. Check GitHub Issues in the repository
2. Review server logs (Railway dashboard)
3. Check browser console for frontend errors
4. Review GitHub Actions logs for deployment issues
