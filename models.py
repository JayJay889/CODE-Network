from pymongo import ASCENDING

class Contact:
    """
    Contact Model mirroring the SQL schema but adapted for MongoDB.
    """
    def __init__(self, first_name, last_name, email, phone=None, company=None, position=None, linkedin_url=None, value_description=None, tags=None, user_id=None, _id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.company = company
        self.position = position
        self.linkedin_url = linkedin_url
        self.value_description = value_description
        self.tags = tags
        self.user_id = user_id  # reserved for future auth integration (e.g., Supabase, Auth0)
        self._id = _id

    def to_dict(self):
        """Converts the object to a dictionary for MongoDB insertion."""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "position": self.position,
            "linkedin_url": self.linkedin_url,
            "value_description": self.value_description,
            "tags": self.tags,
            "user_id": self.user_id
        }

    @staticmethod
    def init_indexes(mongo):
        """
        Creates necessary indexes for the contacts collection.
        Equivalent to SQL constraints (e.g., UNIQUE).
        """
        try:
            # Create unique index on email
            mongo.db.contacts.create_index([("email", ASCENDING)], unique=True)
            print("Indexes created successfully.")
        except Exception as e:
            print(f"Error creating indexes: {e}")

