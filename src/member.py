from flask import Flask, request, render_template, make_response, redirect, url_for, session, flash, app

def retrieve_member_data(cur):
    cur.execute("""SELECT * FROM user_account""")
    data = cur.fetchall()
    return data    

def retrieve_member(cur, email):
    cur.execute("""SELECT user_discount FROM user_account WHERE email =%s""", (email,))
    data = cur.fetchone()[0]
    return data   

def update_member(cur, conn, email, membership_type):
    try:
        cur.execute("SELECT * FROM user_account WHERE email = %s", (email,))
        user = cur.fetchone()
        if user is None:
            message = "Account with that email does not exist"
            flash(message, 'danger')
            return redirect(url_for('members'))
        cur.execute("UPDATE user_account SET membership = %s WHERE email = %s", 
            (membership_type, email))
        conn.commit()
        discount = ""
        if membership_type == 'BASIC':
            amount_charged = 20
            discount = 10

        elif membership_type == 'SILVER':
            amount_charged = 30
            discount = 20

        elif membership_type == 'GOLD':
            amount_charged = 40
            discount = 30

        message = f"The following amount has been charged to your account: ${amount_charged}. You now have a {discount}% discount on exhibit/film purchases."
        
        flash(message, 'success')
        return redirect(url_for('members'))
        
    except Exception as e:
        print("An error occurred while updating the user account: ", e)
        message = "An error occurred while updating the user account"
        flash(message, 'danger')
        return redirect(url_for('members'))



def delete_member(cur, conn, email):
    try:
        cur.execute("UPDATE user_account SET account_status = %s WHERE email = %s", 
            (0, email))
        conn.commit()
        print("User account deleted successfully")
    except Exception as e:
        print("An error occurred while deleting the user account: ", e)
