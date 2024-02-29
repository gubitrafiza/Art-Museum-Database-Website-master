class Artwork:
    def __init__(self, obj_num, artist, title, year, type, image_id):
        self.obj_num = obj_num
        self.artist = artist
        self.title = title
        self.year = year
        self.type = type
        self.image_id = image_id

def insert_art(cur, conn, obj_num, artist, title, made_on, obj_type, img_uuid):
    sql_query = """INSERT INTO artworks VALUES (%s, %s, %s, %s, %s, %s)"""
    values = (obj_num, artist,title, made_on, obj_type, img_uuid)
    try:
        cur.execute(sql_query, values)
        print("Art values inserted successfully!")
         # very important to commit sql transactions
        conn.commit()
    except Exception as e:
        print(f"Error inserting values into artworks table: {e}")
 
def delete_artwork(cur, conn, obj_num):
    try:
        cur.execute("DELETE FROM artworks WHERE obj_num = ?", (obj_num,))
        conn.commit()
    except Exception as e:
        print("An error occurred while deleting the artwork", e)

def update_art(cur, conn, artist, title, made_on, obj_type, obj_num, art_byte, art_id):
    sql_query = """UPDATE artworks SET artist = %s, title = %s, made_on = %s, obj_type = %s, obj_num = %s, art_byte = %s WHERE id = %s"""
    values = (artist, title, made_on, obj_type, obj_num, art_byte, art_id)
    try:
        cur.execute(sql_query, values)
        conn.commit()
        print("Art values updated successfully!")
      
    except Exception as e:
        print(f"Error updating values in artworks table: {e}")
