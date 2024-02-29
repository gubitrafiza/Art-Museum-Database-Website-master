# report functions

def insert_gift_rep(cur, g_type, s_date, e_date):
   
    cur.execute("""
    SELECT i.gift_sku, i.gift_type, i.gift_price, DATE(s.gift_transaction_at)
    FROM gift_shop_item as i
    INNER JOIN gift_shop_sales as s 
    ON s.gift_sku = i.gift_sku 
    WHERE i.gift_type = %s AND DATE(s.gift_transaction_at) >= %s AND DATE(s.gift_transaction_at) <= %s """, [g_type, s_date, e_date]
    )
    data = cur.fetchall()

    print(data)

    return data

def gift_get_sum(cur, s_date, e_date ):

    cur.execute("""
    SELECT SUM(gift_price) 
    FROM gift_shop_item as i, gift_shop_sales as s
    WHERE i.gift_sku = s.gift_sku AND DATE(s.gift_transaction_at) >= %s AND DATE(s.gift_transaction_at) <= %s""", (s_date,e_date))

    sum_gift_price = cur.fetchone()[0]

    return sum_gift_price

# 2nd report 
def insert_ticket_rep(cur, s_date,e_date):

    cur.execute("""
        SELECT exhib_title, exhib_ticket_price as ticket_price, DATE(ets.transact_at), ets.num_tickets, ets.total_sale
        FROM exhibitions as e
        INNER JOIN ticket_sales as ets
        ON ets.event_name = e.exhib_title
        WHERE DATE(ets.transact_at) >= %s AND DATE(ets.transact_at) <= %s
        UNION ALL
        SELECT film_title, film_ticket_price, DATE(fts.transact_at), fts.num_tickets, fts.total_sale
        FROM films as f
        INNER JOIN ticket_sales as fts
        ON  fts.event_name = f.film_title
        WHERE DATE(fts.transact_at) >= %s AND DATE(fts.transact_at) <= %s
        """, [s_date, e_date, s_date,e_date]
        )
    
    data = cur.fetchall()

    return data

def get_ticket_sales_sum(cur, s_date, e_date):

    cur.execute("""SELECT SUM(num_tickets)
    FROM ticket_sales as ts
    WHERE DATE(ts.transact_at) >= %s AND DATE(ts.transact_at) <= %s
    """, (s_date, e_date))

    sum_tickets = cur.fetchone()[0]
    
    cur.execute("""SELECT SUM(total_sale)
    FROM ticket_sales as ts
    WHERE DATE(ts.transact_at) >= %s AND DATE(ts.transact_at) <= %s""", (s_date, e_date))

    sum_price = cur.fetchone()[0]
    
    # returns tuple of both data
    return (sum_tickets, sum_price)

# 3rd report
def insert_don_rep(cur, s_date, e_date):

    cur.execute("""SELECT u.first_name, u.last_name, 
    d.donator_email, d.donation_amount, u.membership, d.donation_on
    FROM donation as d
    INNER JOIN user_account as u
    ON d.donator_email = u.email
    WHERE d.donation_on >= %s AND d.donation_on <= %s
    GROUP BY u.first_name, u.last_name, d.donator_email, d.donation_amount, u.membership, d.donation_on
    """, (s_date,e_date))

    data = cur.fetchall()

    return data 

def retrieve_donation_sum(cur, s_date, e_date):

    cur.execute("""SELECT SUM(donation_amount)
    FROM donation as d
    WHERE d.donation_on >= %s AND d.donation_on <= %s
    """, (s_date, e_date))

    data = cur.fetchone()
    
    return data