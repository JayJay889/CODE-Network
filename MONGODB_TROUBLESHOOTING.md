# MongoDB Atlas Connection Troubleshooting

## The Error: `'NoneType' object has no attribute 'contacts'`

This error means `mongo.db` is `None`, indicating PyMongo failed to initialize properly.

## Root Causes & Solutions

### 1. **MONGO_URI Format Issues (Most Common)**

Your MongoDB Atlas URI must include the database name. The correct format is:

```
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/DATABASE_NAME?retryWrites=true&w=majority
```

**Key points:**
- ✅ Include `/DATABASE_NAME` before the `?` query parameters
- ✅ Replace `DATABASE_NAME` with your actual database name (e.g., `contacts_db`)
- ❌ Don't use just `mongodb+srv://.../?retryWrites=true` (missing database name)

**Example:**
```bash
# WRONG - missing database name
MONGO_URI="mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"

# CORRECT - includes database name
MONGO_URI="mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/contacts_db?retryWrites=true&w=majority"
```

### 2. **Check Your .env File**

Open `/Users/Jesper/Se_Code_CURSOR/Project.py/.env` and verify:

```bash
MONGO_URI="mongodb+srv://your-username:your-password@cluster0.xxxxx.mongodb.net/contacts_db?retryWrites=true&w=majority"
PORT=10000
```

**Important:**
- No spaces around the `=` sign
- Use double quotes around the URI
- Replace `<password>` placeholder with your actual password
- Replace `your-username` with your Atlas database user
- Include the database name (`contacts_db`) in the path

### 3. **Network Access in MongoDB Atlas**

1. Go to MongoDB Atlas dashboard
2. Click **Network Access** in the left sidebar
3. Ensure your IP is whitelisted OR add `0.0.0.0/0` to allow all IPs (for testing)
4. For Render deployment, you need to allow `0.0.0.0/0` since Render uses dynamic IPs

### 4. **Database User Permissions**

1. Go to **Database Access** in MongoDB Atlas
2. Verify your user has:
   - ✅ Read and write permissions
   - ✅ Built-in Role: `readWrite` or `Atlas admin`
3. Password must not contain special characters that need URL encoding (`@`, `:`, `/`, etc.)
   - If it does, URL-encode them: `@` → `%40`, `:` → `%3A`, etc.

### 5. **Test Connection Locally**

Run this command to test your connection string:

```bash
cd /Users/Jesper/Se_Code_CURSOR/Project.py
source venv/bin/activate
python3 -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); client = MongoClient(os.getenv('MONGO_URI')); print('Connected:', client.server_info())"
```

If this fails, your MONGO_URI is incorrect.

### 6. **Check Application Logs**

When you start the app, you should see:

```
Connecting to MongoDB with URI: mongodb+srv://...
MongoDB connected successfully. Database: contacts_db
Indexes created successfully.
```

If you see:
- `CRITICAL: Failed to initialize MongoDB connection` → Check MONGO_URI format
- `Authentication failed` → Check username/password
- `Connection timeout` → Check Network Access whitelist

## For Render Deployment

1. Go to Render Dashboard → Your Web Service → Environment
2. Add environment variable:
   - **Key:** `MONGO_URI`
   - **Value:** Your full Atlas connection string (with database name)
3. Click **Save Changes** and redeploy

## Quick Checklist

- [ ] MONGO_URI includes `/DATABASE_NAME` before query params
- [ ] Password is correctly URL-encoded if it has special chars
- [ ] Network Access allows your IP (or `0.0.0.0/0` for testing)
- [ ] Database user has `readWrite` permissions
- [ ] `.env` file is in `/Users/Jesper/Se_Code_CURSOR/Project.py/` directory
- [ ] You ran `source venv/bin/activate` before starting the app
- [ ] The database name in MONGO_URI matches what you created in Atlas

## Still Not Working?

Run the app and share the complete error output. The logs will show exactly what's failing:

```bash
cd /Users/Jesper/Se_Code_CURSOR/Project.py
source venv/bin/activate
python3 app.py
```

Look for the lines starting with:
- `Connecting to MongoDB with URI:`
- `CRITICAL: Failed to initialize MongoDB connection:`

This will tell us the exact issue.

