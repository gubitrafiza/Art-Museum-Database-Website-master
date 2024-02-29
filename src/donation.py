# imports
import uuid
from datetime import date

def insert_donation(cur, conn, email_address, money_amount):
    try:
        transac_id = str(uuid.uuid4())
        donation_date = date.today()
        cur.execute("INSERT INTO donation (donation_transaction_id, donator_email, donation_on, donation_amount) VALUES (%s, %s, %s, %s)", 
        (transac_id, email_address, donation_date, money_amount))
        conn.commit()
        print("Donation added successfully")
    except Exception as e:
        print(f"Error inserting donation: {e}")
