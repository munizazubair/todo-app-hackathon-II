# Deployment Guide - Phase II Todo Application

This guide covers deploying the full-stack todo application to production.

## Deployment Architecture

Recommended setup:
- **Frontend**: Vercel (optimized for Next.js)
- **Backend**: Railway / Render / Fly.io
- **Database**: Neon DB (serverless PostgreSQL)

## Prerequisites

- GitHub repository with your code
- Neon DB account (free tier available)
- Vercel account (free tier available)
- Railway/Render/Fly.io account (free tier available)

## Database Setup (Neon DB)

### 1. Create Neon Database

1. Go to [console.neon.tech](https://console.neon.tech)
2. Create a new project
3. Name it "todo-app-phase-ii"
4. Select region closest to your users
5. Copy the connection string

**Connection String Format:**
```
postgresql://[user]:[password]@[endpoint]/[dbname]?sslmode=require
```

### 2. Run Migrations

From your local machine:

```bash
cd backend

# Set DATABASE_URL environment variable
export DATABASE_URL="your-neon-connection-string"

# Run migrations
alembic upgrade head
```

## Backend Deployment

### Option A: Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Configure service:
   - **Root Directory**: `phase-II/backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT`

5. Add Environment Variables:
   ```
   DATABASE_URL=your-neon-connection-string
   API_HOST=0.0.0.0
   API_PORT=8000
   CORS_ORIGINS=https://your-frontend-domain.vercel.app
   ENVIRONMENT=production
   ```

6. Deploy and note the generated URL (e.g., `https://your-backend.railway.app`)

### Option B: Render

1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect your GitHub repository
4. Configure:
   - **Name**: todo-backend
   - **Root Directory**: `phase-II/backend`
   - **Runtime**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT`

5. Add Environment Variables (same as Railway)
6. Deploy

### Option C: Fly.io

1. Install Fly CLI: `https://fly.io/docs/hands-on/install-flyctl/`
2. Login: `fly auth login`
3. Navigate to backend directory: `cd phase-II/backend`
4. Initialize: `fly launch --no-deploy`
5. Edit `fly.toml`:

```toml
app = "todo-backend"

[build]

[env]
  API_HOST = "0.0.0.0"
  API_PORT = "8000"
  ENVIRONMENT = "production"

[[services]]
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

[[services.http_checks]]
  interval = 10000
  grace_period = "5s"
  method = "get"
  path = "/health"
  protocol = "http"
  timeout = 2000
```

6. Set secrets:
```bash
fly secrets set DATABASE_URL="your-neon-connection-string"
fly secrets set CORS_ORIGINS="https://your-frontend.vercel.app"
```

7. Deploy: `fly deploy`

## Frontend Deployment (Vercel)

### 1. Prepare Repository

Ensure `phase-II/frontend/next.config.js` has:

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  // ... other config
}

module.exports = nextConfig
```

### 2. Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `phase-II/frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

4. Add Environment Variables:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.railway.app/api
   ```

5. Deploy

### 3. Update CORS

After deployment, update backend CORS_ORIGINS to include your Vercel URL:

```bash
# On Railway/Render/Fly.io
CORS_ORIGINS=https://your-app.vercel.app,https://your-app-preview.vercel.app
```

## Docker Deployment (Alternative)

### Using Docker Compose

1. Clone repository on server
2. Navigate to `phase-II/`
3. Create `.env` file:

```env
# Database
POSTGRES_USER=todouser
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=tododb

# Backend
DATABASE_URL=postgresql://todouser:your-secure-password@db:5432/tododb
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://your-domain.com
ENVIRONMENT=production

# Frontend
NEXT_PUBLIC_API_URL=http://your-domain.com:8000/api
```

4. Run:
```bash
docker-compose up -d
```

Services will be available at:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Database: `localhost:5432`

## Post-Deployment

### 1. Verify Health Checks

```bash
# Backend health
curl https://your-backend.railway.app/health

