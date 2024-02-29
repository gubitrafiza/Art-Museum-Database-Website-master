# imports
import uuid
import src.helper as hp
# User Class
class User():
    def __init__(self, name, email, password, access='USER'):
        self.name = name
        self.email = email
        self.password = password
        self.access = access
    
    def is_admin(self):
        return self.access == 'ADMIN'

def insert_user(cur, conn, user_fname, user_lname, user_email, user_dob):
    # generate uuid
    user_uuid = str(uuid.uuid4())
    active_account = 1
    membership_lvl = "NONE"
   # insert user into database
    try:
        cur.execute("""INSERT INTO user_account VALUES (%s, %s, %s, %s, %s, %s, %s)""", (user_uuid, user_fname, user_lname, user_email, user_dob, membership_lvl, active_account))
        conn.commit()
        print("user successfully inserted")
    except Exception as e:
        print("There was an error creating the account:", {e})

def insert_user_login(cur, conn, user_name, pw):
    # email is used as username
    try:
        cur.execute("SELECT user_id FROM user_account WHERE email = %s", (user_name,))
        user_uuid = cur.fetchone()
        user_role = "USER"
        hashed = hp.hash_pw(pw)
        hashed = hashed.decode("utf-8")
        cur.execute("INSERT INTO user_login VALUES (%s, %s, %s, %s)", (user_uuid, user_role, user_name, hashed))
        conn.commit()
        print("login successfully inserted")
    except Exception as e:
        conn.rollback()
        print("Error occurred while inserting user login:", e)
        raise

def check_email_exists(cur, conn, email):
    cur.execute("SELECT COUNT(*) FROM user_account WHERE email = %s", (email,))
    count = cur.fetchone()[0]
    return count > 0
