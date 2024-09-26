import os
import json
import re
import time
from pymongo import MongoClient
from jsonschema import validate, ValidationError

class ContactManager:
    def __init__(self, db_name='contacts_db', collection_name='contacts'):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def normalize_phone(self, phone):
        """ Normalize phone number to a standard format. """
        phone_pattern = re.compile(r'^\+?\d{1,3}[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$')
        if phone_pattern.match(phone):
            # Assuming we want a format of +1XXXXXXXXXX
            return re.sub(r'\D', '', phone)  # Remove non-digit characters
        raise ValueError(f"Invalid phone number: {phone}")

    def validate_email(self, email):
        """ Validate email and check uniqueness in the database. """
        email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        if email_pattern.match(email):
            if not self.collection.find_one({"email": email}):
                return True
            raise ValueError(f"Email already exists: {email}")
        raise ValueError(f"Invalid email format: {email}")

    def insert_contacts(self, contacts):
        """ Insert contacts into the MongoDB collection. """
        for contact in contacts:
            try:
                contact['phone'] = self.normalize_phone(contact['phone'])
                self.validate_email(contact['email'])
                self.collection.insert_one(contact)
            except (ValueError, KeyError) as e:
                print(f"Error inserting contact {contact}: {e}")

    def process_contact_file(self, filepath):
        """ Process the contact JSON file. """
        attempts = 5  # Number of attempts to open the file
        for attempt in range(attempts):
            try:
                with open(filepath, 'r') as file:
                    contacts = json.load(file)
                    self.insert_contacts(contacts)
                break  # Exit loop if processing was successful
            except (PermissionError, FileNotFoundError):
                print(f"File {filepath} is not accessible. Retrying in 1 second...")
                time.sleep(1)  # Wait before retrying
            except json.JSONDecodeError:
                print(f"Invalid JSON in file: {filepath}")
                break
            except Exception as e:
                print(f"Error processing file {filepath}: {e}")
                break

    def cleanup(self):
        """ Cleanup actions after processing (if needed). """
        self.client.close()
