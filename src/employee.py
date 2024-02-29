# imports
import uuid

def insert_employee(cur, conn, first_name, last_name, email, ssn, phone_number, dob, salary):
    employee_id = str(uuid.uuid4())
    query = """
        INSERT INTO employees (employee_id, employee_first_name, employee_last_name, employee_email, employee_ssn, employee_phone_number, employee_date_of_birth, salary)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cur.execute(query, (employee_id, first_name, last_name, email, ssn, phone_number, dob, salary))
        conn.commit()
        print("New employee added successfully")
    except Exception as e:
        print("An error occurred while adding the new employee: ", e)

def update_employee(cur, conn, employee_first_name, employee_last_name, employee_email, employee_ssn, employee_phone_number, employee_date_of_birth, salary):
    try: 
        cur.execute("""UPDATE employees SET employee_first_name = %s,
                     employee_last_name = %s, employee_ssn = %s, employee_phone_number = %s, 
                     employee_date_of_birth = %s, salary = %s WHERE employee_email = %s""", 
                    (employee_first_name, employee_last_name, employee_ssn, 
                     employee_phone_number,employee_date_of_birth, salary, employee_email))
        conn.commit()
        print("Employee updated successfully!")
    except Exception as e:
        print("An error occurred while updating the employee:", e)

def retrieve_employee_data(cur):
    cur.execute("""SELECT * FROM employees""")
    data = cur.fetchall()
    return data

def delete_employee(cur, conn, employee_id):
    try:
        cur.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
        conn.commit()
        print("Employee's records deleted successfully")
    except Exception as e:
        print("An error occurred while deleting the employee's records", e)    
