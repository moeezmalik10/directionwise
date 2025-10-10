# Streamlit Cloud Deployment Guide

## Changes Made for Streamlit Cloud Compatibility

### 1. Updated requirements.txt
- Removed `spacy>=3.8.0` (causes installation issues on Streamlit Cloud)
- Kept essential dependencies: numpy, pandas, streamlit, sqlalchemy, plotly, nltk, scikit-learn, reportlab, requests

### 2. Replaced spaCy with NLTK
- Removed spaCy imports and model loading
- Replaced spaCy named entity recognition with NLTK alternatives
- Added NLTK data downloads for required components

### 3. Updated Database Configuration
- Modified `counselor_core.py` to support cloud databases
- Added environment variable `DATABASE_URL` support
- Added PostgreSQL URL format handling

## Deployment Steps

### Step 1: Set up Cloud Database (Required)
Since Streamlit Cloud doesn't support persistent SQLite, you need a cloud database:

**Option A: Supabase (Free)**
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Settings > Database
4. Copy the connection string
5. Format: `postgresql://postgres:[password]@[host]:5432/postgres`

**Option B: Railway (Free)**
1. Go to [railway.app](https://railway.app)
2. Create a new PostgreSQL database
3. Copy the connection string

### Step 2: Deploy to Streamlit Cloud
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set main file path: `app.py`
5. Add environment variable:
   - Key: `DATABASE_URL`
   - Value: Your PostgreSQL connection string
6. Deploy!

### Step 3: Verify Deployment
- Check that the app loads without errors
- Test the quiz functionality
- Verify database operations work

## Troubleshooting

### Common Issues:
1. **Database connection errors**: Ensure DATABASE_URL is correctly set
2. **NLTK data missing**: The app will download required NLTK data automatically
3. **Memory issues**: Streamlit Cloud has memory limits; the app is optimized for these constraints

### If deployment still fails:
1. Check Streamlit Cloud logs for specific error messages
2. Ensure all dependencies in requirements.txt are compatible
3. Consider using a lighter version of scikit-learn if needed

## Alternative Deployment Options

If Streamlit Cloud continues to have issues:

1. **Heroku**: Better for Python apps with databases
2. **Railway**: Good for full-stack applications
3. **DigitalOcean App Platform**: More control over the environment
4. **Google Cloud Run**: Serverless with more resources

## Environment Variables Needed

- `DATABASE_URL`: PostgreSQL connection string (required for cloud deployment)
- Optional: `SECRET_KEY` for enhanced security
