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
mycursor.execute(f"CREATE DATABASE {database_name}")
mydb.commit()

mycursor.execute("""
                        CREATE TABLE users (
                            user_name VARCHAR(255),
                            user_passwd VARCHAR(255),
                            user_id INT AUTO_INCREMENT PRIMARY KEY,
                            user_role VARCHAR(255), 
                            user_image LONGBLOB
                        )
                    """)
mydb.commit()

mycursor.execute("""
                    CREATE TABLE student (
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
                        user_id  INT foreign key(user_id) references users(user_id),
                        room_id INT,
                    )
                                """)
mydb.commit()

mycursor.execute("""
                    CREATE TABLE room (
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

mycursor.execute("""
                    CREATE TABLE log_rept (
                        Log_id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT foreign key(user_id) references users(user_id),
                        user_Name VARCHAR(255),
                        user_role VARCHAR(255),
                        Login_date DATE,
                        Login_time TIME,
                        logout_time TIME
                    )
                """)
mydb.commit()

mycursor.execute("""
                    CREATE TABLE parent_info (
                        First_name VARCHAR(255),
                        Second_name VARCHAR(255),
                        Phone_number VARCHAR(255),
                        Email_address VARCHAR(255),
                        student_id INT foreign key(student_id) references student(student_id)
                    )
                """)
mydb.commit()

mycursor.execute("""
                    CREATE TABLE complaint (
                        complaint_id INT AUTO_INCREMENT PRIMARY KEY,
                        student_id INT foreign key(student_id) references student(student_id),
                        complaint_massage VARCHAR(500),
                        status VARCHAR(45),
                        )
                """)
mydb.commit()

mycursor.execute("""
                   CREATE TABLE payment (
                       Payment_id INT AUTO_INCREMENT PRIMARY KEY,
                       Student_id INT foreign key(student_id) references student(student_id),
                       Room_id INT,
                       mpesa_transaction_id VARCHAR(255),
                       payment_for VARCHAR(255),
                       Payment_status VARCHAR(255),
                       tansaction_date DATE
                       )
               """)
mydb.commit()

mycursor.execute("""
                   CREATE TABLE visitors_log (
                       visitor_name VARCHAR(255),
                       phone_number INT,
                       visitor_national_id INT,
                       Time_in TIME,
                       time_out TIMEm
                       Date DATE,
                       student_id INT foreign key(student_id) references student(student_id)
                       )
               """)
mydb.commit()

mycursor.execute("""
                  CREATE TABLE admins (
                      admin_id INT AUTO_INCREMENT PRIMARY KEY,
                      full_name VARCHAR(255),
                      phone_no INT,
                      Email VARCHAR(255),
                      user_id INT foreign key(user_id) references users(user_id)
                      )
              """)
mydb.commit()

mycursor.execute("""
                  CREATE TABLE notice_board (
                      notice_id INT AUTO_INCREMENT PRIMARY KEY,
                      notice_message VARCHAR(2000),
                      date DATE,
                      admin_id INT foreign key(admin_id) references admins(admin_id)
                      )
              """)
mydb.commit()

