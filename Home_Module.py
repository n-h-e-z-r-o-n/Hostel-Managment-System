import tkinter as tk  # import the tkinter module as tk to the program
from tkinter import Menu
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # for image processing
import json
import threading
# ---------------------- creating a connection to the database.---------------------------------------------------------
import mysql.connector

# Connection parameters
host = "your_host"
user = "your_username"
password = "your_password"
database = "hostel"

# Connection parameters

host_name = "localhost"
user_name = "root"
password_key = "12hezron12"
database_name = "hostel"
try:
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password_key,
        database=database_name
    )
    mycursor = mydb.cursor()
except mysql.connector.Error as err:
    print(f"Error connecting to the database: {err}")
    if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
        print(f"Database '{database_name}' does not exist. Creating it...")
        try:
            # Connect to MySQL server without selecting any database
            mydb = mysql.connector.connect(
                host=host_name,
                user=user_name,
                password=password_key
            )

            # Create the database
            mycursor = mydb.cursor()
            mycursor.execute(f"CREATE DATABASE {database_name}")

            print(f"Database '{database_name}' created successfully!")
        except:
            print(f"Error creating database")
            exit(1)

# -----------------------------------------------------------------------------------------------------------------------



# --------------------functions--------------------

def resize(file_location):
    img = (Image.open(file_location))
    Resized_image = img.resize((screen_width, screen_height), Image.LANCZOS)
    new_image = ImageTk.PhotoImage(Resized_image)
    return new_image





def show_frame(frame):
    frame.tkraise()


def close_win():  # Define a function to close the window
    root.destroy()


def changeOnHover(button, colorOnHover, colorOnLeave):  # function to change properties of button on hover
    button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover))
    button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))


def Homepage_Background(widget):
    global x
    image1 = resize("./Assets/images/home_page_background1.jpg")
    image2 = resize("./Assets/images/home_page_background2.jpg")
    image3 = resize("./Assets/images/home_page_background3.jpg")
    image4 = resize("./Assets/images/home_page_background4.jpg")
    image5 = resize("./Assets/images/home_page_background5.jpg")
    x = 1
    def Home_page_Background_changer(widget=widget):
        global x
        while True:
            if x == 1:
                widget.config(image=image1)
                x = 2
            elif x == 2:
                widget.config(image=image2)
                x = 3
            elif x == 3:
                widget.config(image=image3)
                x = 4
            elif x == 4:
                widget.config(image=image4)
                x = 5
            elif x == 5:
                widget.config(image=image4)
                x = 1
            braek

    Home_page_Background_changer()





# -------------------------- Main Window ________________________________________________________________________________
root = tk.Tk()  # create an instance of the tk.Tk class
root.title('school project')  # setting window title
root.geometry('1000x600+50+50')  # setting window size and location
root.state('zoomed')  # open the window in its full size
root.minsize(1000, 800)  # setting the minimum size of the root window
root.rowconfigure(0, weight=1)  # make our frames expand along with the main window
root.columnconfigure(0, weight=1)  # make our frame expand along with the window

root.iconbitmap('./imag/Profile.ico')  # setting windows icon

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# -------------------- frames(System Pages) ----------------


Home_Page = tk.Frame(root, bg='yellow')
Home_Page.place(relheight=1,relwidth=1, rely=0, relx=0)

image5 = resize("./Assets/images/home_page_background5.jpg")
label_image = tk.Label(Home_Page, image=image5, border=0, justify='center')
label_image.place(x=0, y=0, relheight=1, relwidth=1)
Homepage_Background(label_image)





# ======================== Login page frame code =======================================================================

login_Page_frame = tk.Frame(Home_Page, bg='#4B3621', height=500, width=400)
login_Page_frame.place(relx=0.01, rely=0.1)


# store username  and password variables

