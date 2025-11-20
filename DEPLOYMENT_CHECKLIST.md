# Deployment Checklist for Render + MongoDB Atlas 🚀

## ✅ Pre-Deployment Verification

### 1. MongoDB Atlas Configuration
- [ ] Cluster created and running
- [ ] Database user created with username and password
- [ ] User has `readWrite` permissions (or `Atlas admin`)
- [ ] Network Access allows `0.0.0.0/0` (for Render deployment)
- [ ] Connection string copied from Atlas "Connect → Drivers"

### 2. Local Environment Setup
- [ ] `.env` file exists in `/Users/Jesper/Se_Code_CURSOR/Project.py/`
- [ ] `MONGO_URI` includes database name: `mongodb+srv://user:pass@host/DATABASE_NAME?options`
- [ ] Tested connection locally with `python3 test_mongodb_connection.py`
- [ ] App runs successfully with `python3 app.py`
- [ ] Can create/view/edit/delete contacts locally

### 3. Code Verification
- [ ] No SQLAlchemy dependencies (✅ already removed)
- [ ] No SQLite references (✅ already removed)
- [ ] No Supabase references (✅ already removed)
- [ ] `requirements.txt` contains Flask-PyMongo, pymongo, gunicorn
- [ ] `app.py` uses `PyMongo(app)` correctly
- [ ] All routes have error handling

### 4. Files Ready for Deployment
- [ ] `app.py` - Main application
- [ ] `models.py` - Contact model
- [ ] `requirements.txt` - Dependencies
- [ ] `views/` - HTML templates
- [ ] `public/` - CSS, JS, images
- [ ] `.gitignore` - Excludes .env, venv, __pycache__

---

## 🚀 Render Deployment Steps

### Step 1: Push to GitHub
```bash
cd /Users/Jesper/Se_Code_CURSOR
git add Project.py/
git commit -m "MongoDB migration complete - ready for Render"
git push origin main
```

**Important:** Verify `.env` is NOT committed (should be in `.gitignore`)

### Step 2: Create Render Web Service
1. Go to https://render.com/dashboard
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Select the repository containing your code
5. Click **Connect**

### Step 3: Configure Service Settings
Fill in these settings:

**Basic Settings:**
- **Name:** `code-network` (or your preferred name)
- **Region:** Choose closest to your Atlas cluster region
- **Branch:** `main` (or your default branch)
- **Root Directory:** `Project.py`
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

**Instance Type:**
- **Plan:** `Free` (for testing) or `Starter` (for production)

### Step 4: Add Environment Variables
Click **Advanced** → **Add Environment Variable**

Add these variables:
1. **MONGO_URI**
   - Value: `mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/contacts_db?retryWrites=true&w=majority`
   - (Use your actual Atlas connection string with database name)

2. **PORT** (optional, Render sets this automatically)
   - Value: `10000`

**Double-check:** 
- ✅ MONGO_URI includes `/contacts_db` (or your database name)
- ✅ Password is correct and special chars are URL-encoded if needed
- ✅ No extra spaces or quotes

### Step 5: Deploy
1. Click **Create Web Service**
2. Render will:
   - Clone your repo
   - Run `pip install -r requirements.txt`
   - Start `gunicorn app:app`
   - Assign a public URL

### Step 6: Monitor Deployment
Watch the logs in Render dashboard for:
```
Connecting to MongoDB with URI: mongodb+srv://...
MongoDB connected successfully. Database: contacts_db
Indexes created successfully.
```

If you see these lines, deployment succeeded! ✅

---

## 🔍 Post-Deployment Testing

### Test Your Live App
Your app will be available at: `https://your-app-name.onrender.com`

Test all features:
1. [ ] Homepage loads and shows recent contacts (or empty state)
2. [ ] Navigate to Network page
3. [ ] Add a new contact
4. [ ] View contact details
5. [ ] Edit a contact
6. [ ] Delete a contact
7. [ ] Verify changes persist (refresh the page)

### Check MongoDB Atlas
1. Go to Atlas dashboard
2. Click **Browse Collections**
3. Verify `contacts_db.contacts` collection exists
4. Verify contacts are being saved
5. Verify the unique index on `email` field exists

---

## 🐛 Troubleshooting

### Deployment Fails
**Check Render logs for:**
- `CRITICAL: Failed to initialize MongoDB connection` → Fix MONGO_URI
- `Authentication failed` → Check username/password in Atlas
- `Connection timeout` → Check Atlas Network Access
- `No module named 'flask_pymongo'` → Check requirements.txt

### App Shows Database Error
1. Check Render logs for exact error
2. Verify MONGO_URI in Render environment variables
3. Test the URI locally with `test_mongodb_connection.py`
4. Ensure Network Access allows `0.0.0.0/0`

### Common Fixes
1. **Missing database name in URI:** Add `/contacts_db` before `?`
2. **Special chars in password:** URL-encode them (`@` → `%40`)
3. **IP not whitelisted:** Add `0.0.0.0/0` in Atlas Network Access
4. **Wrong credentials:** Go to Database Access in Atlas and reset password

---

## 📋 Quick Reference

### Your MongoDB Atlas Connection String Format
```
mongodb+srv://USERNAME:PASSWORD@CLUSTER.mongodb.net/DATABASE_NAME?retryWrites=true&w=majority
```

### Example (replace with your values)
```
mongodb+srv://render-user:SecurePass123@cluster0.abc123.mongodb.net/contacts_db?retryWrites=true&w=majority
```

### Render Build Settings
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### Test Connection Locally
```bash
cd /Users/Jesper/Se_Code_CURSOR/Project.py
source venv/bin/activate
python3 test_mongodb_connection.py
python3 app.py
```

---

## ✨ Success Indicators

You'll know everything is working when:
- ✅ Render deployment shows "Live" status
- ✅ Logs show "MongoDB connected successfully"
- ✅ Your app URL loads the homepage
- ✅ You can add/edit/delete contacts
- ✅ Data persists after refresh
- ✅ Atlas shows documents in `contacts` collection

---

## 🎯 Final Notes

- Old SQLite database (`instance/contacts.db`) is no longer used
- All data now lives in MongoDB Atlas
- Render automatically redeploys on git push
- Free tier may spin down after inactivity (cold starts take ~30s)
- Monitor Atlas for storage usage (free tier: 512MB)

**You're all set!** 🚀

If you encounter issues, check `MONGODB_TROUBLESHOOTING.md` and `FIX_APPLIED.md` for detailed help.

