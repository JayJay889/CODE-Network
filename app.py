from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import pymongo
from models import Contact
load_dotenv()


port = int(os.getenv("PORT", 10000))

app = Flask(__name__, template_folder='views', static_folder='public')
# Configure MongoDB

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/contacts_db")


if not mongo_uri:
    raise ValueError("MONGO_URI is required. Please set it in your .env file or environment variables.")

print(f"Connecting to MongoDB with URI: {mongo_uri[:30]}...")  # Log first 30 chars for debugging


app.config["MONGO_URI"] = mongo_uri


try:
    mongo = PyMongo(app)

    if mongo.db is None:
        raise RuntimeError("PyMongo failed to initialize. mongo.db is None. Check your MONGO_URI format.")
    print(f"MongoDB connected successfully. Database: {mongo.db.name}")

except Exception as e:
    print(f"CRITICAL: Failed to initialize MongoDB connection: {e}")
    raise


with app.app_context():
    try:
        # Check if connection works
        mongo.db.command('ping')
        Contact.init_indexes(mongo)
    except Exception as e:
        print(f"Database connection/init warning: {e}")

@app.route('/')
def home():
    # last 5 people in Database
    try:
        if mongo.db is None:
            return "Database connection not available. Check MONGO_URI configuration.", 500

        recent_contacts = list(mongo.db.contacts.find().sort('_id', -1).limit(5))
        return render_template('Homepage.html', recent_contacts=recent_contacts)
    except Exception as e:
        return f"Database error: {str(e)}", 500

@app.route('/network')
def network():
    try:
        if mongo.db is None:
            return "Database connection not available. Check MONGO_URI configuration.", 500
        all_contacts = list(mongo.db.contacts.find())
        return render_template('Network.html', contacts=all_contacts)
    except Exception as e:
        return f"Database error: {str(e)}", 500

@app.route('/guide')
def guide():
    return render_template('Guide-on-how-to-use-it.html')


@app.route('/add-contact')
def add_contact_form():
    return render_template('add-contact.html')



@app.route('/add-contact', methods=['POST'])
def add_contact_submit():
    fname = request.form.get('first_name')
    lname = request.form.get('last_name')
    mail = request.form.get('email')
    phonenumber = request.form.get('phone')
    comp = request.form.get('company')
    pos = request.form.get('position')
    linkedin = request.form.get('linkedin_url')
    description = request.form.get('value_description')
    
    tag_list = request.form.getlist('tags')
    tags_str = ','.join(tag_list)
    
    # Create Contact object (Using the Model)
    new_contact = Contact(
        first_name=fname,
        last_name=lname,
        email=mail,
        phone=phonenumber,
        company=comp,
        position=pos,
        linkedin_url=linkedin,
        value_description=description,
        tags=tags_str,
        user_id=None # Placeholder for future auth integration
    )
    
    try:
        mongo.db.contacts.insert_one(new_contact.to_dict())
    except pymongo.errors.DuplicateKeyError:
        # Handle duplicate email error
        return f"Error: A contact with email {mail} already exists.", 400
    
    return redirect(url_for('network'))

@app.route('/edit-contact/<contact_id>')
def edit_contact_form(contact_id):
    person = mongo.db.contacts.find_one_or_404({'_id': ObjectId(contact_id)})
    return render_template('edit-contact.html', contact=person)

@app.route('/edit-contact/<contact_id>', methods=['POST'])
def edit_contact_submit(contact_id):
    # Update logic
    fname = request.form.get('first_name')
    lname = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    company = request.form.get('company')
    position = request.form.get('position')
    linkedin = request.form.get('linkedin_url')
    description = request.form.get('value_description')
    
    tag_list = request.form.getlist('tags')
    tags_str = ','.join(tag_list)
    
    try:
        mongo.db.contacts.update_one(
            {'_id': ObjectId(contact_id)},
            {'$set': {
                "first_name": fname,
                "last_name": lname,
                "email": email,
                "phone": phone,
                "company": company,
                "position": position,
                "linkedin_url": linkedin,
                "value_description": description,
                "tags": tags_str
            }}
        )
    except pymongo.errors.DuplicateKeyError:
         return f"Error: A contact with email {email} already exists.", 400
    return redirect(url_for('network'))


@app.route('/delete-contact/<contact_id>')
def delete_contact(contact_id):
    mongo.db.contacts.delete_one({'_id': ObjectId(contact_id)})
    return redirect(url_for('network'))

# Routing
@app.route('/contact/<id>')
def view_contact(id):
    person = mongo.db.contacts.find_one_or_404({'_id': ObjectId(id)})
    return render_template('contact-detail.html', contact=person)
@app.route('/person/<contact_id>')
def show_person(contact_id):
    p = mongo.db.contacts.find_one_or_404({'_id': ObjectId(contact_id)})
    return render_template('contact-detail.html', contact=p)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
