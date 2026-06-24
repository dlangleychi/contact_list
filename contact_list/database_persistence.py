# this is database class

import os

from contextlib import contextmanager

import logging
import psycopg2
from psycopg2.extras import DictCursor

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class DatabasePersistence:
    def __init__(self):
        self._setup_schema()

    @contextmanager
    def _database_connect(self):
        if os.environ.get('FLASK_ENV') == 'production':
            connection = psycopg2.connect(os.environ['DATABASE_URL'])
        else:
            connection = psycopg2.connect(dbname="contacts")

        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _setup_schema(self):
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_name = 'contacts';
                """)
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        CREATE TABLE contacts(
                            id serial PRIMARY KEY,
                            name text,
                            phone text,
                            email text,
                            category text
                        );
                    """)

    def all_contacts(self):
        query = "SELECT * FROM contacts;"
        logger.info("Executing query: %s", query) 
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

        contacts = [dict(result) for result in results]

        return contacts
    
    def find_contact(self, contact_id):
        query = "SELECT * FROM contacts WHERE id = %s"
        logger.info("Executing query: %s with contact_id: %s", query, contact_id)
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (contact_id,))
                result = cursor.fetchone()

        if result is None:
            return None

        return dict(result)

    def create_new_contact(self, name, phone, email, category):
        query = '''
            INSERT INTO contacts (name, phone, email, category)
            VALUES (%s, %s, %s, %s);
        '''
        logger.info("Executing query: %s with name: %s phone: %s email: %s category: %s", 
                    query, name, phone, email, category) 
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (name, phone, email, category))

    def delete_contact(self, contact_id):
        query = "DELETE FROM contacts WHERE id = %s;"
        logger.info("Executing query: %s with contact_id: %s", query, contact_id) 
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (contact_id,))

    def update_contact(self, contact_id, name, phone, email, category):
        query = '''
            UPDATE contacts
            SET
                name = %s,
                phone  = %s,
                email = %s,
                category = %s
            WHERE id = %s;
        '''
        logger.info("Executing query: %s with contact_id: %s name: %s \
                    phone: %s email: %s category: %s", 
                    query, contact_id, name, phone, email, category) 
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (name, phone, email, category, contact_id))
