host_name = "localhost"
user_name = "root"
password_key = "12hezron12"
database_name = "hostel"

import mysql.connector


mydb = mysql.connector.connect(
    host=host_name,
    user=user_name,
    password=password_key
)

# Create the database
mycursor = mydb.cursor()
try:
    mycursor.execute(f"CREATE DATABASE {database_name}")
    mydb.commit()
except:
    mycursor.execute(f"DROP DATABASE IF EXISTS {database_name}")
    mydb.commit()
    mycursor.execute(f"CREATE DATABASE {database_name}")
    mydb.commit()



mycursor.execute(f"""
                        CREATE TABLE {database_name}.users (
                            user_name VARCHAR(255),
                            user_passwd VARCHAR(255),
                            user_id INT AUTO_INCREMENT PRIMARY KEY,
                            user_role VARCHAR(255), 
                            user_image LONGBLOB
                        )
                    """)
mydb.commit()
mycursor.execute(f"INSERT INTO {database_name}.users (user_name, user_passwd, user_id, user_role) VALUES (%s, %s, %s, %s);", ("admin", "admin", 2353, "admin"))
mydb.commit()


mycursor.execute(f"""
                  CREATE TABLE {database_name}.admins (
                      admin_id INT AUTO_INCREMENT PRIMARY KEY,
                      full_name VARCHAR(255),
                      phone_no INT,
                      Email VARCHAR(255),
                      user_id INT,
                      FOREIGN KEY (user_id) REFERENCES users(user_id)
                      )
              """)
mydb.commit()
mycursor.execute(f"INSERT INTO {database_name}.admins (full_name, user_id) VALUES (%s, %s);", ("Super User", 2353))
mydb.commit()



mycursor.execute(f"""
                    CREATE TABLE {database_name}.student (
                        student_id INT AUTO_INCREMENT PRIMARY KEY,
                        first_name VARCHAR(255),
                        second_name VARCHAR(255),
                        lasrt_name VARCHAR(255),
                        date_of_birth DATE,
                        gender VARCHAR(255),
                        phone_no VARCHAR(255),
                        email_id VARCHAR(255),
                        year_of_study INT,
                        institution VARCHAR(255),
                        national_id VARCHAR(255),
                        user_id  INT,
                        room_id INT,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )
                                """)
mydb.commit()

mycursor.execute(f"""
                    CREATE TABLE {database_name}.room (
                        room_id INT AUTO_INCREMENT PRIMARY KEY,
                        room_type VARCHAR(255),
                        room_number INT,                                                    
                        room_price INT,
                        room_status VARCHAR(255),
                        room_condition VARCHAR(255),
                        total_beds VARCHAR(255),
                        room_amenities VARCHAR(255),
                        gender_room_type LONGTEXT
                    )
                """)
mydb.commit()

mycursor.execute(f"""
                    CREATE TABLE {database_name}.log_rept (
                        Log_id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        user_Name VARCHAR(255),
                        user_role VARCHAR(255),
                        Login_date DATE,
                        Login_time TIME,
                        logout_time TIME,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )
                """)
mydb.commit()

mycursor.execute(f"""
                    CREATE TABLE {database_name}.parent_info (
                        First_name VARCHAR(255),
                        Second_name VARCHAR(255),
                        Phone_number VARCHAR(255),
                        Email_address VARCHAR(255),
                        student_id INT,
                        FOREIGN KEY (student_id) REFERENCES student(student_id)
                    )
                """)
mydb.commit()

mycursor.execute(f"""
                    CREATE TABLE {database_name}.complaint (
                        complaint_id INT AUTO_INCREMENT PRIMARY KEY,
                        student_id INT,
                        complaint_massage VARCHAR(500),
                        status VARCHAR(45),
                        FOREIGN KEY (student_id) REFERENCES student(student_id)
                        )
                """)
mydb.commit()

mycursor.execute(f"""
                   CREATE TABLE {database_name}.payment (
                       Payment_id INT AUTO_INCREMENT PRIMARY KEY,
                       Student_id INT,
                       Room_id INT,
                       mpesa_transaction_id VARCHAR(255),
                       payment_for VARCHAR(255),
                       Payment_status VARCHAR(255),
                       tansaction_date DATE,
                       FOREIGN KEY (Student_id) REFERENCES student(student_id)
                     
                       )
               """)
mydb.commit()

mycursor.execute(f"""
                   CREATE TABLE {database_name}.visitors_log (
                       visitor_name VARCHAR(255),
                       phone_number INT,
                       visitor_national_id INT,
                       Time_in TIME,
                       time_out TIME,
                       Date DATE,
                       student_id INT,
                       FOREIGN KEY (student_id) REFERENCES student(student_id)
                       )
               """)
mydb.commit()


mycursor.execute(f"""
                  CREATE TABLE {database_name}.notice_board (
                      notice_id INT AUTO_INCREMENT PRIMARY KEY,
                      notice_message VARCHAR(2000),
                      date DATE,
                      admin_id INT,
                      Foreign key (admin_id) REFERENCES admins(admin_id)
                      )
              """)
mydb.commit()

