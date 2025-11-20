#!/usr/bin/env python3
"""
Test script to verify MongoDB Atlas connection.
Run this before starting the app to diagnose connection issues.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError, OperationFailure
import sys

def test_mongodb_connection():
    print("=" * 60)
    print("MongoDB Connection Test")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    
    # Check if MONGO_URI exists
    if not mongo_uri:
        print("❌ ERROR: MONGO_URI not found in environment variables")
        print("   Please check your .env file")
        return False
    
    # Show partial URI (hide password)
    safe_uri = mongo_uri[:30] + "..." if len(mongo_uri) > 30 else mongo_uri
    print(f"✓ MONGO_URI found: {safe_uri}")
    
    # Check if database name is in URI
    if "mongodb+srv://" in mongo_uri or "mongodb://" in mongo_uri:
        # Extract the part between @ and ?
        try:
            if "@" in mongo_uri and "/" in mongo_uri:
                host_part = mongo_uri.split("@")[1]
                if "/" in host_part:
                    db_name = host_part.split("/")[1].split("?")[0]
                    if db_name:
                        print(f"✓ Database name detected: {db_name}")
                    else:
                        print("⚠️  WARNING: No database name in URI (will use default 'test')")
                        print("   Add database name like: .../contacts_db?retryWrites=...")
        except Exception:
            pass
    
    print("\nAttempting connection...")
    
    try:
        # Create client
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ SUCCESS: Connected to MongoDB!")
        
        # Get database info
        db_name = client.get_default_database().name
        print(f"✓ Using database: {db_name}")
        
        # List collections
        collections = client.get_default_database().list_collection_names()
        print(f"✓ Collections: {collections if collections else '(none yet)'}")
        
        # Test write operation
        test_db = client.get_default_database()
        result = test_db.command("serverStatus")
        print(f"✓ MongoDB version: {result.get('version', 'unknown')}")
        
        print("\n" + "=" * 60)
        print("✅ All checks passed! Your app should work correctly.")
        print("=" * 60)
        return True
        
    except ConfigurationError as e:
        print(f"\n❌ CONFIGURATION ERROR: {e}")
        print("\nCommon fixes:")
        print("1. Check MONGO_URI format")
        print("2. Ensure database name is included: .../DATABASE_NAME?...")
        print("3. URL-encode special characters in password")
        return False
        
    except OperationFailure as e:
        print(f"\n❌ AUTHENTICATION ERROR: {e}")
        print("\nCommon fixes:")
        print("1. Verify username and password in MongoDB Atlas")
        print("2. Check Database Access settings in Atlas")
        print("3. Ensure user has readWrite permissions")
        return False
        
    except ConnectionFailure as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        print("\nCommon fixes:")
        print("1. Check Network Access in MongoDB Atlas")
        print("2. Whitelist your IP or use 0.0.0.0/0")
        print("3. Verify cluster is running")
        return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {type(e).__name__}: {e}")
        print("\nPlease check your MONGO_URI and Atlas configuration")
        return False

if __name__ == "__main__":
    success = test_mongodb_connection()
    sys.exit(0 if success else 1)

