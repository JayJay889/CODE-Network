# CODE Network

A contact management web application for the CODE community. Built with Python Flask and MongoDB (Atlas or self-hosted).

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [MongoDB Atlas Setup](#mongodb-atlas-setup-recommended-for-production)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Database Schema](#database-schema)
- [Usage](#usage)
- [Deployment](#deployment)
- [Development Notes](#development-notes)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [Support](#support)

## Features

✨ **Full CRUD Operations**
- ➕ Add new contacts with detailed information
- 📋 View all contacts in a searchable directory
- ✏️ Edit existing contact information
- 🗑️ Delete contacts with confirmation

🏷️ **Tags System**
- Categorize contacts (Speaker, Mentor, Sponsor, Alumni, Partner)
- Multiple tags per contact
- Color-coded tag badges

📱 **Responsive Design**
- Mobile-friendly layout
- Adapts to phone, tablet, and desktop screens
- CSS Grid and Flexbox layouts

🎯 **Additional Features**
- Recent contacts display on homepage
- LinkedIn and email links
- Professional, clean UI
- Duplicate email prevention with unique index
- Error handling for database operations
- Interactive user guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (tested with Python 3.13)
- **MongoDB** (local installation) OR **MongoDB Atlas** account (free tier available)
- **pip** (Python package manager)
- **Git** (for cloning the repository)

Optional but recommended:
- **Virtual environment tools** (`venv` or `virtualenv`)
- **MongoDB Compass** (GUI for MongoDB management)

## Quick Start

### 1. Install dependencies

```bash
cd Project.py
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file with your MongoDB connection string (Atlas or local):

```
MONGO_URI="your-mongodb-connection-string"
PORT=10000  # optional locally; Render supplies one in production
```

If `MONGO_URI` is not provided the app falls back to `mongodb://localhost:27017/contacts_db`, so you can skip this step for local testing if you already have MongoDB running on your machine.

### 3. Run the app

For production/Atlas:
```bash
bash run.sh
```

For local development with local MongoDB:
```bash
bash run_local.sh
```

Or manually:
```bash
python3 app.py
```

### 4. Open in browser

Visit: http://localhost:10000

Your MongoDB cluster/instance will automatically receive a `contacts` collection on first insert and a unique index on the `email` field.

## MongoDB Atlas Setup (Recommended for Production)

1. Create a free cluster at https://www.mongodb.com/cloud/atlas.
2. In **Database Access**, add a user with read/write permissions.
3. In **Network Access**, allow your IP (and Render’s IP range for deployment).
4. Create a database named `contacts_db` (optional—Mongo will create it on demand).
5. Copy the connection string from “Connect → Drivers” and store it as `MONGO_URI`.
6. Run the app once so it can create the `contacts` collection and the unique index on `email`.

## Project Structure

```
Project.py/
├── app.py                      # Main Flask application
├── models.py                   # Contact model and database schemas
├── views/                      # HTML templates
│   ├── Homepage.html           # Landing page with recent contacts
│   ├── Network.html            # All contacts directory
│   ├── add-contact.html        # Add contact form
│   ├── edit-contact.html       # Edit contact form
│   ├── contact-detail.html     # Individual contact view
│   └── Guide-on-how-to-use-it.html  # User guide
├── public/
│   ├── css/style.css           # Responsive styling
│   ├── js/script.js            # Client-side JavaScript
│   └── images/                 # Image assets
├── requirements.txt            # Python dependencies
├── run.sh                      # Production startup script
└── run_local.sh                # Local development startup script
```

## Technologies Used

**Backend:**
- Python 3.13
- Flask 3.1.2 (Web framework)
- Flask-PyMongo + PyMongo (MongoDB driver)
- MongoDB Atlas / MongoDB Community Edition

**Frontend:**
- HTML5
- CSS3 (Grid, Flexbox, Media Queries)
- Jinja2 (Template engine)

**Development:**
- python-dotenv (Environment variables)
- Virtual environment (venv)

## Database Schema

Each contact is stored as a MongoDB document in the `contacts` collection:

```
{
  "_id": ObjectId,
  "first_name": string,
  "last_name": string,
  "email": string (unique),
  "phone": string | null,
  "company": string | null,
  "position": string | null,
  "linkedin_url": string | null,
  "value_description": string | null,
  "tags": string | null,  # comma-separated until tag array support is added
  "user_id": string | null
}
```

## Usage

1. **Homepage** (`/`) - Overview with 5 most recent contacts
2. **View Network** (`/network`) - Browse all contacts directory
3. **Add Contact** (`/add-contact`) - Form to create new contacts
4. **Edit Contact** (`/edit-contact/<id>`) - Update existing contact information
5. **View Contact** (`/person/<id>`) - View detailed contact information
6. **Delete Contact** (`/delete-contact/<id>`) - Remove contacts
7. **Guide** (`/guide`) - User guide on how to use the application

## Deployment

### Render Deployment

1. **Create a new Web Service** on [Render](https://render.com)
2. **Connect your repository**
3. **Configure the service:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. **Add environment variables:**
   - `MONGO_URI`: Your MongoDB Atlas connection string
   - `PORT`: Automatically provided by Render
5. **Deploy** - Render will automatically build and start your app

### Other Platforms

The app can be deployed to any platform that supports Python web applications:
- **Heroku**: Use `Procfile` with `web: gunicorn app:app`
- **Railway**: Configure via `railway.toml` or dashboard
- **PythonAnywhere**: Upload files and configure WSGI
- **DigitalOcean App Platform**: Similar to Render configuration

## Development Notes

- Uses MongoDB for persistence (Atlas for production, local for dev)
- `Contact.init_indexes` enforces a unique index on `email`
- Responsive breakpoints: 600px (mobile), 768px (tablet), 1024px+ (desktop)
- Tags stored as comma-separated strings for now
- Two startup scripts available:
  - `./run.sh` - Production/general use (uses PORT from .env or defaults to 10000)
  - `./run_local.sh` - Local development (automatically uses local MongoDB)

## Troubleshooting

### MongoDB Connection Issues

**Problem:** `CRITICAL: Failed to initialize MongoDB connection`

**Solutions:**
- Verify your `MONGO_URI` is correctly formatted
- Check MongoDB Atlas IP whitelist (add `0.0.0.0/0` for testing)
- Ensure MongoDB service is running (if using local)
- Test connection with: `mongo "your-connection-string"`

### Duplicate Email Error

**Problem:** `Error: A contact with email [email] already exists`

**Solution:** This is expected behavior. Each email must be unique. Either:
- Use a different email address
- Delete the existing contact first
- Update the existing contact instead

### Port Already in Use

**Problem:** `OSError: [Errno 48] Address already in use`

**Solutions:**
- Change `PORT` in `.env` to a different value
- Kill the process using port 10000: `lsof -ti:10000 | xargs kill -9`
- Use a different port: `PORT=8080 python3 app.py`

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'flask'`

**Solutions:**
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`
- Create new venv: `python3 -m venv venv`

## Future Improvements

- 🔍 Search and filter functionality for contacts
- 📄 Pagination for large datasets
- 🔐 User authentication and authorization (Flask-Login/Auth0)
- 📊 Export contacts to CSV/Excel
- 🏷️ Convert tags to array type instead of comma-separated strings
- 📱 RESTful API endpoints for mobile app integration
- 📧 Email integration for contact communication
- 📈 Analytics dashboard for network insights
- 🔔 Notifications for contact updates
- 🌐 Multi-language support

## Contributing

Contributions are welcome! If you'd like to contribute to CODE Network:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows the existing style and includes appropriate comments.

## Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the [Troubleshooting](#troubleshooting) section
- Review the [User Guide](#usage) within the app

---

Built with ❤️ for the CODE community 🚀
