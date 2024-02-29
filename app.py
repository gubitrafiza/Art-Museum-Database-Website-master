from flask import Flask, request, render_template, make_response, redirect, url_for, session, flash, app
app = Flask(__name__)
app.secret_key = 'my_secret'
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# modules
import src.helper as hp
import src.art as art
import src.donation as don
import src.employee as emp
import src.exhibition as exhib
import src.film as film
import src.gift as gift
import src.member as mem
import src.report as rep
import src.user as user

# Local Connection
try:
    with open("config.toml") as tomlfile:
        content = tomlfile.read()
    conn = psycopg2.connect(content)
    cur = conn.cursor()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    print("Connected to Postgres")
except Exception as e:
    print("An error occurred while connecting: ", e)

@app.route("/")
def index():
    return render_template("login.html") 

@app.route('/home', methods = ['POST', 'GET'])
def home():
    if request.method == 'GET':
        user = session["user-role"]
        # this is just to guide users to the notification tab
        e_req = request.cookies.get('e_title') 
        f_req = request.cookies.get('f_title')
        if e_req:
            flash(f"A new event, {e_req}, has been added!")
        if f_req:
            flash(f"A new event, {f_req}, has been added!")
    return render_template("home.html", user=user)

@app.get('/notification')
def notification():
    user = session["user-role"]
    cur.execute("""SELECT * FROM notifs""")
    data = cur.fetchall()
    if data == []:
        msg = "You have no notifications at this time."
        return render_template('notification.html', msg=msg)
    return render_template("notification.html", data=data)

