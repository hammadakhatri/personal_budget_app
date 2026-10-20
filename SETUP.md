# Setup Instructions for Neon PostgreSQL + OAuth

## 🚀 Quick Start Guide

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit>=1.42` - For OAuth support
- `python-dotenv` - Environment variables
- `Authlib>=1.3.2` - OAuth client
- `psycopg2-binary` - PostgreSQL driver
- `plotly` - Charts

### Step 2: Configure Secrets

Edit `.streamlit/secrets.toml` and replace the placeholders:

```toml
[oidc.google]
client_id = "${OAUTH_CLIENT_ID}"  # Replace with actual Google Client ID
client_secret = "${OAUTH_CLIENT_SECRET}"  # Replace with actual secret
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

[oidc]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "GENERATE_RANDOM_SECRET_HERE"  # Generate with: python -c "import secrets; print(secrets.token_hex(32))"
```

**To generate cookie_secret:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 3: Run Database Migration

```bash
python migrate_to_neon.py
```

This will:
- Create all tables in Neon PostgreSQL
- Enable Row-Level Security (RLS)
- Create indexes for performance

### Step 4: Run the App

```bash
streamlit run app.py
```

---

## 🔐 Google OAuth Setup

### 1. Go to Google Cloud Console
Visit: https://console.cloud.google.com

### 2. Create/Select Project
- Create a new project or select existing one

### 3. Enable Google+ API
- Go to "APIs & Services" → "Library"
- Search for "Google+ API"
- Click "Enable"

### 4. Create OAuth Credentials
- Go to "APIs & Services" → "Credentials"
- Click "Create Credentials" → "OAuth 2.0 Client ID"
- Application type: "Web application"
- Name: "Budget App"

### 5. Configure Authorized Redirect URIs
Add:
- `http://localhost:8501/oauth2callback` (for local development)
- `https://your-production-domain.com/oauth2callback` (for production)

### 6. Copy Credentials
- Copy the **Client ID** and **Client Secret**
- Paste them into `.streamlit/secrets.toml`

---

## ✅ Verification Checklist

- [ ] `.env` file has `NEON_DB_KEY` with PostgreSQL connection string
- [ ] `.streamlit/secrets.toml` has Google OAuth credentials
- [ ] `cookie_secret` is generated and added to secrets.toml
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database migration completed (`python migrate_to_neon.py`)
- [ ] App runs without errors (`streamlit run app.py`)
- [ ] Can login with Google account
- [ ] Can create wallets/categories/transactions
- [ ] Can logout successfully

---

## 🐛 Troubleshooting

### "NEON_DB_KEY not found"
- Check `.env` file exists in project root
- Verify `NEON_DB_KEY` is set correctly

### "OAuth redirect URI mismatch"
- Ensure redirect URI in Google Cloud Console matches exactly
- For local: `http://localhost:8501/oauth2callback`
- No trailing slashes!

### "Row-Level Security" errors
- Run `python migrate_to_neon.py` again
- Check Neon database connection

### Can't login
- Verify Google OAuth credentials in `secrets.toml`
- Check browser console for errors
- Ensure Streamlit version >= 1.42

---

## 📝 Environment Variables

Your `.env` file should contain:
```env
NEON_DB_KEY=postgresql://user:password@host/database?sslmode=require
OAUTH_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
OAUTH_CLIENT_SECRET=your_google_client_secret
```

**Note**: The `.streamlit/secrets.toml` file references these environment variables using `${VARIABLE_NAME}` syntax.
