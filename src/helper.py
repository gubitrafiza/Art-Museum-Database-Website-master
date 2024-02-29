import bcrypt
import PIL.Image as Image
from io import BytesIO
import uuid

def hash_pw(password):
    # encoding user password
    bytes = password.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    print(hash)
    # print(result)
    return hash

def isValidPw(in_password,hash):
    db_pw_byte = hash[0].encode('utf-8')
   # print(hash[0], " pw")
    userBytes = in_password.encode('utf-8')
    # checking password (boolean)
    result = bcrypt.checkpw(userBytes, db_pw_byte)
    print("passed!")
    return result

# Testing Hash Functions
# print("first admin: ",hash_pw("admin"), isValidPw("admin", hash_pw("admin")))
# print("first user: ", hash_pw("user"))
# print("second user pw: ",hash_pw("user1"))
# print("third user pw: ", hash_pw("user2"))

def insert_image(cur, con, img_file):
    # open image
    pil_im = Image.open(img_file)
    # crop image
    # border = (20, 20, 100, 100)
    # cropped = pil_im.crop(border)
    # save new image to bytes in memory
    b = BytesIO()
    pil_im.save(b, 'jpeg')

    # generate new ID
    img_uuid = str(uuid.uuid4())
    try:
        cur.execute("""INSERT INTO images VALUES (%s, %s)""",  (img_uuid, b.getvalue()))
        print("Inserted into images succesfully!")
        con.commit()
    except Exception as e:
        print(f"Error inserting values into images table: {e}")

    return img_uuid