@app.route('/registration', methods=['POST','GET'])
def registration():
    if request.method == 'POST':
        fname = request.form['user_fname']
        lname = request.form['user_lname']
        email = request.form['user_email']
        birthdate = request.form['bdate']
        
        # Check if email is already in use
        if user.check_email_exists(cur, conn, email):
            flash("That email is already in use.")
        else:
            # Insert new user and login details
            user.insert_user(cur, conn, fname, lname, email, birthdate)
            password = request.form['user_password']
            user.insert_user_login(cur, conn, email, password)
            flash("Registration successful!")
            
    return render_template('registration.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['user_email']
        in_password = request.form['user_password']
        valid_password = ""
        try:
            cur.execute("""SELECT hashed_password FROM user_login WHERE user_name = %s""", (email,))
            db_password = cur.fetchone()
        except psycopg2.Error as e:
            print("error", e)        

        valid_password = hp.isValidPw(in_password, db_password)
        # print(valid_password)
        if valid_password:
            cur.execute("""SELECT * FROM user_login WHERE user_name = %s""", (email,))
            account = cur.fetchone()
            if account:
                account_id = account[0]
                cur.execute("""SELECT account_status FROM user_account WHERE user_id = %s""", (account_id,))
                account_status_value = cur.fetchone()[0]
                if account_status_value == '1':
                    cur.execute("""SELECT first_name FROM user_account as ua, user_login as ul WHERE ua.user_id = ul.user_id AND user_name=%s""",
                                (email,))
                    name = cur.fetchone()
                    cur.execute("""SELECT user_role FROM user_login WHERE user_name=%s""", (email,))
                    db_role = cur.fetchone()
                    print("role is ", db_role[0])

                    usr = user.User(name, email, in_password, db_role[0])
                    session['user-role'] = usr.access
                    return redirect(url_for('home'))
                else:
                    # account_status is not 1, don't render home.html
                    flash("Account status is not active")
                    return render_template('login.html')
            else:
                # account doesn't exist, don't render home.html
                flash("Account doesn't exist")
                return render_template('login.html')
    return render_template('login.html')

@app.route('/logout', methods=['POST','GET'])
def logout():
    session.clear()
    return render_template('login.html')

@app.get('/artworks')
def artworks():
        user = session["user-role"]
        cur.execute("""SELECT * FROM artworks""")
        rows = cur.fetchall()
        artworks = []
        for row in rows:
            art_obj = art.Artwork(row[0], row[1], row[2], row[3], row[4], row[5])
            artworks.append(art_obj)
        return render_template('artworks.html', user=user, artworks=artworks)

@app.get('/image/<id>')
def get_image(id):
    cur.execute("""SELECT bytes FROM images WHERE image_id = %s """, (id,))
    row = cur.fetchone()
    # convert memview to bytes
    image_binary = bytes(row[0])
    # print(image_binary)
    response = make_response(image_binary)
    # send custom header
    response.mimetype = "image/jpeg"
    return response

@app.route('/add_new_artwork', methods=['POST','GET'])
def add_new_artwork():
    if request.method == 'POST':
        obj_num = request.form['object_number']
        artist = request.form['artist']
        title = request.form['artwork_title']
        made_on = request.form['made_on']
        obj_type = request.form['object_type']
        img_file = request.files['art_img']

        img_uuid = hp.insert_image(cur, conn, img_file)
        art.insert_art(cur, conn, obj_num, artist,title,made_on,obj_type, img_uuid)
    return render_template('add_new_artwork.html')
  
@app.route('/update_artwork', methods=['POST','GET'])
def update_artwork():
    if request.method == 'POST':
        obj_num = request.form['object_number']
        artist = request.form['artist']
        title = request.form['artwork_title']
        made_on = request.form['made_on']
        obj_type = request.form['object_type']
        img_file = request.files['art_img']
        img_uuid = hp.insert_image(cur, conn, img_file)
        art.insert_art(cur, conn, obj_num, artist,title,made_on,obj_type, img_uuid)
    return render_template('add_new_artwork.html')
    
@app.route('/add_new_donation', methods = ['GET', 'POST'])
def add_new_donation():
    if request.method == 'POST':
        email_address = request.form['email']
        money_amount = request.form['donation_amount']
        don.insert_donation(cur, conn, email_address, money_amount)
        flash("Thank you for your donation!")
        return render_template('donations.html')
    else:
        return render_template('donations.html')
    
@app.get('/exhibitions')
def exhibitions():
    user = session["user-role"]
    cur.execute("""SELECT * FROM exhibitions""")
    rows = cur.fetchall()
    exhibs = []
    for row in rows:
            exhib_obj = exhib.Exhibition(row[0],row[1],row[2],
                                         row[3],row[4],row[5],
                                         row[6],row[7])
            exhibs.append(exhib_obj)
    return render_template('exhibitions.html',user=user, exhibs=exhibs)

@app.route('/add_new_exhibition', methods = ['GET', 'POST'])
def add_new_exhibition():
    if request.method == 'POST':
       
        date_and_time = request.form['exhibition_at']
        ticket_price = request.form['exhibition_ticket_price']
        gallery = request.form['exhibition_gallery']
        title = request.form['exhibition_title']
        curator = request.form['curator']
        artists = request.form['exhibition_artists']
        img_file = request.files['exhib_img']

        img_uuid = hp.insert_image(cur,conn, img_file)
        exhib.insert_exhibition(cur, conn, date_and_time,
                                 ticket_price,gallery, title, 
                                 curator, artists, img_uuid)
        
        resp = make_response(render_template('add_new_exhibition.html'))
        resp.set_cookie('e_title', title, max_age=80)
        return resp
    else:
        return render_template('add_new_exhibition.html')


@app.route('/update_exhibition', methods = ['POST'])
def update_exhibition():
    if request.method == 'POST':
        title = request.form['exhibition_title']
        date_and_time = request.form['exhibition_at']
        ticket_price = request.form['exhibition_ticket_price']
        gallery = request.form['exhibition_gallery']
        curator = request.form['curator']
        artists = request.form['exhibition_artists']
        try:
            exhib.update_exhibition(cur, conn, title, date_and_time, ticket_price,
        gallery, curator, artists)
            flash('Exhibition updated successfully.')
        except Exception as e:
            print(f"Error updating exhibition: {e}")
            flash('Error updating exhibition.')
    return render_template('add_new_exhibition.html')
   

@app.route('/delete_exhibition', methods = ['POST'])
def delete_exhibition():
    if request.method == 'POST':
        title = request.form['exhibition_title']
        try:
            exhib.delete_exhibit(cur, conn, title)
        except Exception as e:
            print(f"Error deleting exhibition: {e}")
            flash('Error deleting exhibition.')
        return render_template('add_new_exhibition.html')

@app.get('/films')
def films():
    user = session["user-role"]
    cur.execute("""SELECT * FROM films""")
    rows = cur.fetchall()
    films = []
    for row in rows:
        film_obj = film.Film(row[0],row[1],row[2],
                             row[3],row[4],row[5],
                             row[6],row[7])
        films.append(film_obj)
    return render_template('films.html',user=user, films=films)

@app.route('/add_new_film', methods=['GET', 'POST'])
def add_new_film():
    if request.method == 'POST':

        location = request.form['viewing_at']
        title = request.form['film_title']
        ticket_price = request.form['film_ticket_price']
        duration = request.form['duration_min']
        director = request.form['film_director']
        rating = request.form['film_rating']
        img_file = request.files['film_img']

        img_uuid = hp.insert_image(cur,conn,img_file)
        film.insert_films(cur, conn, location,
        title, ticket_price, duration, director,
        rating, img_uuid)

        resp = make_response(render_template('add_new_film.html'))
        resp.set_cookie('f_title', title, max_age=80)
        return resp
    else:
        return render_template('add_new_film.html')
   

@app.route('/update_film', methods = ['POST'])
def update_film():
    if request.method == 'POST':
        title = request.form['film_title']
        location = request.form['viewing_at']
        ticket_price = request.form['film_ticket_price']
        duration = request.form['duration_min']
        director = request.form['film_director']
        rating = request.form['film_rating']

        film.update_film(cur, conn, title, location,
        ticket_price, duration, director,
        rating)
    return render_template('add_new_film.html')
   


@app.route('/delete_film', methods = ['POST'])
def delete_film():
    title = request.form['film_title']
    try:
        film.delete_film(cur, conn, title)
        flash('Film deleted successfully')
    except Exception as e:
        print (f"Error deleting film: {e}")
        flash('Error deleting film.')
    return render_template('add_new_film.html') 

@app.route('/add_new_employee', methods=['GET', 'POST'])
def add_new_employee():
    if request.method == 'POST':
        first_name = request.form['employee_first_name']
        last_name = request.form['employee_last_name']       
        email = request.form['employee_email']
        ssn = request.form['employee_ssn']
        phone_number = request.form['employee_phone_number']
        dob = request.form['employee_date_of_birth']
        salary = request.form['salary']
        emp.insert_employee(cur, conn, first_name,
        last_name, email, ssn, phone_number,
        dob, salary)
        flash("New Employee's Records has been added.")
    return render_template('add_new_employee.html')
    
@app.route('/update_employee', methods = ['POST'])
def update_employee():
    if request.method == 'POST':
        first_name = request.form['employee_first_name']
        last_name = request.form['employee_last_name']
        email = request.form['employee_email']
        ssn = request.form['employee_ssn']
        phone_number = request.form['employee_phone_number']
        dob = request.form['employee_date_of_birth']
        salary = request.form['salary']
        emp.update_employee(cur, conn, first_name,
        last_name, email, ssn, phone_number,
        dob, salary)
        flash("Employee's Records have been updated.")
    return render_template('add_new_employee.html')
   

@app.route('/delete_employee', methods = ['POST'])
def delete_employee():
    if request.method == 'POST':
        id_num = request.form['emp_id']
        emp.delete_employee(cur, conn, id_num)
    return render_template('add_new_employee.html')
   

@app.get('/add_new_member')
def add_new_member():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address_line1 = request.form['address_line1']
        address_line2 = request.form['address_line2']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip']
        email = request.form['email']
        phone_number = request.form['phone_number']
        gender = request.form['gender']
        dob = request.form['dob']
        membership_type = request.form['membership']
        mem.insert_member(cur, conn, first_name, last_name,
        address_line1, address_line2, city, state,
        zip_code, email, phone_number, gender, dob, membership_type)
    return render_template('add_new_member.html')
    

@app.route('/update_member', methods = ['POST'])
def update_member():
    if request.method == 'POST':
        email = request.form['email']
        membership_type = request.form['membership']
        mem.update_member(cur, conn, email, membership_type)
    return render_template('members.html')
    

@app.route('/delete_member', methods = ['POST'])
def delete_member():        
    if request.method == 'POST':
        member_id = request.form['email']
        try:
            mem.delete_member(cur, conn, member_id)
            flash('User account deleted successfully')
        except Exception as e:
            print(f"Error deleting user account: {e}")
            flash('Error deleting user account.')
    return render_template('add_new_member.html')

@app.route('/gift_shop', methods=['GET', 'POST'])
def gift_shop():
    user = session["user-role"]
    msg = ""
    data = gift.retrieve_gift_shop_data(cur)
    giftshop = []
    for row in data:
        gift_obj = gift.Giftshop(row[0],row[1],row[2],
                                 row[3],row[4])
        giftshop.append(gift_obj)
    if request.method == 'POST':
        gift_name = request.form['item_name']
        email = request.form['email']
        try:
            gift.insert_gift_sales(cur, conn, gift_name, email)
            flash('Gift item purchased successfully')
        except Exception as e:
            flash('Error purchasing item.')
    if data == []:
        msg = "No Gift Shop Inventory Data Available"
        return render_template('gift_shop.html', msg=msg)
    else:
        app.logger.info(data)
        return render_template('gift_shop.html', giftshop=giftshop, user=user)

@app.route('/add_new_gift_shop_item', methods=['GET', 'POST'])
def add_new_gift_shop_item():
    if request.method == 'POST':
        name = request.form['name']
        item_type = request.form['type']
        price = request.form['price']
        img_file = request.files['gift_img']

        img_uuid = hp.insert_image(cur, conn, img_file)

        try:
            gift.insert_gift_item(cur, conn, name, item_type, price, img_uuid)
            flash('Gift item added successfully.')
        except Exception as e:
            print(f"Error adding gift item: {e}")
            flash('Error adding gift item.')
    return render_template('add_new_gift_shop_item.html')

@app.route('/update_gift_shop_item', methods=['POST'])
def update_gift_shop_item():
    gift_name = request.form['name']
    gift_type = request.form['type']
    gift_price = request.form['price']
    try:
        gift.update_gift_item(cur, conn, gift_name, gift_type, gift_price)
        flash('Gift item updated successfully.')
    except Exception as e:
        print (f"Error updating gift item: {e}")
        flash('Error updating gift item.')
    return render_template('add_new_gift_shop_item.html')


@app.route('/delete_gift_shop_item', methods=['POST'])
def delete_gift_shop_item():
    gift_name = request.form['name']
    try:
        gift.delete_gift_shop_item(cur, conn, gift_name)
        flash('Gift item deleted successfully')
    except Exception as e:
        print (f"Error deleting gift item: {e}")
        flash('Error deleting gift item.')
    return render_template('add_new_gift_shop_item.html')  




@app.get('/members')
def members():
    user = session["user-role"]
    msg = ""
    data = mem.retrieve_member_data(cur)
    if data == []:
        msg = "No Member Data Available"
        app.logger.info(data)
        return render_template('members.html', msg=msg)
    else:
        app.logger.info(data)
        return render_template('members.html', data=data)

@app.get('/employees')
def employees():
    user = session["user-role"]
    msg = ""
    data = emp.retrieve_employee_data(cur)
    if data == []:
        msg = "No Employee Data Available"
        app.logger.info(data)
        return render_template('employees.html', msg=msg)
    else:
        app.logger.info(data)
        return render_template('employees.html', data=data)

@app.route('/Fticket_details', methods = ['GET', 'POST'])
def Fticket_details():
    user = session["user-role"]
    if not user:
        return render_template('login')
    cur.execute("""SELECT * FROM films""")
    rows = cur.fetchall()
    film_title = []
    for row in rows:
        film_title.append(row[2])
  
    if request.method == 'POST':
        selection = request.form['film_name']
        num_tickets = request.form['total_adults']
        user_email = request.form['visitor_email']
        print(f"{selection} and {num_tickets} and {user_email}")
        try:
            film.purchase_film_tickets(cur, conn, selection, num_tickets, user_email)
            print('Film tickets booked successfully!')
            user_discount = mem.retrieve_member(cur, user_email)
            if user_discount != 1.0:
                flash("Successfully purchased with membership discount.")
            else:
                flash("Film tickets booked successfully!")
            print(film_title)
           
        except Exception as e:
            print(f"Error booking film tickets: {e}")
            flash('Failed to book film tickets. Please try again later')

    return render_template('Fticket_details.html', user=user, film_title=film_title)

@app.route('/Eticket_details', methods = ['GET', 'POST'])
def Eticket_details():
    user = session["user-role"]
    if not user:
        return render_template('login')
    cur.execute("""SELECT * FROM exhibitions""")
    rows = cur.fetchall()
    exhib_title = []
    for row in rows:
        exhib_title.append(row[4])
    if request.method == 'POST':
        selection = request.form['exh_name']
        num_tickets = request.form['total_adults']
        user_email = request.form['visitor_email']
        print(f"{selection} and {num_tickets} and {user_email}")
        try:
            exhib.purchase_film_tickets(cur, conn, selection, num_tickets, user_email)
            print('Exhibition tickets booked successfully!')
            print(exhib_title)
            user_discount = mem.retrieve_member(cur, user_email)
            print(user_discount)
            if user_discount != 1.0:
                flash("Successfully purchased with membership discount.")
            else:
                flash("Exhibit tickets booked successfully!")
        except Exception as e:
            print(f"Error booking Exhibition tickets: {e}")
            msg = 'Failed to book Exhibition tickets. Please try again later'
            return render_template('Eticket_details.html', msg=msg)

    return render_template('Eticket_details.html', user=user, exhib_title=exhib_title)



@app.route('/user_info')
def user_info():
    f_name = request.form['user_fname']
    l_name = request.form['user_lname']
    # address area
    line_1 = request.form['line_1']
    city = request.form['city']
    state = request.form['state']
    phone_number = request.form['phone_number']
    sex = request.form['sex']
    dob = request.form['dob']
    user.insert_user(cur,f_name,l_name,(line_1,city,state), phone_number,sex, dob, 'NONE')


# the reports

@app.get('/report_gifts')
def report_gifts():
    mgs = ""
    data = []
    gift_type = request.args.get('gift-type')
    start_date = request.args.get('start-date')
    end_date = request.args.get('end-date')

    ticket_data = rep.insert_gift_rep(cur, gift_type, start_date, end_date)
    ticket_sum = rep.gift_get_sum(cur, start_date,end_date)
    print(ticket_data)
    print(ticket_sum)
    if ticket_data == []:
        msg = "There was no report for the selected interval. Please try another set of dates!"
        return render_template('report_gifts.html', msg=msg)
       
    else:
        data.append(ticket_data)
        data.append(ticket_sum)
        return render_template('report_gifts.html',data=data, user=user)
            
@app.get('/report_tickets')
def report_tickets():
    user = session["user-role"]
    data = []
    msg = ""
    start_date = request.args.get('start-date')
    end_date = request.args.get('end-date')
  
    ticket_rep = rep.insert_ticket_rep(cur, start_date, end_date)
    sales_sum = rep.get_ticket_sales_sum(cur, start_date, end_date)
    if ticket_rep == []:
        msg = "There was no report for the selected interval. Please try another set of dates!"
        app.logger.info(ticket_rep)
        app.logger.info(sales_sum[0])
        
        return render_template('report_tickets.html', msg=msg)
        
    else:
        data.append(ticket_rep)
        data.append(sales_sum[0])
        data.append(sales_sum[1])

        return render_template('report_tickets.html', user=user, data=data)


@app.get('/donations')
def donations():
    user = session["user-role"]
    msg = ""
    data = []
    start_date = request.args.get('start-date')
    end_date = request.args.get('end-date')
    donation_data = rep.insert_don_rep(cur, start_date, end_date)
    donation_sum = rep.retrieve_donation_sum(cur, start_date, end_date)

    if donation_data == []:
        msg = "No Donation Data Available"
        app.logger.info(data)
        return render_template('donations.html', msg=msg)
    else:
        data.append(donation_data)
        data.append(donation_sum[0])

        print("this is the don. sum: ", data[0])
        return render_template('donations.html', data=data,user=user)

# end of reports