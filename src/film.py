# import
import uuid
from flask import flash
from datetime import date
from decimal import Decimal
from re import sub


class Film:
    def __init__(self, uuid, view_at, film_title, ticket_price, dur, direc, rate, image_id):
        self.uuid = uuid
        self.view_at = view_at
        self.film_title = film_title
        self.ticket_price = ticket_price 
        self.dur = dur
        self.direc = direc
        self.rate = rate
        self.image_id = image_id

def insert_films(cur, conn, film_at, film_title, film_price, film_dur, film_dir, film_rate, image_id):
    try:
        film_id = str(uuid.uuid4())
        cur.execute("""INSERT INTO films (film_id, film_at, film_title, film_ticket_price, duration_min, film_director, film_rating, image_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (film_id, film_at, film_title, film_price, film_dur, film_dir, film_rate, image_id))
        conn.commit()
        flash("Film inserted successfully")
    except Exception as e:
        flash("An error occurred while inserting the film", e)

def delete_film(cur, conn, film_title):
    try:
        cur.execute("DELETE FROM films WHERE film_title = %s", (film_title,))
        conn.commit()
        flash("Film deleted successfully")
    except Exception as e:
        flash("An error occurred while deleting the film", e)

def update_film(cur, conn, film_title,  film_at, film_price, film_dur, film_dir, film_rate,):
    try:
        cur.execute("""UPDATE films SET film_at = %s, film_ticket_price = %s, duration_min = %s, film_director = %s, film_rating = %s WHERE film_title = %s""", (film_at, film_price, film_dur, film_dir, film_rate, film_title,))
        conn.commit()
        flash("Film updated successfully!")
    except Exception as e:
        flash("An error occurred while updating the film:", e)


def purchase_film_tickets(cur,conn, event_name,num_tickets, email):

    try:
        # Generate a unique transaction ID
        event_transac_id = str(uuid.uuid4())

        trans_date = date.today()

        # Get the user ID for the given email address
        cur.execute("""SELECT user_id FROM user_account WHERE email = %s""", (email,))
        user_id = cur.fetchone()[0]

        # Get the event ID for the given event name
        cur.execute("""SELECT film_id FROM films WHERE film_title = %s""", (event_name,))
        event_id = cur.fetchone()[0]
        
        # Get the ticket price
        cur.execute("""SELECT film_ticket_price FROM films WHERE film_title = %s""", (event_name,))
        film_price = cur.fetchone()[0]
        price = Decimal(sub(r'[^\d.]', '', film_price))

        print(price)
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