def Login_function(username, password):
    if password == '' and username == '':
        stut1 = tk.Label(Home_Page, text='✗ Error:\n\n User name or Password is Empty/blank', bg='#BA0021', fg='black', font='-family {Georgia}  -size 10 -weight bold')
        stut1.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
        stut1.after(4100, lambda: stut1.place_forget())
        return
    else:
        mycursor.execute("select * from hostel.users where user_name=%s and user_passwd=%s", (username, password))
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            stut1 = tk.Label(Home_Page, text='✗ LOGIN ERROR:\n\n Invalid Username or Password', bg='#FF0000', fg='black', font='-family {Georgia}  -size 10 -weight bold')
            stut1.place(relx=0.6, rely=0.05, relwidth=0.25, relheight=0.09)
            stut1.after(4100, lambda: stut1.place_forget())
            return
        else:
            user_id = myresult[0][2]

            if myresult[0][3] == 'student':
                mycursor.execute("SELECT * FROM hostel.student WHERE user_id = %s;", [user_id])
                fetg = mycursor.fetchall()
                mycursor.execute("INSERT INTO hostel.log_rept (user_id, user_Name, user_role, Login_date, Login_time) VALUES (%s, %s, %s, CURDATE(), CURTIME());", (myresult[0][2], f'{fetg[0][1]} {fetg[0][2]} {fetg[0][2]}', myresult[0][3]))
                mydb.commit()
                mycursor.execute("SELECT * FROM hostel.log_rept;")
                log_id_f = mycursor.fetchall()
                i = len(log_id_f) - 1
                curent_log_id = log_id_f[i][0]

                dic = {'session_id': user_id, 'log_id': curent_log_id}
                json_object = json.dumps(dic, indent=4)
                print(json_object)
                with open("SessionInfo.json", "w") as outfile:
                    outfile.write(json_object)

                import subprocess
                cmd = 'python StudentPage.py'
                p = subprocess.Popen(cmd, shell=True)
                out, err = p.communicate()
                print(err)
                print(out)

            if myresult[0][3] == 'admin':
                mycursor.execute("SELECT * FROM hostel.admins WHERE admin_Id = %s;", [user_id])
                fetg = mycursor.fetchall()
                mycursor.execute("INSERT INTO hostel.log_rept (user_id, user_Name, user_role, Login_date, Login_time) VALUES (%s, %s, %s, CURDATE(), CURTIME());", (myresult[0][2], fetg[0][1], myresult[0][3]))
                mydb.commit()

                mycursor.execute("SELECT * FROM hostel.log_rept;")
                log_id_f = mycursor.fetchall()
                i = len(log_id_f) - 1
                curent_log_id = log_id_f[i][0]

                dic = {'session_id': user_id, 'log_id': curent_log_id}
                json_object = json.dumps(dic, indent=4)
                print(json_object)
                with open("SessionInfo.json", "w") as outfile:
                    outfile.write(json_object)

                import subprocess
                cmd = 'python AdminPage.py'
                p = subprocess.Popen(cmd, shell=True)
                out, err = p.communicate()
                print(err)
                print(out)


username = tk.StringVar()
password = tk.StringVar()
#  logo
login_image = ImageTk.PhotoImage(file='./imag/123.ico')
tk.Label(login_Page_frame, image=login_image, border=0, justify='center').place(relx=0.5, rely=0.26, anchor='center')
# username

tk.Label(login_Page_frame, text='User Name', bg='#4B3621', fg='white', anchor='w', borderwidth=0, font='-family {Cascadia Code} -size 11').place(rely=0.6, relx=0.1, relheight=0.05, relwidth=0.8)
fht = tk.Entry(login_Page_frame, textvariable=username, bg='#4B3621', fg='white', borderwidth=1, font='-family {Courier New} -size 11')
fht.place(rely=0.65, relx=0.1, relheight=0.06, relwidth=0.8)
changeOnHover(fht, '#1e4d2b', '#4B3621')

tk.Label(login_Page_frame, text='Password', anchor='w', bg='#4B3621', fg='white', borderwidth=0, font='-family {Cascadia Code} -size 11').place(rely=0.75, relx=0.1, relheight=0.05, relwidth=0.8)
grt = tk.Entry(login_Page_frame, textvariable=password, bg='#4B3621', fg='white', show='#', borderwidth=1, font='-family {Consolas} -size 11')
grt.place(rely=0.8, relx=0.1, relheight=0.06, relwidth=0.8)
changeOnHover(grt, '#1e4d2b', '#4B3621')

# login button
login_button = tk.Button(login_Page_frame, text="Login", borderwidth=0, bg='#00ffff', font='-family {Georgia} -size 10 -weight bold', command=lambda: Login_function(username.get(), password.get()))
login_button.place(relx=0.5, rely=0.92, relwidth=0.3, anchor='center')
changeOnHover(login_button, '#1e4d2b', '#00ffff')

root.mainloop()  # Event loop  used keeps the window visible on the screen
