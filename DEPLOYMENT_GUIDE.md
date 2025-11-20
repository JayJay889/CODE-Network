# Deployment Guide

## Recommended Platform: Render

Render remains the simplest way to host this Flask + MongoDB app end-to-end. Render will run the Flask service while MongoDB Atlas stores the data.

---

## 1. Prepare MongoDB Atlas

1. Sign in at https://www.mongodb.com/cloud/atlas and create a **free Tier cluster**.
2. Create a **database user** (e.g., `render-user`) with a strong password and read/write access to all databases.
3. Allow Render’s IP range or just `0.0.0.0/0` in the **Network Access** tab (you can tighten the range later).
4. Create a database (e.g., `contacts_db`) and an empty collection named `contacts`. MongoDB will also create these automatically after the first insert if they don’t exist.
5. Copy the **connection string** from the “Connect” dialog, choosing the “Drivers” option. It looks like:
   ```
   mongodb+srv://render-user:<password>@cluster0.xxxxx.mongodb.net/contacts_db?retryWrites=true&w=majority
   ```
6. Store that value as `MONGO_URI` in your `.env` file locally so you can test against the same cluster.

> The application automatically creates a unique index on `contacts.email` the first time it runs, so no manual schema migration is required.

---

## 2. Verify the Application Locally

1. Install dependencies: `pip install -r requirements.txt`
2. Set `MONGO_URI` in `.env` (Atlas or local one).
3. Run `./run_local.sh` or `python3 app.py`
4. Visit `http://127.0.0.1:10000` and add a test contact to confirm the Atlas collection is populated.

---

## 3. Deploy to Render

### Prerequisites
1. GitHub repository containing the project
2. MongoDB Atlas connection string (from Step 1)
3. (Optional) Custom domain if desired

### Create the Service
1. Visit https://render.com and sign up/login with GitHub.
2. Click **New + → Web Service**.
3. Connect your GitHub repo and choose the default branch.
4. Configure the service:
   - **Environment:** Python 3
   - **Region:** pick the closest to your Atlas region to reduce latency
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free (good enough for testing)

### Environment Variables
Add the following in the Render dashboard:
- `MONGO_URI` = `<your Atlas connection string>`
- `PORT` = `10000` (Render sets `$PORT` automatically, but keeping the default in `.env` avoids surprises for other hosts)

No other database variables are required.

### Deploy
Click **Create Web Service**. Render will:
- Install dependencies (including Flask-PyMongo + PyMongo)
- Launch `gunicorn app:app`
- Expose a public URL such as `https://code-network.onrender.com`

Any deployment automatically runs `Contact.init_indexes`, so the unique constraint on `email` applies in production too.

---

## 4. Requirements Snapshot

`requirements.txt` already contains everything needed for MongoDB + Render:
```
blinker==1.9.0
click==8.3.0
Flask==3.1.2
Flask-PyMongo==2.3.0
pymongo==4.6.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
typing_extensions==4.15.0
Werkzeug==3.1.3
python-dotenv==1.0.0
dnspython==2.6.1
gunicorn==21.2.0
```

---

## 5. Post-Deployment Checklist

1. **Smoke test** the Render URL (create/edit/delete a contact).
2. **Monitor logs** in Render → Logs for any connection errors.
3. **Set up backups** in MongoDB Atlas (built-in snapshots on M0+ tiers).
4. **Restrict IPs** in Atlas once Render’s outbound addresses are known.
5. **Configure alerts** in Atlas (optional) for slow queries or disk usage.

---

## 6. Alternative Platforms (Optional)

- **Railway:** Similar workflow (GitHub + env vars). Supply `MONGO_URI` and use the same build/start commands.
- **Fly.io / Docker:** Containerize the app, inject `MONGO_URI`, and expose port `$PORT`.
- **PythonAnywhere:** Requires manual WSGI config; still just needs `MONGO_URI`.

---

## 7. Need Help?

1. Double-check `MONGO_URI` credentials if you see `Authentication failed` in logs.
2. Use `mongosh "<MONGO_URI>" --apiVersion 1` locally to verify Atlas connectivity.
3. Ensure Atlas Network Access allows Render’s IPs.
4. Confirm `gunicorn app:app` is spelled correctly (case-sensitive).

You’re ready to go live on Render with MongoDB Atlas 🚀