# Frontend (should return 200)
curl https://your-app.vercel.app
```

### 2. Test API Endpoints

```bash
# Create a todo
curl -X POST https://your-backend.railway.app/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Test deployment"}'

# List todos
curl https://your-backend.railway.app/api/todos

# Get stats
curl https://your-backend.railway.app/api/todos/stats
```

### 3. Monitor Logs

**Railway:**
```bash
railway logs
```

**Render:**
Check dashboard → Logs tab

**Fly.io:**
```bash
fly logs
```

**Vercel:**
Check dashboard → Deployments → Logs

## Environment Variables Reference

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `API_HOST` | API host | `0.0.0.0` |
| `API_PORT` | API port | `8000` |
| `CORS_ORIGINS` | Allowed origins (comma-separated) | `https://app.vercel.app` |
| `ENVIRONMENT` | Environment name | `production` |

### Frontend (.env.local or Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://backend.railway.app/api` |

## Scaling Considerations

### Database (Neon DB)

- **Free tier**: 0.5 GB storage, 1 vCPU
- **Pro tier**: Auto-scaling, connection pooling
- Monitor with Neon dashboard

### Backend

- **Railway**: Auto-scaling with usage-based pricing
- **Render**: Configure instance type (starter/standard/pro)
- **Fly.io**: Scale with `fly scale count 2`

### Frontend (Vercel)

- Automatic CDN distribution
- Edge functions for optimal performance
- Unlimited bandwidth on Pro tier

## Security Checklist

- [ ] Database password is strong and secret
- [ ] DATABASE_URL uses SSL (`?sslmode=require`)
- [ ] CORS_ORIGINS only includes your frontend domain
- [ ] API keys are stored in environment variables, not code
- [ ] HTTPS enforced on all services
- [ ] Health check endpoints don't expose sensitive data

## Monitoring

### Application Performance

- **Vercel Analytics**: Enable in Vercel dashboard
- **Backend Logging**: Check Railway/Render/Fly logs
- **Database**: Neon dashboard shows query performance

### Error Tracking

Consider adding:
- **Sentry** for error tracking
- **LogRocket** for session replay
- **Datadog** for APM

## Rollback Procedure

### Vercel (Frontend)

1. Go to Deployments
2. Find previous successful deployment
3. Click "..." → Promote to Production

### Railway/Render (Backend)

1. Go to Deployments
2. Select previous version
3. Click "Redeploy"

### Fly.io (Backend)

```bash
fly releases
fly releases rollback <version>
```

## Troubleshooting

### Frontend can't connect to backend

**Check:**
1. `NEXT_PUBLIC_API_URL` is correct
2. Backend CORS includes frontend URL
3. Backend is running (check health endpoint)
4. Network tab in browser for errors

### Database connection fails

**Check:**
1. `DATABASE_URL` format is correct
2. Database is running (Neon dashboard)
3. SSL mode is specified (`?sslmode=require`)
4. IP allowlist (Neon allows all by default)

### Migrations fail

**Check:**
1. Alembic is installed
2. `DATABASE_URL` is set
3. Run `alembic current` to see current version
4. Run `alembic upgrade head` manually

## Cost Estimate (Free Tiers)

- **Neon DB**: Free (0.5 GB storage)
- **Railway**: $5/month credit (may require credit card)
- **Vercel**: Free (hobby plan)
- **Total**: ~$0-5/month for small projects

For production traffic, expect:
- **Neon Pro**: $19/month
- **Railway**: Usage-based (~$10-50/month)
- **Vercel Pro**: $20/month

## Support

- **Neon**: https://neon.tech/docs
- **Railway**: https://docs.railway.app
- **Vercel**: https://vercel.com/docs

## Next Steps

1. Set up custom domain
2. Configure SSL certificates
3. Set up monitoring and alerts
4. Enable backup strategy
5. Set up CI/CD pipeline
