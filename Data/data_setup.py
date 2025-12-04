import sys
sys.path.append('/content/drive/MyDrive/Applied Agentic AI/HW5')
import database_setup

from database_setup import DatabaseSetup

# 1. Create DB helper pointing to "support.db"
db = DatabaseSetup("support.db")

# 2. Connect
db.connect()

# 3. Create tables (customers, tickets)
db.create_tables()

# 4. Create triggers (for updated_at)
db.create_triggers()

# 5. Insert sample data (customers + tickets)
db.insert_sample_data()

# 6. (Optional) Show schema + a few records
db.display_schema()
db.run_sample_queries()  # or comment out if too verbose

# 7. Close connection
db.close()

import sqlite3

conn = sqlite3.connect("support.db")
cur = conn.cursor()

cur.execute("SELECT id, name, email, status FROM customers LIMIT 5;")
print(cur.fetchall())

cur.execute("SELECT id, customer_id, issue, status, priority FROM tickets LIMIT 5;")
print(cur.fetchall())

conn.close()
