# CODE Network

A contact management web application for the CODE community. Built with Python Flask and MongoDB (Atlas or self-hosted).

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

```bash
bash run.sh
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
├── app.py              # Main Flask application
├── views/              # HTML templates
│   ├── Homepage.html
│   ├── Network.html
│   ├── add-contact.html
│   └── edit-contact.html
├── public/
│   ├── css/style.css   # Responsive styling
│   └── images/         # Image assets
├── requirements.txt    # Python dependencies
└── run.sh             # Startup script
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

1. **Homepage** - Overview with recent contacts
2. **View Network** - Browse all contacts with filtering
3. **Add Contact** - Form to create new contacts
4. **Edit Contact** - Update existing contact information
5. **Delete Contact** - Remove contacts (with confirmation)

## Development Notes

- Uses MongoDB for persistence (Atlas for production, local for dev)
- `Contact.init_indexes` enforces a unique index on `email`
- Responsive breakpoints: 600px (mobile), 768px (tablet), 1024px+ (desktop)
- Tags stored as comma-separated strings for now
- Run `./run_local.sh` to start with a local MongoDB connection string automatically

## Future Improvements

- Search functionality
- Pagination for large datasets
- User authentication (Flask-Login)
- Export contacts to CSV
- Database migrations (Flask-Migrate)
- API endpoints for mobile app

---

Built for the CODE community 🚀
