from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='views', static_folder='public')

# Database setup - Supabase PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SUPABASE_DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    position = db.Column(db.String(100))
    linkedin_url = db.Column(db.String(200))
    value_description = db.Column(db.Text)

# Routes
@app.route('/')
def home():
    return render_template('Homepage.html')

@app.route('/network')
def network():
    contacts = Contact.query.all()
    return render_template('Network.html', contacts=contacts)

@app.route('/guide')
def guide():
    return render_template('Guide-on-how-to-use-it.html')

@app.route('/add-contact')
def add_contact_form():
    return render_template('add-contact.html')

@app.route('/add-contact', methods=['POST'])
def add_contact_submit():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    company = request.form.get('company')
    position = request.form.get('position')
    linkedin_url = request.form.get('linkedin_url')
    value_description = request.form.get('value_description')
    
    new_contact = Contact(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        company=company,
        position=position,
        linkedin_url=linkedin_url,
        value_description=value_description
    )
    
    db.session.add(new_contact)
    db.session.commit()
    
    return redirect(url_for('network'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)
