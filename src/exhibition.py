#import 
from datetime import date
import uuid
from flask import flash
from decimal import Decimal
from re import sub

class Exhibition:
    def __init__(self, uuid, exhib_at, exhib_ticket_price, exhib_gallery, exhib_title, curator, exhib_artists, image_id):
        self.uuid = uuid
        self.exhib_at = exhib_at
        self.exhib_ticket_price = exhib_ticket_price 
        self.exhib_gallery = exhib_gallery
        self.exhib_title = exhib_title
        self.curator = curator
        self.exhib_artists = exhib_artists
        self.image_id = image_id

def insert_exhibition(cur, conn, exhib_at, exhib_price, exhib_gallery, exhib_title, exhib_curator, exhibition_artists, image_id):
    try:
        exhib_id = str(uuid.uuid4())
        cur.execute("""INSERT INTO exhibitions VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *""", 
                    (exhib_id, exhib_at, exhib_price, exhib_gallery, exhib_title, exhib_curator, exhibition_artists, image_id))
        conn.commit()
        flash("Exhibition inserted successfully")
    except Exception as e:
        flash("An error occurred while inserting the exhibition:", e)
        
        # Catch the exception raised by the trigger and print the message to the command line
        if "Trigger function failed" in str(e):
            flash("An exhibition or film has been inserted into the database.")
            flash("Trigger function called successfully")

def update_exhibition(cur, conn, exhib_title, exhib_at, exhib_price, exhib_gallery, exhib_curator, exhibition_artists):
    try:
        cur.execute("""UPDATE exhibitions SET exhib_at = %s, exhib_ticket_price = %s, exhib_gallery = %s, curator = %s, exhib_artists = %s WHERE exhib_title = %s""",
         (exhib_at, exhib_price, exhib_gallery, exhib_curator, exhibition_artists, exhib_title,))
        conn.commit()
        flash("Exhibition updated successfully!")
    except Exception as e:
        flash("An error occurred while updating the exhibition:", e)
   
def delete_exhibit(cur, conn, exhib_title):
    try:
        cur.execute("DELETE FROM exhibitions WHERE exhib_title = %s", (exhib_title,))
        conn.commit()
        flash("Exhibit deleted successfully")
    except Exception as e:
        flash("An error occurred while deleting the exhibit", e)


def purchase_film_tickets(cur,conn, event_name,num_tickets, email):

    try:
        # Generate a unique transaction ID
        event_transac_id = str(uuid.uuid4())

        trans_date = date.today()

        # Get the user ID for the given email address
        cur.execute("""SELECT user_id FROM user_account WHERE email = %s""", (email,))
        user_id = cur.fetchone()[0]
        
        # Get the event ID for the given event name
        cur.execute("""SELECT exhib_id FROM exhibitions WHERE exhib_title = %s""", (event_name,))
        event_id = cur.fetchone()[0]

        # Get the user's ticket price
        cur.execute("""SELECT exhib_ticket_price FROM exhibitions WHERE exhib_title = %s""", (event_name,))
        exhib_price = cur.fetchone()[0]
        price = Decimal(sub(r'[^\d.]', '', exhib_price))
        
        # Get ticket discounter
        cur.execute("""SELECT user_discount FROM user_account WHERE user_id =%s""", (user_id,))
        price_coefficient = cur.fetchone()[0]
        print(price_coefficient)

        # Get ticket sales
        total = Decimal(price_coefficient)*price*Decimal(num_tickets)
        print(total)

        # Insert the ticket transaction into the database
        cur.execute("""INSERT INTO ticket_sales VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (event_transac_id, user_id, trans_date, event_id, event_name, num_tickets, total))
        conn.commit()

        # Print a success message to the command line
        flash("Ticket transaction successful")
    except Exception as e:
        print("An error occurred while inserting the tickets:", e)
