import tkinter as tk
from tkinter import ttk
from tkcalendar import *
from PIL import Image, ImageTk
import base64
import io
import json
import smtplib
import subprocess
import threading
# --------------------------------------- UI color settings --------------------------------------------------------

side_bar_frame_bg_color = '#654321' # sidebar background color
side_bar_frame_fg_color = 'white'   # sidebar text color
side_bar_bt_hover_color = '#C2B280'

sections_bg_colors = 'gray'
sections_fg_colors = "black"
# --------------------------------------------------------------------------------------------------------------------
# Create an instance of tkinter frame
root = tk.Tk()
root.state('zoomed')
root.minsize(1050, 800)
# root.maxsize(1350, 950)
root.config(bg='black')


# root.overrideredirect(True)#Make the window borderless
root.rowconfigure(0, weight=1)  # make our frame expand along with the window
root.columnconfigure(0, weight=1)  # make our frame expand along with the window
# ---------------------- creating a connection to the database.---------------------------------------------------------
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12hezron12",
    database="hostel"
)
mycursor = mydb.cursor()

with open('SessionInfo.json', 'r') as openfile:
    json_object = json.load(openfile)
session_user_id = json_object['session_id']
log_id =  json_object['log_id']
print("log_id:", log_id)
mycursor.execute("select * from users where user_id = %s", [session_user_id])


output = mycursor.fetchall()
db_username = output[0][0]
db_userpassword = output[0][1]
db_userid = output[0][2]
db_userrole = output[0][3]
db_image = output[0][4]
mycursor.execute("select * from hostel.admins where user_id=%s", [db_userid])
admin_out = mycursor.fetchall()
db_full_Name = admin_out[0][1]
db_phone_number = admin_out[0][2]
db_email = admin_out[0][3]


# -------------------------------- Functions ===========================================================================
def frame_changer(frame):
    frame.tkraise()

def Exit_program():
    mycursor.execute("UPDATE hostel.log_rept SET logout_time = CURTIME() WHERE Log_id = %s;", [log_id])
    mydb.commit()


    cmd = 'python Home_Module.py'
    p = subprocess.Popen(cmd, shell=True)
    out, err = p.communicate()
    print(err)
    print(out)

    threading.Thread(target=Home_page_call).start()
    root.destroy()

def restart_g():
    def open_instance():
        cmd = 'python Home_Module.py'
        p = subprocess.Popen(cmd, shell=True)
        out, err = p.communicate()
        print(err)
        print(out)


    threading.Thread(target=open_instance).start()

    cmd = 'python AdminPage.py'
    p = subprocess.Popen(cmd, shell=True)
    out, err = p.communicate()
    messagebox.showwarning("student portal", 'error while resterting')
    print(out)
    print(err)

    


def changeOnHover(button, colorOnHover, colorOnLeave):
    # adjusting backgroung of the widget
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover))

    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))


def show_frame_OnHover(frame, colorOnHover, colorOnLeave):
    frame.bind("<Enter>", func=lambda e: frame.config(background=colorOnHover))
    # background color on leving widget
    frame.bind("<Leave>", func=lambda e: frame.config(background=colorOnLeave))

 def Home_page_call():
        cmd = 'python Home_Module.py'
        p = subprocess.Popen(cmd, shell=True)
        out, err = p.communicate()
        print(err)
        print(out)

        threading.Thread(target=Home_page_call).start()
        root.destroy()

# ================================== Side Bar Frame ====================================================================

side_bar_frame = tk.Frame(root, bg=side_bar_frame_bg_color)
side_bar_frame.place(relwidth=0.17, relheight=1)

info_frame_lable = tk.Label(side_bar_frame, text='ADMIN', bg=side_bar_frame_bg_color, fg=side_bar_frame_fg_color,
                            font='-size 16 -weight bold')
info_frame_lable.place(rely=0.04, relx=0, relwidth=1, relheight=0.05)

info_frame = tk.Frame(side_bar_frame, bg='gray')
info_frame.place(rely=0.92, relx=0.03, relwidth=0.945, relheight=0.07)
info_frame_lable = tk.Label(info_frame,
                            text='For any system issue please call\nKenya: +254714415034 \nOther: +254756435127',
                            bg='#996515', fg='white', font='-family {Courier New} -size 8')
info_frame_lable.place(relwidth=1, relheight=1)

side_bar_frame_bg_button_color = side_bar_frame_bg_color
side_bar_frame_fg_button_color = side_bar_frame_fg_color

# sidebar button BUTTONS #
profile_BT = tk.Button(side_bar_frame, bg=side_bar_frame_bg_button_color, foreground=side_bar_frame_fg_button_color,
                       text='⍜ Profile', anchor='w', borderwidth=0, font='-family {Consolas} -size 11',
                       command=lambda: frame_changer(profile_frame))
profile_BT.place(rely=0.1, relx=0, relwidth=1, relheight=0.03)
changeOnHover(profile_BT, side_bar_bt_hover_color, side_bar_frame_bg_button_color)

Hostel_Status_BT = tk.Button(side_bar_frame, bg=side_bar_frame_bg_button_color,foreground=side_bar_frame_fg_button_color, text='⌘ Hostel Status', anchor='w',borderwidth=0, font='-family {Consolas} -size 11',command=lambda: frame_changer(Hostel_Status_frame))
Hostel_Status_BT.place(rely=0.135, relx=0, relwidth=1, relheight=0.03)
changeOnHover(Hostel_Status_BT, side_bar_bt_hover_color, side_bar_frame_bg_button_color)

Reserve_Room_BT = tk.Button(side_bar_frame, bg=side_bar_frame_bg_button_color, foreground=side_bar_frame_fg_button_color, text='⍗ Reserve', anchor='w', borderwidth=0,font='-family {Consolas} -size 11', command=lambda: frame_changer(Reserve_Room_frame))
Reserve_Room_BT.place(relx=0, rely=0.17, relwidth=1, relheight=0.03)
changeOnHover(Reserve_Room_BT, side_bar_bt_hover_color, side_bar_frame_bg_button_color)

Deallocate_BT = tk.Button(side_bar_frame, bg=side_bar_frame_bg_button_color, foreground=side_bar_frame_fg_button_color, text='Ω Deallocate Room', anchor='w', borderwidth=0, font='-family {Consolas} -size 11', command=lambda: frame_changer(Deallocate_frame))
Deallocate_BT.place(relx=0, rely=0.205, relwidth=1, relheight=0.03)
changeOnHover(Deallocate_BT, side_bar_bt_hover_color, side_bar_frame_bg_button_color)

Rooms_BT = tk.Button(side_bar_frame, bg=side_bar_frame_bg_button_color, foreground=side_bar_frame_fg_button_color, text='∷ Rooms', anchor='w', borderwidth=0, font='-family {Consolas} -size 11', command=lambda: frame_changer(Rooms_frame))
Rooms_BT.place(relx=0, rely=0.24, relwidth=1, relheight=0.03)
changeOnHover(Rooms_BT, side_bar_bt_hover_color, side_bar_frame_bg_button_color)

Reports_BT = tk.Button(side_bar_frame, bg=side_bar_frame_bg_button_color, foreground=side_bar_frame_fg_button_color, text='⊛ Reports', anchor='w', borderwidth=0, font='-family {Consolas} -size 11',command=lambda: frame_changer(Reports_frame))
Reports_BT.place(relx=0, rely=0.275, relwidth=1, relheight=0.03)
changeOnHover(Reports_BT, side_bar_bt_hover_color, side_bar_frame_bg_button_color)

Complaints_BT = tk.Button(side_bar_frame, bg=side_bar_frame_bg_button_color, foreground=side_bar_frame_fg_button_color,text='⌭ Complaints', anchor='w', borderwidth=0, font='-family {Consolas} -size 11', command=lambda: frame_changer(Complaints_frame))
Complaints_BT.place(relx=0, rely=0.31, relwidth=1, relheight=0.03)
changeOnHover(Complaints_BT, side_bar_bt_hover_color, side_bar_frame_bg_button_color)

Notice_Board_BT = tk.Button(side_bar_frame, bg=side_bar_frame_bg_button_color, foreground=side_bar_frame_fg_button_color, text='⌨ Notice Board', anchor='w', borderwidth=0,font='-family {Consolas} -size 11', command=lambda: frame_changer(Notice_Board_frame))
Notice_Board_BT.place(relx=0, rely=0.345, relwidth=1, relheight=0.03)
changeOnHover(Notice_Board_BT, side_bar_bt_hover_color, side_bar_frame_bg_button_color)

Visitor_log_BT = tk.Button(side_bar_frame, bg=side_bar_frame_bg_button_color, foreground=side_bar_frame_fg_button_color, text='⍝ Visitor log', anchor='w', borderwidth=0, font='-family {Consolas} -size 11', command=lambda: frame_changer(Visitor_log_frame))
Visitor_log_BT.place(relx=0, rely=0.38, relwidth=1, relheight=0.03)
changeOnHover(Visitor_log_BT, side_bar_bt_hover_color, side_bar_frame_bg_button_color)

Transaction_BT = tk.Button(side_bar_frame, bg=side_bar_frame_bg_button_color, foreground=side_bar_frame_fg_button_color, text='〶 Transaction log', anchor='w', borderwidth=0, font='-family {Consolas} -size 11', command=lambda: frame_changer(Transaction_frame))
Transaction_BT. place(relx=0, rely=0.415, relwidth=1, relheight=0.03)
changeOnHover(Transaction_BT, side_bar_bt_hover_color, side_bar_frame_bg_button_color)

log_out_bt = tk.Button(side_bar_frame, bg=side_bar_frame_bg_button_color, foreground=side_bar_frame_fg_button_color, text='✘ Exit', anchor='w', borderwidth=0, font='-family {Consolas} -size 11', command=lambda: Exit_program())
log_out_bt.place(relx=0, rely=0.585, relwidth=1, relheight=0.03)
changeOnHover(log_out_bt, side_bar_bt_hover_color, side_bar_frame_bg_button_color)






restart_bt = tk.Button(side_bar_frame, fg='white', bg=side_bar_frame_bg_button_color, text="⟳ Restart", borderwidth=0,   anchor='w', font='-family {Cambria} -size 13', command=restart_g)
restart_bt.place(rely=0.63, relwidth=1, relheight=0.03)
changeOnHover(restart_bt, side_bar_bt_hover_color, side_bar_frame_bg_button_color)

# ================================ Frame ===============================================================================
# ------------------------------- PROFILE FRAME ------------------------------------------------------------------------
profile_frame = tk.Frame(root, bg=sections_bg_colors)
profile_frame.place(relx=0.173, rely=0, relwidth=0.83, relheight=1)

profil_photo_frame = tk.Frame(profile_frame, bg=sections_bg_colors)
profil_photo_frame.place(relx=0.04, rely=0.05, relwidth=0.16, relheight=0.16)

try:
    binary_data = base64.b64decode(db_image)  # Decode the string
    profile_image = Image.open(io.BytesIO(binary_data))  # Convert the bytes into a PIL image
    Resized_image = profile_image.resize((204, 160), Image.ANTIALIAS)
    new_image = ImageTk.PhotoImage(Resized_image)
    tk.Label(profil_photo_frame, image=new_image, bg=sections_bg_colors, border=0, justify='center').place(relx=0, rely=0, relwidth=1, relheight=1)
except:
    tk.Label(profil_photo_frame, bg=sections_bg_colors, border=0, justify='center').place(relx=0, rely=0, relwidth=1, relheight=1)


tk.Label(profile_frame, text=f'{db_full_Name}', fg=sections_fg_colors, borderwidth=0, bg=sections_bg_colors,
         font='-family {Georgia} -size 11 -weight bold').place(relx=0.244, rely=0.05)
tk.Label(profile_frame, text=f' {db_email}  -  Administrator',fg=sections_fg_colors, bg=sections_bg_colors, borderwidth=0,
         font='-family {Georgia} -size 11 -weight bold').place(relx=0.24, rely=0.1)

# -------------
basic_info = tk.Label(profile_frame, text='Basic Information', anchor='w', fg=sections_fg_colors, bg=sections_bg_colors, borderwidth=10,
                      font='-family {Georgia} -size 13 -weight bold')
basic_info.place(relx=0.04, rely=0.22)
basic_info_frame = tk.Frame(profile_frame, bg=sections_bg_colors)
basic_info_frame.place(relx=0.07, rely=0.26, relwidth=0.4, relheight=0.2)

tk.Label(basic_info_frame, text='Full Name:', anchor='w', borderwidth=0,fg=sections_fg_colors, bg=sections_bg_colors,
         font='-family {Georgia} -size 10 -weight bold').place(relx=0.0, rely=0, relwidth=0.37, relheight=0.17)
tk.Label(basic_info_frame, text=f'{db_full_Name}', anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
         font='-family {Georgia} -size 10 -weight bold').place(relx=0.41, rely=0, relwidth=0.57, relheight=0.17)

tk.Label(basic_info_frame, text='Email Address:', anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
         font='-family {Georgia} -size 10 -weight bold').place(relx=0.0, rely=0.2, relwidth=0.37, relheight=0.17)
tk.Label(basic_info_frame, anchor='w', borderwidth=0, text=db_email,  fg=sections_fg_colors, bg=sections_bg_colors,
         font='-family {Georgia} -size 10 -weight bold').place(relx=0.41, rely=0.2, relwidth=0.57, relheight=0.17)

tk.Label(basic_info_frame, text='Admin ID:', anchor='w', borderwidth=0, bg=sections_bg_colors, fg=sections_fg_colors,
         font='-family {Georgia} -size 10 -weight bold').place(relx=0.0, rely=0.4, relwidth=0.37, relheight=0.17)
tk.Label(basic_info_frame, anchor='w', borderwidth=0, text=db_userid, bg=sections_bg_colors, fg=sections_fg_colors,
         font='-family {Georgia} -size 10 -weight bold').place(relx=0.41, rely=0.4, relwidth=0.57, relheight=0.17)

tk.Label(basic_info_frame, text='Username:', anchor='w', borderwidth=0, bg=sections_bg_colors, fg=sections_fg_colors,
         font='-family {Georgia} -size 10 -weight bold').place(relx=0.0, rely=0.6, relwidth=0.37, relheight=0.17)
tk.Label(basic_info_frame, anchor='w', borderwidth=0, text=db_username, bg=sections_bg_colors, fg=sections_fg_colors,
         font='-family {Georgia} -size 10 -weight bold').place(relx=0.41, rely=0.6, relwidth=0.57, relheight=0.17)

tk.Label(basic_info_frame, text='Current Password:', anchor='w', borderwidth=0, bg=sections_bg_colors, fg=sections_fg_colors,
         font='-family {Georgia} -size 10 -weight bold').place(relx=0.0, rely=0.8, relwidth=0.37, relheight=0.17)
tk.Label(basic_info_frame, anchor='w', borderwidth=0, text=db_userpassword, bg=sections_bg_colors, fg=sections_fg_colors,
         font='-family {Georgia} -size 10 -weight bold').place(relx=0.41, rely=0.8, relwidth=0.57, relheight=0.17)

# ----------------------
tk.Label(profile_frame, text='Update Profile', anchor='w', bg=sections_bg_colors, borderwidth=10, fg=sections_fg_colors,
         font='-family {Georgia} -size 13 -weight bold').place(relx=0.04, rely=0.5)

update_Profile_frame = tk.Frame(profile_frame, bg=sections_bg_colors)
update_Profile_frame.place(relx=0.07, rely=0.54, relwidth=0.4, relheight=0.25)

# store username  and password variables
change_username = tk.StringVar()
change_password = tk.StringVar()
change_Phone_no = tk.StringVar()
change_Email = tk.StringVar()

tk.Label(update_Profile_frame, text='Change Username :', anchor='w', borderwidth=0, bg=sections_bg_colors, fg=sections_fg_colors,
         font='-family {Georgia} -size 10 -weight bold').place(relx=0.01, rely=0, relwidth=0.4, relheight=0.13)
t12 = tk.Entry(update_Profile_frame, textvariable=change_username, borderwidth=1, fg=sections_fg_colors,   bg=sections_bg_colors,
               font='-family {Georgia} -size 12 -slant italic')
t12.place(relx=0.41, rely=0, relwidth=0.54, relheight=0.13)
changeOnHover(t12, '#D0F0C0', sections_bg_colors)

tk.Label(update_Profile_frame, text='Change Password :', anchor='w', fg=sections_fg_colors, bg=sections_bg_colors, borderwidth=0,
         font='-family {Georgia} -size 10 -weight bold').place(relx=0.01, rely=0.16, relwidth=0.4, relheight=0.13)
t13 = tk.Entry(update_Profile_frame, show="*", textvariable=change_password, fg=sections_fg_colors,  bg=sections_bg_colors, borderwidth=1,
               font='-family {Georgia} -size 12 -slant italic')
t13.place(relx=0.41, rely=0.16, relwidth=0.54, relheight=0.13)
changeOnHover(t13, '#D0F0C0', sections_bg_colors)

tk.Label(update_Profile_frame, text='Change Phone NO :', anchor='w', fg=sections_fg_colors, bg=sections_bg_colors, borderwidth=0,
         font='-family {Georgia} -size 10 -weight bold').place(relx=0.01, rely=0.32, relwidth=0.4, relheight=0.13)
t14 = tk.Entry(update_Profile_frame, textvariable=change_Phone_no, fg=sections_fg_colors, bg=sections_bg_colors, borderwidth=1,
               font='-family {Georgia} -size 12 -slant italic')
t14.place(relx=0.41, rely=0.32, relwidth=0.54, relheight=0.13)
changeOnHover(t14, '#D0F0C0', sections_bg_colors)

tk.Label(update_Profile_frame, text='Change Email :', anchor='w', fg=sections_fg_colors,  bg=sections_bg_colors, borderwidth=0,
         font='-family {Georgia} -size 10 -weight bold').place(relx=0.01, rely=0.48, relwidth=0.4, relheight=0.13)
t15 = tk.Entry(update_Profile_frame, textvariable=change_Email, fg=sections_fg_colors, bg=sections_bg_colors, borderwidth=1,
               font='-family {Georgia} -size 12 -slant italic')
t15.place(relx=0.41, rely=0.48, relwidth=0.54, relheight=0.13)
changeOnHover(t15, '#D0F0C0', sections_bg_colors)

global filepath
filepath = None


def profile_update_photo():
    from tkinter import filedialog
    global filepath
    filepath = filedialog.askopenfilename(title="Select Profile Photo", filetypes=((" ", "*.jpg"), (" ", "*.png")))


def update_p_d(username, password, Phone, Email):
    global filepath
    log.place(relx=0.49, rely=0.54, relwidth=0.4, relheight=0.2)
    y = 0.1
    if username != '':
        mycursor.execute("UPDATE hostel.users SET user_name=%s WHERE (user_id=%s);", (username, db_userid))
        mydb.commit()
        tk.Label(log, text=f'log: username changed to: {username}', anchor='w',   bg=sections_bg_colors, fg='#004830',
                 font='-family {Georgia} -size 10 -slant italic').place(relx=0, rely=y, relheight=0.11, relwidth=1)
    else:
        print('user blank')
        tk.Label(log, text='log: no change username', anchor='w',  bg=sections_bg_colors, fg='red',
                 font='-family {Georgia} -size 10 -slant italic').place(relx=0, rely=y, relheight=0.11, relwidth=1)

    y = y + 0.12
    if password != '':
        mycursor.execute("UPDATE hostel.users SET user_passwd=%s WHERE (user_id=%s);", (password, db_userid))
        mydb.commit()
        tk.Label(log, text=f'log: password changed to: {password}', anchor='w', bg='white', fg='#004830',
                 font='-family {Georgia} -size 10 -slant italic').place(relx=0, rely=y, relheight=0.11, relwidth=1)
    else:
        print('pass blank')
        tk.Label(log, text='log: no change in password', anchor='w', bg=sections_bg_colors, fg='red',
                 font='-family {Georgia} -size 10 -slant italic').place(relx=0, rely=y, relheight=0.11, relwidth=1)

    y = y + 0.12
    if Phone != '':
        mycursor.execute("UPDATE hostel.admins SET phone_no=%s WHERE (admin_Id=%s);", (Phone, db_userid))
        mydb.commit()
        tk.Label(log, text=f'log: Phone Number changed to: {Phone}', anchor='w',  bg=sections_bg_colors, fg='#004830',
                 font='-family {Georgia} -size 10 -slant italic').place(relx=0, rely=y, relheight=0.11, relwidth=1)

    else:
        print('phone blank')
        tk.Label(log, text='log: no change in phone number', anchor='w',   bg=sections_bg_colors, fg='red',
                 font='-family {Georgia} -size 10 -slant italic').place(relx=0, rely=y, relheight=0.11, relwidth=1)

    y = y + 0.12
    if Email != '':
        mycursor.execute("UPDATE hostel.admins SET Email=%s WHERE (admin_Id=%s);", (Email, db_userid))
        mydb.commit()
        tk.Label(log, text=f'log: Email changed to: {Email}', anchor='w',   bg=sections_bg_colors, fg='#004830',
                 font='-family {Georgia} -size 10 -slant italic').place(relx=0, rely=y, relheight=0.11, relwidth=1)
    else:
        print('email blank')
        tk.Label(log, text='log: no change in email', anchor='w',  bg=sections_bg_colors, fg='red',
                 font='-family {Georgia} -size 10 -slant italic').place(relx=0, rely=y, relheight=0.11, relwidth=1)

    y = y + 0.12
    if filepath != None and filepath != '':
        # Open a file in binary mode
        print(filepath)
        try:
            file = open(filepath, 'rb').read()
            # We must encode the file to get base64 string
            file = base64.b64encode(file)
            # Execute the query and commit the database.
            mycursor.execute('UPDATE hostel.users SET user_image = %s WHERE user_id = %s', [file, db_userid])
            mydb.commit()
            tk.Label(log, text=f'log: Photo changed changed to: {filepath}', anchor='w', bg=sections_bg_colors, fg='#004830',
                     font='-family {Georgia} -size 10 -slant italic').place(relx=0, rely=y, relheight=0.11, relwidth=1)
        except:
            tk.Label(log, text=f'log: wrong profile photo file path', anchor='w',bg=sections_bg_colors, fg='#A67B50',
                     font='-family {Georgia} -size 10 -slant italic').place(relx=0, rely=y, relheight=0.11, relwidth=1)

    else:
        tk.Label(log, text='log: no change in profile photo', anchor='w', bg=sections_bg_colors, fg='red',
                 font='-family {Georgia} -size 10 -slant italic').place(relx=0, rely=y, relheight=0.11, relwidth=1)


def clear_p_entry():
    t12.delete(0, tk.END)
    t13.delete(0, tk.END)
    t14.delete(0, tk.END)
    t14.delete(0, tk.END)
    log.place_forget()


tk.Label(update_Profile_frame, text='Change Profile :', anchor='w', fg=sections_fg_colors, bg=sections_bg_colors, borderwidth=0,
         font='-family {Georgia} -size 10 -weight bold').place(relx=0.01, rely=0.64, relwidth=0.4, relheight=0.13)
t16 = tk.Button(update_Profile_frame, text="Change Your Profile", fg=sections_fg_colors, bg=sections_bg_colors, borderwidth=1,
                font='-family {Georgia} -size 12 -slant italic', command=profile_update_photo)
t16.place(relx=0.41, rely=0.64, relwidth=0.54, relheight=0.13)
changeOnHover(t16, '#7F7053', sections_bg_colors)

cancel_profile = tk.Button(update_Profile_frame, text="CANCEL", borderwidth=0, bg='light gray', activebackground='Red',
                           command=lambda: clear_p_entry())
cancel_profile.place(relx=0.19, rely=0.8, relwidth=0.3, relheight=0.17)
changeOnHover(cancel_profile, '#D1BEA8', 'light gray')
update_profile = tk.Button(update_Profile_frame, text="UPDATE", borderwidth=0, bg='light gray',
                           activebackground='green',
                           command=lambda: update_p_d(change_username.get(), change_password.get(),
                                                      change_Phone_no.get(), change_Email.get()))
update_profile.place(relx=0.5, rely=0.8, relwidth=0.3, relheight=0.17)
changeOnHover(update_profile, '#D1BEA8', 'light gray')

log = tk.Frame(profile_frame, bg=sections_bg_colors)

# ------------------------HOSTEL STATUS FRAME --------------------------------------------------------------------------

Hostel_Status_frame = tk.Frame(root, bg=sections_bg_colors)
Hostel_Status_frame.place(relx=0.173, rely=0, relwidth=0.83, relheight=1)

navbar_hostel_status_frame = tk.Frame(Hostel_Status_frame, bg='gray')
navbar_hostel_status_frame.place(relx=0, rely=0, relwidth=1, relheight=0.03)
global total_number_of_rooms
global total_number_of_male_rooms
global total_number_of_female_rooms
global total_number_of_resident
global total_male_resident
global total_female_resident
global total_number_of_available_rooms
global total_number_of_male_available_rooms
global total_number_of_female_available_rooms
global total_number_of_reserved
global total_number_of_female__rooms_reserved
global total_number_of_male__rooms_reserved


def show_STATUS_FRAME():
    global total_number_of_rooms
    global total_number_of_male_rooms
    global total_number_of_female_rooms
    global total_number_of_resident
    global total_male_resident
    global total_female_resident
    global total_number_of_available_rooms
    global total_number_of_male_available_rooms
    global total_number_of_female_available_rooms
    global total_number_of_reserved
    global total_number_of_female__rooms_reserved
    global total_number_of_male__rooms_reserved
    global total_staff
    mycursor.execute("SELECT * FROM hostel.room")
    total_rooms = mycursor.fetchall()
    total_number_of_rooms = len(total_rooms)
    mycursor.execute("SELECT *  FROM hostel.room where gender_room_type = 'male-room';")
    male_rooms = mycursor.fetchall()
    total_number_of_male_rooms = len(male_rooms)
    mycursor.execute("SELECT *  FROM hostel.room where gender_room_type = 'female-room';")
    female_rooms = mycursor.fetchall()
    total_number_of_female_rooms = len(female_rooms)

    mycursor.execute("SELECT *  FROM hostel.room where room_status = 'occupied';")
    resident = mycursor.fetchall()
    total_number_of_resident = len(resident)
    mycursor.execute("SELECT *  FROM hostel.room where room_status = 'occupied' and gender_room_type = 'male-room';")
    male_resident = mycursor.fetchall()
    total_male_resident = len(male_resident)
    mycursor.execute("SELECT *  FROM hostel.room where room_status = 'occupied' and gender_room_type = 'female-room';")
    female_resident = mycursor.fetchall()
    total_female_resident = len(female_resident)

    mycursor.execute("SELECT *  FROM hostel.room where room_status = 'not occupied';")
    Available_rooms = mycursor.fetchall()
    total_number_of_available_rooms = len(Available_rooms)
    mycursor.execute(
        "SELECT *  FROM hostel.room where room_status = 'not occupied' and gender_room_type = 'male-room';")
    male_Available_rooms = mycursor.fetchall()
    total_number_of_male_available_rooms = len(male_Available_rooms)
    mycursor.execute(
        "SELECT *  FROM hostel.room where room_status = 'not occupied' and gender_room_type = 'female-room';")
    female_Available_rooms = mycursor.fetchall()
    total_number_of_female_available_rooms = len(female_Available_rooms)




show_STATUS_FRAME()

tk.Button(Hostel_Status_frame, text='⟳ refresh', fg=sections_fg_colors, bg=sections_bg_colors, borderwidth=1, command=show_STATUS_FRAME).place(rely=0.03,
                                                                                                             relx=0.88,
                                                                                                             relheight=0.03,
                                                                                                             relwidth=0.1)

total_rooms_frame = tk.Frame(Hostel_Status_frame,  bg=sections_bg_colors,)
total_rooms_frame.place(relx=0.02, rely=0.1, relwidth=0.21, relheight=0.06)

total_rooms_lable1 = tk.Label(total_rooms_frame, text="TOTAL ROOMS\n(total number of rooms)", anchor='center',
                              font='-family {Times New Roman} -size 8 -weight bold', fg=sections_fg_colors, bg=sections_bg_colors)
total_rooms_lable1.place(relwidth=0.6, relheight=1)
total_rooms_lable2 = tk.Label(total_rooms_frame, text=f"{total_number_of_rooms}", anchor='center', fg='#704214',
                              font='-family {Courier New} -size 15 -weight bold -slant italic',  bg=sections_bg_colors)
total_rooms_lable2.place(relx=0.6, relwidth=0.4, relheight=1)

Male_rooms_frame = tk.Frame(Hostel_Status_frame, bg=sections_bg_colors,)
Male_rooms_frame.place(relx=0.27, rely=0.1, relwidth=0.21, relheight=0.06)

Male_rooms_lable1 = tk.Label(Male_rooms_frame, text="TOTAL MALE ROOMS\n(number of male rooms)", anchor='center', fg=sections_fg_colors, bg=sections_bg_colors,
                             font='-family {Times New Roman} -size 8 -weight bold')
Male_rooms_lable1.place(relwidth=0.6, relheight=1)
Male_rooms_lable2 = tk.Label(Male_rooms_frame, text=f"{total_number_of_male_rooms}", anchor='center', fg='#704214', bg=sections_bg_colors,
                             font='-family {Courier New} -size 15 -weight bold -slant italic')
Male_rooms_lable2.place(relx=0.6, relwidth=0.4, relheight=1)

Female_rooms_frame = tk.Frame(Hostel_Status_frame,  bg=sections_bg_colors,)
Female_rooms_frame.place(relx=0.52, rely=0.1, relwidth=0.21, relheight=0.06)

Female_rooms_lable1 = tk.Label(Female_rooms_frame, text="TOTAL FEMALE ROOMS\n(number of female rooms)", anchor='center', fg=sections_fg_colors, bg=sections_bg_colors,
                               font='-family {Times New Roman} -size 8 -weight bold')
Female_rooms_lable1.place(relwidth=0.6, relheight=1)
Female_rooms_lable2 = tk.Label(Female_rooms_frame, text=f"{total_number_of_female_rooms}", anchor='center', bg=sections_bg_colors,
                               fg='#704214', font='-family {Courier New} -size 15 -weight bold -slant italic')
Female_rooms_lable2.place(relx=0.6, relwidth=0.4, relheight=1)

total_Resident_frame = tk.Frame(Hostel_Status_frame, bg=sections_bg_colors,)
total_Resident_frame.place(relx=0.02, rely=0.2, relwidth=0.21, relheight=0.06)

total_Resident_lable1 = tk.Label(total_Resident_frame, text="TOTAL RESIDENT\n(total number of residence)", fg=sections_fg_colors, bg=sections_bg_colors,
                                 anchor='center', font='-family {Times New Roman} -size 8 -weight bold')
total_Resident_lable1.place(relwidth=0.6, relheight=1)
total_Resident_lable2 = tk.Label(total_Resident_frame, text=f"{total_number_of_resident}", anchor='center', bg=sections_bg_colors,
                                 fg='#704214', font='-family {Courier New} -size 15 -weight bold -slant italic')
total_Resident_lable2.place(relx=0.6, relwidth=0.4, relheight=1)

male_Resident_frame = tk.Frame(Hostel_Status_frame, bg=sections_bg_colors,)
male_Resident_frame.place(relx=0.27, rely=0.2, relwidth=0.21, relheight=0.06)
male_Resident_lable1 = tk.Label(male_Resident_frame, text="MALE RESIDENTS\n(total male residents)", anchor='center', fg=sections_fg_colors, bg=sections_bg_colors,
                                font='-family {Times New Roman} -size 8 -weight bold')
male_Resident_lable1.place(relwidth=0.6, relheight=1)
male_Resident_lable2 = tk.Label(male_Resident_frame, text=f"{total_male_resident}", anchor='center', fg='#704214',  bg=sections_bg_colors,
                                font='-family {Courier New} -size 15 -weight bold -slant italic')
male_Resident_lable2.place(relx=0.6, relwidth=0.4, relheight=1)

female_Resident_frame = tk.Frame(Hostel_Status_frame, bg=sections_bg_colors,)
female_Resident_frame.place(relx=0.52, rely=0.2, relwidth=0.21, relheight=0.06)
female_Resident_lable1 = tk.Label(female_Resident_frame, text="FEMALE RESIDENTS\n(number of rooms reserved)", fg=sections_fg_colors, bg=sections_bg_colors,
                                  anchor='center', font='-family {Times New Roman} -size 8 -weight bold')
female_Resident_lable1.place(relwidth=0.6, relheight=1)
female_Resident_lable2 = tk.Label(female_Resident_frame, text=f"{total_female_resident}", anchor='center', fg='#704214', bg=sections_bg_colors,
                                  font='-family {Courier New} -size 15 -weight bold -slant italic')
female_Resident_lable2.place(relx=0.6, relwidth=0.4, relheight=1)

available_rooms_frame = tk.Frame(Hostel_Status_frame, bg=sections_bg_colors,)
available_rooms_frame.place(relx=0.02, rely=0.3, relwidth=0.21, relheight=0.06)
available_rooms_lable1 = tk.Label(available_rooms_frame, text="AVAILABLE ROOMS\n(number of rooms unoccupied)", fg=sections_fg_colors, bg=sections_bg_colors,
                                  anchor='center', font='-family {Times New Roman} -size 8 -weight bold')
available_rooms_lable1.place(relwidth=0.6, relheight=1)
available_rooms_lable2 = tk.Label(available_rooms_frame, text=f"{total_number_of_available_rooms}", anchor='center',  bg=sections_bg_colors,
                                  fg='#704214', font='-family {Courier New} -size 15 -weight bold -slant italic')
available_rooms_lable2.place(relx=0.6, relwidth=0.4, relheight=1)

male_Resident_frame = tk.Frame(Hostel_Status_frame, bg=sections_bg_colors,)
male_Resident_frame.place(relx=0.27, rely=0.3, relwidth=0.21, relheight=0.06)
male_Resident_lable1 = tk.Label(male_Resident_frame, text="MALE AVAILABLE ROOMS\n(total available male rooms)", fg=sections_fg_colors, bg=sections_bg_colors,
                                anchor='center', font='-family {Times New Roman} -size 8 -weight bold')
male_Resident_lable1.place(relwidth=0.6, relheight=1)
male_Resident_lable2 = tk.Label(male_Resident_frame, text=f"{total_number_of_male_available_rooms}", anchor='center',  bg=sections_bg_colors,
                                fg='#704214', font='-family {Courier New} -size 15 -weight bold -slant italic')
male_Resident_lable2.place(relx=0.6, relwidth=0.4, relheight=1)

female_Resident_frame = tk.Frame(Hostel_Status_frame,  bg=sections_bg_colors,)
female_Resident_frame.place(relx=0.52, rely=0.3, relwidth=0.21, relheight=0.06)
female_Resident_lable1 = tk.Label(female_Resident_frame, text="FEMALE AVAILABLE ROOMS\n(total available female rooms)", fg=sections_fg_colors, bg=sections_bg_colors,
                                  anchor='center', font='-family {Times New Roman} -size 8 -weight bold')
female_Resident_lable1.place(relwidth=0.6, relheight=1)
female_Resident_lable2 = tk.Label(female_Resident_frame, text=f"{total_number_of_female_available_rooms}",  bg=sections_bg_colors,
                                  anchor='center', fg='#704214',
                                  font='-family {Courier New} -size 15 -weight bold -slant italic')
female_Resident_lable2.place(relx=0.6, relwidth=0.4, relheight=1)

total_reservation_frame = tk.Frame(Hostel_Status_frame , bg=sections_bg_colors,)
total_reservation_frame.place(relx=0.02, rely=0.4, relwidth=0.21, relheight=0.06)
total_reservation_lable1 = tk.Label(total_reservation_frame, text="TOTAL RESERVATION\n(total number of reservation)", fg=sections_fg_colors, bg=sections_bg_colors,
                                    anchor='center', font='-family {Times New Roman} -size 8 -weight bold')
total_reservation_lable1.place(relwidth=0.6, relheight=1)


male_room_reservation_frame = tk.Frame(Hostel_Status_frame, bg=sections_bg_colors,)
male_room_reservation_frame.place(relx=0.27, rely=0.4, relwidth=0.21, relheight=0.06)
male_room_reservation_lable1 = tk.Label(male_room_reservation_frame, text="MALE RESERVATION\n(male rooms reserved)", fg=sections_fg_colors, bg=sections_bg_colors,
                                        anchor='center', font='-family {Times New Roman} -size 8 -weight bold')
male_room_reservation_lable1.place(relwidth=0.6, relheight=1)


female_room_reservation_frame = tk.Frame(Hostel_Status_frame,  bg=sections_bg_colors,)
female_room_reservation_frame.place(relx=0.52, rely=0.4, relwidth=0.21, relheight=0.06)
female_room_reservation_lable1 = tk.Label(female_room_reservation_frame,
                                          text="FEMALE RESERVATION\n(female rooms reserved)", fg='#410200',  bg=sections_bg_colors,
                                          anchor='center', font='-family {Times New Roman} -size 8 -weight bold')
female_room_reservation_lable1.place(relwidth=0.6, relheight=1)
female_room_reservation_lable2 = tk.Label(female_room_reservation_frame,
                                          text=f"total_number_of_female__rooms_reserved", anchor='center',  bg=sections_bg_colors,
                                          fg='#704214',
                                          font='-family {Courier New} -size 15 -weight bold -slant italic')
female_room_reservation_lable2.place(relx=0.6, relwidth=0.4, relheight=1)

total_staff_frame = tk.Frame(Hostel_Status_frame,  bg=sections_bg_colors,)
total_staff_frame.place(relx=0.77, rely=0.1, relwidth=0.21, relheight=0.06)
total_staff_lable1 = tk.Label(total_staff_frame, text="TOTAL STAFF\n(number of staff employed)", anchor='center', fg=sections_fg_colors, bg=sections_bg_colors,
                              font='-family {Times New Roman} -size 8 -weight bold')
total_staff_lable1.place(relwidth=0.6, relheight=1)
total_staff_lable2 = tk.Label(total_staff_frame, text=f"total_staff", anchor='center', fg='#704214', bg=sections_bg_colors,
                              font='-family {Courier New} -size 15 -weight bold -slant italic')
total_staff_lable2.place(relx=0.6, relwidth=0.4, relheight=1)

blank_frame = tk.Frame(Hostel_Status_frame,  bg=sections_bg_colors,)
blank_frame.place(relx=0.77, rely=0.2, relwidth=0.21, relheight=0.06)
blank_lable1 = tk.Label(blank_frame, text="blank\n()", anchor='center', fg=sections_fg_colors, bg=sections_bg_colors,
                        font='-family {Times New Roman} -size 8 -weight bold')
blank_lable1.place(relwidth=0.6, relheight=1)
blank_lable2 = tk.Label(blank_frame, fg='blue', text="1000", anchor='center', bg=sections_bg_colors,
                        font='-family {Courier New} -size 10 -weight bold')
blank_lable2.place(relx=0.6, relwidth=0.4, relheight=1)

blank1_frame = tk.Frame(Hostel_Status_frame,  bg=sections_bg_colors,)
blank1_frame.place(relx=0.77, rely=0.3, relwidth=0.21, relheight=0.06)
blank1_lable1 = tk.Label(blank1_frame, text="blank\n()", anchor='center', fg=sections_fg_colors, bg=sections_bg_colors,
                         font='-family {Times New Roman} -size 8 -weight bold')
blank1_lable1.place(relwidth=0.6, relheight=1)
blank1_lable2 = tk.Label(blank1_frame, text="1000", anchor='center', fg='#704214',  bg=sections_bg_colors,
                         font='-family {Courier New} -size 15 -weight bold -slant italic')
blank1_lable2.place(relx=0.6, relwidth=0.4, relheight=1)

blank1_frame = tk.Frame(Hostel_Status_frame,  bg=sections_bg_colors,)
blank1_frame.place(relx=0.77, rely=0.4, relwidth=0.21, relheight=0.06)
blank1_lable1 = tk.Label(blank1_frame, text="blank\n()", anchor='center', fg=sections_fg_colors, bg=sections_bg_colors,
                         font='-family {Times New Roman} -size 8 -weight bold')
blank1_lable1.place(relwidth=0.6, relheight=1)
blank1_lable2 = tk.Label(blank1_frame, fg='blue', text="1000", anchor='center', bg=sections_bg_colors,
                         font='-family {Courier New} -size 10 -weight bold')
blank1_lable2.place(relx=0.6, relwidth=0.4, relheight=1)

# ----------------------------RESERVE FRAME-----------------------------------------------------------------------------
Reserve_Room_frame = tk.Frame(root,  bg=sections_bg_colors,)
Reserve_Room_frame.place(relx=0.173, rely=0, relwidth=0.83, relheight=1)

student_first_name = tk.StringVar()
student_second_name = tk.StringVar()
student_last_name = tk.StringVar()
student_gender = tk.StringVar()
student_phone_number = tk.IntVar()
student_email = tk.StringVar()
institution = tk.StringVar()
year_of_study = tk.IntVar()
student_natinal_id = tk.IntVar()

parent_first_name = tk.StringVar()
parent_second_name = tk.StringVar()
parent_phone_no = tk.IntVar()
parent_email = tk.StringVar()

room_type = tk.StringVar()

title_lable1 = tk.Label(Reserve_Room_frame, text="Student Personal Information *", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                        font='-family {Georgia} -size 14 -weight bold')
title_lable1.place(relx=0.05, rely=0.1, relwidth=0.31, relheight=0.04)

first_name_lable = tk.Label(Reserve_Room_frame, text="First Name", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                            font='-family {Georgia} -size 12 -weight bold')
first_name_lable.place(relx=0.05, rely=0.15, relwidth=0.1, relheight=0.04)

first_name_entry = tk.Entry(Reserve_Room_frame, textvariable=student_first_name, font='-family {Consolas} -size 12 ',
                            bg='#F0EAD2', fg='blue')
first_name_entry.place(relx=0.16, rely=0.15, relwidth=0.2, relheight=0.04)
changeOnHover(first_name_entry, '#D0F0C0', "#F0EAD2")

Second_name_lable = tk.Label(Reserve_Room_frame, text="Second Name", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                             font='-family {Georgia} -size 10 -weight bold')
Second_name_lable.place(relx=0.05, rely=0.2, relwidth=0.1, relheight=0.04)
Second_name_entry = tk.Entry(Reserve_Room_frame, textvariable=student_second_name, font='-family {Consolas} -size 12 ',
                             bg='#F0EAD2', fg='blue')
Second_name_entry.place(relx=0.16, rely=0.2, relwidth=0.2, relheight=0.04)
changeOnHover(Second_name_entry, '#D0F0C0', "#F0EAD2")

Last_name_lable = tk.Label(Reserve_Room_frame, text="Last Name", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                           font='-family {Georgia} -size 10 -weight bold')
Last_name_lable.place(relx=0.05, rely=0.25, relwidth=0.1, relheight=0.04)
Last_name_entry = tk.Entry(Reserve_Room_frame, textvariable=student_last_name, font='-family {Consolas} -size 12 ',
                           bg='#F0EAD2', fg='blue')
Last_name_entry.place(relx=0.16, rely=0.25, relwidth=0.2, relheight=0.04)
changeOnHover(Last_name_entry, '#D0F0C0', "#F0EAD2")

Date_of_birth_lable = tk.Label(Reserve_Room_frame, text="Date Of Birth", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                               font='-family {Georgia} -size 10 -weight bold')
Date_of_birth_lable.place(relx=0.05, rely=0.3, relwidth=0.1, relheight=0.04)
cal_date_of_birth = DateEntry(Reserve_Room_frame, bg='#004953')
cal_date_of_birth.place(relx=0.16, rely=0.3, relwidth=0.2, relheight=0.04)
changeOnHover(cal_date_of_birth, '#4B5320', "#004953")

Gender_lable = tk.Label(Reserve_Room_frame, text="Gender", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                        font='-family {Georgia} -size 10 -weight bold')
Gender_lable.place(relx=0.05, rely=0.35, relwidth=0.1, relheight=0.04)
Gender_entry = tk.Entry(Reserve_Room_frame, textvariable=student_gender, font='-family {Consolas} -size 12 ',
                        bg='#F0EAD2', fg='blue')
Gender_entry.place(relx=0.16, rely=0.35, relwidth=0.2, relheight=0.04)
changeOnHover(Gender_entry, '#D0F0C0', "#F0EAD2")

Phone_no_lable = tk.Label(Reserve_Room_frame, text="Phone NO ", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                          font='-family {Georgia} -size 10 -weight bold')
Phone_no_lable.place(relx=0.05, rely=0.4, relwidth=0.1, relheight=0.04)
Phone_no_entry = tk.Entry(Reserve_Room_frame, textvariable=student_phone_number, font='-family {Consolas} -size 12',
                          bg='#F0EAD2', fg='blue')
Phone_no_entry.place(relx=0.16, rely=0.4, relwidth=0.2, relheight=0.04)
changeOnHover(Phone_no_entry, '#D0F0C0', "#F0EAD2")

email_lable = tk.Label(Reserve_Room_frame, text="Email Address ", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                       font='-family {Georgia} -size 10 -weight bold')
email_lable.place(relx=0.05, rely=0.45, relwidth=0.1, relheight=0.04)
email_entry = tk.Entry(Reserve_Room_frame, textvariable=student_email, font='-family {Consolas} -size 12 ',
                       bg='#F0EAD2', fg='blue')
email_entry.place(relx=0.16, rely=0.45, relwidth=0.2, relheight=0.04)
changeOnHover(email_entry, '#D0F0C0', "#F0EAD2")

institution_lable = tk.Label(Reserve_Room_frame, text="Institution ", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                             font='-family {Georgia} -size 10 -weight bold')
institution_lable.place(relx=0.05, rely=0.5, relwidth=0.1, relheight=0.04)
institution_entry = tk.Entry(Reserve_Room_frame, textvariable=institution, font='-family {Consolas} -size 12 ',
                             bg='#F0EAD2', fg='blue')
institution_entry.place(relx=0.16, rely=0.5, relwidth=0.2, relheight=0.04)
changeOnHover(institution_entry, '#D0F0C0', "#F0EAD2")

Year_of_study_lable = tk.Label(Reserve_Room_frame, text="Year Of Study ", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                               font='-family {Georgia} -size 10 -weight bold')
Year_of_study_lable.place(relx=0.05, rely=0.55, relwidth=0.1, relheight=0.04)
Year_of_study_entry = tk.Entry(Reserve_Room_frame, textvariable=year_of_study, font='-family {Consolas} -size 12 ',
                               bg='#F0EAD2', fg='blue')
Year_of_study_entry.place(relx=0.16, rely=0.55, relwidth=0.2, relheight=0.04)
changeOnHover(Year_of_study_entry, '#D0F0C0', "#F0EAD2")

National_ID_lable = tk.Label(Reserve_Room_frame, text="National ID No ", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                             font='-family {Georgia} -size 10 -weight bold')
National_ID_lable.place(relx=0.05, rely=0.6, relwidth=0.1, relheight=0.04)
National_ID_entry = tk.Entry(Reserve_Room_frame, textvariable=student_natinal_id, font='-family {Consolas} -size 12 ',
                             bg='#F0EAD2', fg='blue')
National_ID_entry.place(relx=0.16, rely=0.6, relwidth=0.2, relheight=0.04)
changeOnHover(National_ID_entry, '#D0F0C0', "#F0EAD2")

title_lable2 = tk.Label(Reserve_Room_frame, text="Parent Information *", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                        font='-family {Georgia} -size 14 -weight bold')
title_lable2.place(relx=0.45, rely=0.1, relwidth=0.31, relheight=0.04)

Parent_first_name_lable = tk.Label(Reserve_Room_frame, text="First Name", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                                   font='-family {Georgia} -size 12 -weight bold')
Parent_first_name_lable.place(relx=0.45, rely=0.15, relwidth=0.1, relheight=0.04)
Parent_first_name_entry = tk.Entry(Reserve_Room_frame, textvariable=parent_first_name,
                                   font='-family {Consolas} -size 12 ', bg='#F0EAD2', fg='blue')
Parent_first_name_entry.place(relx=0.56, rely=0.15, relwidth=0.2, relheight=0.04)
changeOnHover(Parent_first_name_entry, '#D0F0C0', "#F0EAD2")

Parent_second_name_lable = tk.Label(Reserve_Room_frame, text="Second Name", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                                    font='-family {Georgia} -size 10 -weight bold')
Parent_second_name_lable.place(relx=0.45, rely=0.2, relwidth=0.1, relheight=0.04)
Parent_second_name_entry = tk.Entry(Reserve_Room_frame, textvariable=parent_second_name,
                                    font='-family {Consolas} -size 12 ', bg='#F0EAD2', fg='blue')
Parent_second_name_entry.place(relx=0.56, rely=0.2, relwidth=0.2, relheight=0.04)
changeOnHover(Parent_second_name_entry, '#D0F0C0', "#F0EAD2")

Parent_Phone_no_lable = tk.Label(Reserve_Room_frame, text="Phone Name", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                                 font='-family {Georgia} -size 10 -weight bold')
Parent_Phone_no_lable.place(relx=0.45, rely=0.25, relwidth=0.1, relheight=0.04)
Parent_Phone_no_entry = tk.Entry(Reserve_Room_frame, textvariable=parent_phone_no, font='-family {Consolas} -size 12 ',
                                 bg='#F0EAD2', fg='blue')
Parent_Phone_no_entry.place(relx=0.56, rely=0.25, relwidth=0.2, relheight=0.04)
changeOnHover(Parent_Phone_no_entry, '#D0F0C0', "#F0EAD2")

Parent_Email_lable = tk.Label(Reserve_Room_frame, text="Email Name", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                              font='-family {Georgia} -size 10 -weight bold')
Parent_Email_lable.place(relx=0.45, rely=0.3, relwidth=0.1, relheight=0.04)
Parent_Email_name_entry = tk.Entry(Reserve_Room_frame, textvariable=parent_email, font='-family {Consolas} -size 12 ',
                                   bg='#F0EAD2', fg='blue')
Parent_Email_name_entry.place(relx=0.56, rely=0.3, relwidth=0.2, relheight=0.04)
changeOnHover(Parent_Email_name_entry, '#D0F0C0', "#F0EAD2")

title_lable3 = tk.Label(Reserve_Room_frame, text="Reserve Room *", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                        font='-family {Georgia}  -size 14 -weight bold')
title_lable3.place(relx=0.45, rely=0.36, relwidth=0.31, relheight=0.04)
Room_Type_lable = tk.Label(Reserve_Room_frame, text="ROOM TYPE", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                           font='-family {Georgia} -size 10 -weight bold')
Room_Type_lable.place(relx=0.45, rely=0.41, relwidth=0.1, relheight=0.04)
tk.Radiobutton(Reserve_Room_frame, text='Twin Room', width=25, value='Twin Room', fg=sections_fg_colors, bg=sections_bg_colors, variable=room_type, anchor='w').place(
    relx=0.56, rely=0.41, relwidth=0.09, relheight=0.04)
tk.Radiobutton(Reserve_Room_frame, text='Single Room', width=25, value='Single Room', fg=sections_fg_colors, bg=sections_bg_colors, variable=room_type, anchor='w').place(
    relx=0.645, rely=0.41, relwidth=0.09, relheight=0.04)
tk.Radiobutton(Reserve_Room_frame, text='Premium Room', width=25, value='Premium Room', fg=sections_fg_colors, bg=sections_bg_colors, variable=room_type,
               anchor='w').place(relx=0.73, rely=0.41, relwidth=0.1, relheight=0.04)
changeOnHover(first_name_entry, '#D0F0C0', "#F0EAD2")

Room_no_lable = tk.Label(Reserve_Room_frame, text="ROOM NUMBER", anchor='w', borderwidth=0, fg=sections_fg_colors, bg=sections_bg_colors,
                         font='-family {Georgia} -size 10 -weight bold')
Room_no_lable.place(relx=0.45, rely=0.46, relwidth=0.1, relheight=0.04)
Room_no_entry = tk.Label(Reserve_Room_frame, text='room', font='-family {Consolas} -size 12 ', anchor='w', fg=sections_fg_colors, bg=sections_bg_colors,)
Room_no_entry.place(relx=0.56, rely=0.46, relwidth=0.2, relheight=0.04)
changeOnHover(first_name_entry, '#D0F0C0', "#F0EAD2")


def Clear_reservation():
    first_name_entry.delete(0, tk.END)
    Second_name_entry.delete(0, tk.END)
    cal_date_of_birth.delete(0, tk.END)
    Gender_entry.delete(0, tk.END)
    Phone_no_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    Year_of_study_entry.delete(0, tk.END)
    National_ID_entry.delete(0, tk.END)
    Parent_first_name_entry.delete(0, tk.END)
    Parent_second_name_entry.delete(0, tk.END)
    Parent_Phone_no_entry.delete(0, tk.END)
    Parent_Email_name_entry.delete(0, tk.END)
    Room_no_entry.config(text="number")


save_reservation = tk.Button(Reserve_Room_frame, text="SAVE", activebackground="Green", activeforeground="white",
                             bg='#937A62', borderwidth=1, font='-family {Courier New}  -size 10 -weight bold',
                             command=lambda: reserve_room(student_first_name.get(), student_second_name.get(),
                                                          student_last_name.get(), cal_date_of_birth.get_date(),
                                                          student_gender.get(), int(student_phone_number.get()),
                                                          student_email.get(), year_of_study.get(), institution.get(),
                                                          student_natinal_id.get(), parent_first_name.get(),
                                                          parent_second_name.get(), int(parent_phone_no.get()),
                                                          parent_email.get(), room_type.get()))
save_reservation.place(relx=0.5, rely=0.9, relwidth=0.09, relheight=0.037)

Cancel_reservation = tk.Button(Reserve_Room_frame, text="CANCEL", activebackground="Red", activeforeground="white",
                               bg='#937A62', borderwidth=1, font='-family {Courier New}  -size 10 -weight bold',
                               command=Clear_reservation)
Cancel_reservation.place(relx=0.6, rely=0.9, relwidth=0.09, relheight=0.037)
changeOnHover(save_reservation, '#D0F0C0', "#937A62")
changeOnHover(Cancel_reservation, '#D0F0C0', "#937A62")

from tkinter import messagebox
from datetime import date as ty
import re
import random


def reserve_room(f_name, s_name, l_name, d_birth, s_gender, s_phone, s_email, year_study, s_institution, s_national_is, p_first_name, p_second_name, p_phone_no, p_email, room_ty):
    if f_name == '':
        stut1 = tk.Label(Reserve_Room_frame, text='✗ Error:\n\n Student First Name Field is Empty', bg='#BA0021', fg='white', font='-family {Georgia}  -size 10 -slant italic')
        stut1.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
        stut1.after(3100, lambda: stut1.place_forget())
        return
    if s_name == '':
        stut1 = tk.Label(Reserve_Room_frame, text='✗ Error:\n\n Student Second Name Field is Empty', bg='#BA0021', fg='white', font='-family {Georgia}  -size 10 -slant italic')
        stut1.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
        stut1.after(3100, lambda: stut1.place_forget())
        return
    if l_name == '':
        stut1 = tk.Label(Reserve_Room_frame, text='✗ Error:\n\n Last First Name Field is Empty', bg='#BA0021', fg='white', font='-family {Georgia}  -size 10 -slant italic')
        stut1.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
        stut1.after(3100, lambda: stut1.place_forget())
        return

    if s_gender != '':
        if s_gender == 'male' or s_gender == 'Male':
            s_gender = 'Male'

        elif s_gender == 'female' or s_gender == 'Female':
            s_gender = 'Female'

        elif (s_gender != 'female') or (s_gender != 'Female') or (s_gender != 'male') or (s_gender != 'Male'):
            messagebox.showwarning("ERROR", "Gender Specification either male or female")
            gender_error = tk.Label(Reserve_Room_frame, text='✗ ERROR:\n\n Student Gender !', bg='#BA0021', fg='white',  font='-family {Georgia}  -size 10 -slant italic')
            gender_error.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
            gender_error.after(3100, lambda: gender_error.place_forget())
            return

    if s_phone == 0:
        s_phone_error = tk.Label(Reserve_Room_frame, text='✗ ERROR:\n\n Student Phone Number', bg='#BA0021', fg='white',  font='-family {Georgia}  -size 10 -slant italic')
        s_phone_error.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
        s_phone_error.after(3100, lambda: s_phone_error.place_forget())
        return

    if s_email != '':
            print('valid s email')
    else:
        messagebox.showwarning("ERROR", "No Email Provided")
        s_email_error = tk.Label(Reserve_Room_frame, text='✗ Error:\n\n No Student Email Provided', bg='#BA0021', fg='white', font='-family {Georgia}  -size 10 -slant italic')
        s_email_error.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
        s_email_error.after(3100, lambda: s_email_error.place_forget())
        return

    sssdtoday = ty.today()
    db = abs((d_birth - sssdtoday).days)
    age = db / 365
    if d_birth != sssdtoday:
        if d_birth > sssdtoday:
            d_birth_error = tk.Label(Reserve_Room_frame, text='✗ Error:\n\n Date of Birth Erro', bg='#BA0021', fg='white',  font='-family {Georgia}  -size 10 -slant italic')
            d_birth_error.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
            d_birth_error.after(3100, lambda: d_birth_error.place_forget())
            return
        if age < 17:
            print(age)
            age_error = tk.Label(Reserve_Room_frame, text='✗ Error:\n\n Age is Less Than 17', bg='#BA0021', fg='white', font='-family {Georgia}  -size 10 -slant italic')
            age_error.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
            age_error.after(3100, lambda: age_error.place_forget())
            return
    else:
        stut1 = tk.Label(Reserve_Room_frame, text='✗ Error:\n\n Select Age', bg='#BA0021', fg='white', font='-family {Georgia}  -size 10 -slant italic')
        stut1.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
        stut1.after(3100, lambda: stut1.place_forget())
        return

    if year_study <= 0 or year_study >= 7:
        year_study_error = tk.Label(Reserve_Room_frame, text='✗ Error:\n\n Invalid Year Of Study', bg='#BA0021', fg='white',  font='-family {Georgia}  -size 10 -slant italic')
        year_study_error.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
        year_study_error.after(3100, lambda: year_study_error.place_forget())
        return

    if s_institution == '':
        s_institution_error = tk.Label(Reserve_Room_frame, text='✗ Error:\n\n Please Fill Student Institution Name', bg='#BA0021',   fg='white', font='-family {Georgia}  -size 10 -slant italic')
        s_institution_error.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
        s_institution_error.after(3100, lambda: s_institution_error.place_forget())
        return

    if s_national_is == 0:
        s_national_is_error = tk.Label(Reserve_Room_frame, text='✗ Error:\n\n National ID field is empty', bg='#BA0021', fg='white', font='-family {Georgia}  -size 10 -slant italic')
        s_national_is_error.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
        s_national_is_error.after(3100, lambda: s_national_is_error.place_forget())
        return

    if p_first_name == '':
        p_first_name_error = tk.Label(Reserve_Room_frame, text='✗ Error:\n\n Parent First Name Field is Empty', bg='#BA0021', fg='white', font='-family {Georgia}  -size 10 -slant italic')
        p_first_name_error.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
        p_first_name_error.after(3100, lambda: p_first_name_error.place_forget())
        return
    if p_second_name == '':
        p_second_name_error = tk.Label(Reserve_Room_frame, text='✗ Error:\n\n Parent Second Name Field is Empty', bg='#BA0021', fg='white', font='-family {Georgia}  -size 10 -slant italic')
        p_second_name_error.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
        p_second_name_error.after(3100, lambda: p_second_name_error.place_forget())
        return

    if p_email != '':
            pass

    else:
        p_email_error = tk.Label(Reserve_Room_frame, text='✗ Error:\n\n No Parent Email Provided', bg='#BA0021', fg='white', font='-family {Georgia}  -size 10 -slant italic')
        p_email_error.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
        p_email_error.after(3100, lambda: p_email_error.place_forget())
        return

    if p_phone_no == 0:
        p_phone_no_error = tk.Label(Reserve_Room_frame, text='✗ Error:\n\n Parent Phone Number', bg='#BA0021', fg='white', font='-family {Georgia}  -size 10 -slant italic')
        p_phone_no_error.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
        p_phone_no_error.after(3100, lambda: p_phone_no_error.place_forget())
        return

    mycursor.execute( "SELECT * FROM hostel.student where  first_name = %s and second_name =  %s and last_name = %s and gender = %s and phone_no = %s and email_id = %s;", (f_name, s_name, l_name, s_gender, s_phone, s_email))
    check_inf = mycursor.fetchall()
    print("Existing data", check_inf , len(check_inf) )
    if len(check_inf) == 0:
        print("accepted")
        mycursor.execute("SELECT * FROM hostel.room where room_type = %s and room_status='not occupied' and room_condition = 'good'", [room_ty])
        r_output = mycursor.fetchall()
        print(room_ty)
        print("rooms", r_output)
        if r_output != []:
            room_number = r_output[0][2]
            room_id = r_output[0][0]
            mycursor.execute("UPDATE hostel.room SET room_status = 'occupied' WHERE  room_number = %s", [room_number])
            mydb.commit()

            user_name = f_name + str(random.randrange(50, 1000))
            pass_word = s_name + str(random.randrange(50, 1000))
            mycursor.execute("INSERT INTO hostel.users (user_name, user_passwd, user_role) VALUES (%s, %s, %s);",(user_name, pass_word, 'student'))
            mydb.commit()
            mycursor.execute("SELECT * FROM hostel.users where user_name = %s and user_passwd = %s and user_role= %s;", (user_name, pass_word, 'student'))
            user_det = mycursor.fetchall()
            newUser_id = user_det[0][2]
            spr = "INSERT INTO hostel.student(first_name, second_name, last_name, date_of_birth, gender, phone_no, email_id, year_of_study, institution, national_id, user_id,  room_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            var = (f_name, s_name, l_name, d_birth, s_gender, s_phone, s_email, year_study, s_institution, s_national_is, newUser_id, room_id)
            mycursor.execute(spr, var)
            mydb.commit()

            mycursor.execute('SELECT * FROM hostel.student where first_name = %s and second_name = %s and last_name = %s and date_of_birth = %s and gender = %s;',(f_name, s_name, l_name, d_birth, s_gender))
            student_id = mycursor.fetchall()

            spr1 = "INSERT INTO hostel.parent_info (First_name, Second_name, Phone_number, Email_Address, student_id) VALUES (%s, %s, %s, %s, %s);"
            var1 = (p_first_name, p_second_name, p_phone_no, p_email, student_id[0][0])
            mycursor.execute(spr1, var1)
            mydb.commit()

            Room_no_entry.config(text=f"{room_number}")

            Reserved_success = tk.Label(Reserve_Room_frame, text='✔ Successfuly Reserved', bg='green', fg='#6B4423', font='-family {Georgia}  -size 14 -slant italic')
            Reserved_success.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.07)
            Reserved_success.after(4100, lambda: Reserved_success.place_forget())

            show_password = tk.Label(Reserve_Room_frame, text=f"USER DEFAULT USERNAME: {user_name} \nUSER DEFAULT PASSWORD: {pass_word}", fg='green',  anchor='w', borderwidth=0, font='-family {Georgia} -size 10 -weight bold')
            show_password.place(relx=0.45, rely=0.52, relwidth=0.4, relheight=0.09)
            show_password.after(70000, lambda: Reserved_success.destroy())




            try:
                    sender_add = 'hostelmanagmentq@gmail.com'
                    receiver_add = s_email
                    password = 'hostel123'

                    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
                    smtp_server.ehlo()
                    smtp_server.starttls()
                    smtp_server.ehlo()
                    smtp_server.login(sender_add, password)
                    msg_to_be_sent = f'''
                                    Hello {s_name} {l_name},
                                    
                                             Hope you are doing well.
                                             Welcome to Students Apartments (Hostels)!
                                             your login Cridential are :
                                                       USERNAME : {user_name}
                                                       PASSWORD : {pass_word}
                                              you can login and change your password and upload your profile
                                    My name is Nangulu Hezron, and welcome to the Qwetu community.
                                    regards
                                    '''
                    # sending the mail by specifying the from and to address and the message
                    smtp_server.sendmail(sender_add, receiver_add, msg_to_be_sent)
                    print('Successfully the mail is sent')
                    smtp_server.quit()

                    ChecK_conform = tk.Label(Reserve_Room_frame, text='✔ ChecK Your Email For Password', bg='green', fg='#6B4423', font='-family {Georgia}  -size 14 -slant italic')
                    ChecK_conform.place(relx=0.7, rely=0.08, relwidth=0.25, relheight=0.07)
                    ChecK_conform.after(4100, lambda: ChecK_conform.place_forget())
            except:
                    Email_error = tk.Label(Reserve_Room_frame, text=' Email Not sent', bg='green', fg='#6B4423', font='-family {Georgia}  -size 14 -slant italic')
                    Email_error.place(relx=0.7, rely=0.18, relwidth=0.25, relheight=0.07)
                    Email_error.after(4100, lambda: Email_error.place_forget())
        else:
            No_avaliable_rooms_errors = tk.Label(Reserve_Room_frame, text='No avaliable rooms\nall rooms are occupied ', bg='red', fg='#6B4423', font='-family {Georgia}  -size 8 -slant italic')
            No_avaliable_rooms_errors.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.07)
            No_avaliable_rooms_errors.after(3000, lambda: No_avaliable_rooms_errors.place_forget())
    else:
        student_already_error = tk.Label(Reserve_Room_frame, text=' ERROR \n Student already in the database', bg='red', fg='#6B4423', font='-family {Georgia}  -size 8 -slant italic')
        student_already_error.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.07)
        student_already_error.after(3000, lambda: student_already_error.place_forget())


# ====================================  Deallocate FRAME ======================================================================

Deallocate_frame = tk.Frame(root, bg=sections_bg_colors,)
Deallocate_frame.place(relx=0.173, rely=0, relwidth=0.83, relheight=1)
section_1_deall = tk.Frame(Deallocate_frame, bg=sections_bg_colors,)
section_1_deall.place(relx=0.001, rely=0.001, relwidth=0.998, relheight=0.1)
def Search_del_student(room_num, student_name):

        mycursor.execute('SELECT * FROM hostel.student WHERE first_name = %s OR second_name = %s OR last_name = %s;', [student_name,student_name,student_name])
        deloc_s = mycursor.fetchall()
        if deloc_s == []:
            de_conf = tk.Label(Deallocate_frame, bg='yellow', text=' ! SOORY ! \nStudent Name Not IN the System', font='-family {Courier New}  -size 10 -weight bold')
            de_conf.place(relx=0.25, rely=0.4, relwidth=0.4, relheight=0.1)
            de_conf.after(4000, lambda: de_conf.place_forget())
            return
        room_id_del = deloc_s[0][12]
        mycursor.execute('SELECT * FROM hostel.room WHERE room_id = %s;', [room_id_del])
        deloc_r = mycursor.fetchall()
        mycursor.execute('SELECT * FROM hostel.parent_info WHERE student_id = %s;', [deloc_s[0][0]])
        deloc_par = mycursor.fetchall()
        if room_num == deloc_r[0][2]:

                    tk.Label(section_2_deall, fg='red',  bg=sections_bg_colors, text=f'{deloc_s[0][1]} {deloc_s[0][2]} {deloc_s[0][3]}', anchor='w', font='-family {Courier New}  -size 11 -weight bold').place(rely=0.01, relx=0.17, relwidth=0.27, relheight=0.065)
                    tk.Label(section_2_deall, fg='red',  bg=sections_bg_colors, text=f'{deloc_s[0][5]}', anchor='w', font='-family {Courier New}  -size 11 -weight bold').place(rely=0.077, relx=0.17, relwidth=0.27, relheight=0.065)
                    tk.Label(section_2_deall, fg='red',  bg=sections_bg_colors,text=f'{deloc_s[0][4]}', anchor='w', font='-family {Courier New}  -size 11 -weight bold').place(rely=0.144, relx=0.17, relwidth=0.27, relheight=0.065)
                    tk.Label(section_2_deall, fg='red',  bg=sections_bg_colors,text=f'{deloc_s[0][6]}', anchor='w', font='-family {Courier New}  -size 11 -weight bold').place(rely=0.211, relx=0.17, relwidth=0.27, relheight=0.065)
                    tk.Label(section_2_deall, fg='red',  bg=sections_bg_colors,text=f'{deloc_s[0][7]}', anchor='w', font='-family {Courier New}  -size 11 -weight bold').place(rely=0.278, relx=0.17, relwidth=0.27, relheight=0.065)
                    tk.Label(section_2_deall, fg='red',  bg=sections_bg_colors,text=f'{deloc_s[0][9]}', anchor='w', font='-family {Courier New}  -size 11 -weight bold').place(rely=0.345, relx=0.17, relwidth=0.27, relheight=0.065)
                    tk.Label(section_2_deall, fg='red',  bg=sections_bg_colors,text=f'{deloc_s[0][10]}', anchor='w', font='-family {Courier New}  -size 11 -weight bold').place(rely=0.412, relx=0.17, relwidth=0.27, relheight=0.065)
                    tk.Label(section_2_deall, fg='red',  bg=sections_bg_colors,text=f'{deloc_r[0][2]}', anchor='w', font='-family {Courier New}  -size 11 -weight bold').place(rely=0.479, relx=0.17, relwidth=0.27, relheight=0.065)

                    tk.Label(section_2_deall, fg='red',  bg=sections_bg_colors,text=f'{deloc_par[0][0]} {deloc_par[0][1]}', anchor='w', font='-family {Courier New}  -size 11 -weight bold').place(rely=0.01, relx=0.66, relwidth=0.27, relheight=0.065)
                    tk.Label(section_2_deall, fg='red',  bg=sections_bg_colors,text=f'{deloc_par[0][2]}', anchor='w', font='-family {Courier New}  -size 11 -weight bold').place(rely=0.077, relx=0.66, relwidth=0.27, relheight=0.065)
                    tk.Label(section_2_deall, fg='red',  bg=sections_bg_colors,text=f'{deloc_par[0][3]}', anchor='w', font='-family {Courier New}  -size 11 -weight bold').place(rely=0.144, relx=0.66, relwidth=0.27, relheight=0.065)

                    def delete_student_records():
                                def YES():
                                       mycursor.execute('DELETE FROM hostel.student WHERE (student_id = %s);', [deloc_s[0][0]])
                                       mydb.commit()
                                       mycursor.execute('DELETE FROM hostel.parent_info WHERE (student_id = %s);', [deloc_s[0][0]])
                                       mydb.commit()
                                       mycursor.execute('DELETE FROM hostel.users WHERE (user_id = %s);', [deloc_s[0][11]])
                                       mydb.commit()
                                       mycursor.execute('DELETE FROM hostel.complaint WHERE (student_id = %s);', [deloc_s[0][0]])
                                       mydb.commit()
                                       mycursor.execute("UPDATE hostel.room  SET room_status = 'not occupied' WHERE(`room_id` = '100102');", [deloc_s[0][12]])
                                       mydb.commit()
                                def NO():
                                       de_conf.place_forget()

                                de_conf = tk.Frame(Deallocate_frame, bg=side_bar_frame_bg_color)
                                de_conf.place(relx=0.25, rely=0.4, relwidth=0.4, relheight=0.1)
                                tk.Label(de_conf, text='Are you Sure You Want To Dealocate This Student !',bg=side_bar_frame_bg_color,font='-family {Courier New}  -size 10 -weight bold').place(relx=0,rely=0, relwidth=1, relheight=0.3)
                                tk.Label(de_conf, text='! !This Action Is Can not be Reversed! !', bg=side_bar_frame_bg_color, font='-family {Courier New}  -size 10 -weight bold').place(relx=0, rely=0.31, relwidth=1, relheight=0.3)
                                tk.Button(de_conf, text='YES', bg='green' , command=YES).place(relx=0, rely=0.7, relwidth=0.5, relheight=0.3)
                                tk.Button(de_conf, text='NO', bg='red', command=NO).place(relx=0.5, rely=0.7, relwidth=0.5, relheight=0.3)

                    del_bt = tk.Button(section_2_deall, bg='#EFDECD',text='DEALOCATE', font='-family {Agency FB}  -size 11 -weight bold', command= lambda :delete_student_records())
                    del_bt.place(relx=0.4, rely=0.9, relwidth=0.15, relheight=0.05)
                    changeOnHover(del_bt, 'brown', '#EFDECD')

        else:
            de_conf = tk.Label(Deallocate_frame,  bg='pink', text=' ! SOORY ! \nSTUDENT NAME DOSE-NOT MATCH ROOM NUMBER', font='-family {Courier New}  -size 10 -weight bold')
            de_conf.place(relx=0.25, rely=0.4, relwidth=0.4, relheight=0.1)
            de_conf.after(4000, lambda :de_conf.place_forget())




deallocate_room = tk.IntVar()
deallocate_student = tk.StringVar()
tk.Label(section_1_deall,      fg = sections_fg_colors, bg = sections_bg_colors, text='Room NO :', font='-family {Georgia}  -size 11 -weight bold').place(relx=0.1, rely=0.03, relheight=0.3, relwidth=0.14)
tk.Label(section_1_deall,       fg = sections_fg_colors, bg = sections_bg_colors,text='Student Name:', font='-family {Georgia}  -size 11 -weight bold').place(relx=0.1, rely=0.4, relheight=0.3, relwidth=0.14)
tk.Entry(section_1_deall,      fg = sections_fg_colors, bg = sections_bg_colors, textvariable=deallocate_room, font='-family {Georgia}  -size 11 -weight bold').place(relx=0.26, rely=0.03, relheight=0.3, relwidth=0.2)
tk.Entry(section_1_deall,       fg = sections_fg_colors, bg = sections_bg_colors, textvariable=deallocate_student, font='-family {Georgia}  -size 11 -weight bold').place(relx=0.26, rely=0.4, relheight=0.3, relwidth=0.2)
del_ser = tk.Button(section_1_deall, bg="#EFDECD",text='Search', font='-family {Georgia}  -size 9 -weight bold', borderwidth=0, command= lambda: Search_del_student(deallocate_room.get(), deallocate_student.get()))
del_ser.place(relx=0.3, rely=0.723, relheight=0.27, relwidth=0.1)
changeOnHover(del_ser,'Green', '#EFDECD')
section_2_deall = tk.LabelFrame(Deallocate_frame, fg = sections_fg_colors, bg = sections_bg_colors,)
section_2_deall.place(relx=0.001, rely=0.123, relwidth=0.998, relheight=0.6)
tk.Label(section_2_deall,      fg = sections_fg_colors, bg = sections_bg_colors,text='Student Name:', anchor='e', font='-family {Cambria}  -size 11 -weight bold').place(rely=0.01, relx=0.01, relwidth=0.15, relheight=0.065)
tk.Label(section_2_deall,      fg = sections_fg_colors, bg = sections_bg_colors,text='Gender:', anchor='e', font='-family {Cambria}  -size 11 -weight bold').place(rely=0.077, relx=0.01, relwidth=0.15, relheight=0.065)
tk.Label(section_2_deall,      fg = sections_fg_colors, bg = sections_bg_colors,text='Date Of Birth:', anchor='e', font='-family {Cambria}  -size 11 -weight bold').place(rely=0.144, relx=0.01, relwidth=0.15, relheight=0.065)
tk.Label(section_2_deall,      fg = sections_fg_colors, bg = sections_bg_colors,text='Phone No:', anchor='e', font='-family {Cambria}  -size 11 -weight bold').place(rely=0.211, relx=0.01, relwidth=0.15, relheight=0.065)
tk.Label(section_2_deall,      fg = sections_fg_colors, bg = sections_bg_colors,text='Email ID:', anchor='e', font='-family {Cambria}  -size 11 -weight bold').place(rely=0.278, relx=0.01, relwidth=0.15, relheight=0.065)
tk.Label(section_2_deall,      fg = sections_fg_colors, bg = sections_bg_colors,text='Institution:', anchor='e', font='-family {Cambria}  -size 11 -weight bold').place(rely=0.345, relx=0.01, relwidth=0.15, relheight=0.065)
tk.Label(section_2_deall,      fg = sections_fg_colors, bg = sections_bg_colors,text='National ID:', anchor='e', font='-family {Cambria}  -size 11 -weight bold').place(rely=0.412, relx=0.01, relwidth=0.15, relheight=0.065)
tk.Label(section_2_deall,      fg = sections_fg_colors, bg = sections_bg_colors,text='Room Number:', anchor='e', font='-family {Cambria}  -size 11 -weight bold').place(rely=0.479, relx=0.01, relwidth=0.15, relheight=0.065)
# parent info
tk.Label(section_2_deall,      fg = sections_fg_colors, bg = sections_bg_colors,text='Parent Name:', anchor='e', font='-family {Cambria}  -size 11 -weight bold').place(rely=0.01, relx=0.5, relwidth=0.15, relheight=0.065)
tk.Label(section_2_deall,      fg = sections_fg_colors, bg = sections_bg_colors,text='Parent Phone NO::', anchor='e', font='-family {Cambria}  -size 11 -weight bold').place(rely=0.077, relx=0.5, relwidth=0.15, relheight=0.065)
tk.Label(section_2_deall,      fg = sections_fg_colors, bg = sections_bg_colors,text='Parent Email', anchor='e', font='-family {Cambria}  -size 11 -weight bold').place(rely=0.144, relx=0.5, relwidth=0.15, relheight=0.065)




# ==================================== ROOM FRAME ======================================================================

Rooms_frame = tk.Frame(root,   bg = sections_bg_colors,)
Rooms_frame.place(relx=0.173, rely=0, relwidth=0.83, relheight=1)
room_search = tk.IntVar()


def search(s_number):
    mycursor.execute("SELECT * FROM room where (room_number = %s) ", [s_number])
    output = mycursor.fetchall()
    if output == []:
        print("Room Number Doesn't Exist")
        status.config(text='Room Number Does not Exist', fg='red')
    else:
        room_number = output[0][2]
        room_id = output[0][0]
        room_type = output[0][1]
        room_status = output[0][4]
        room_price = output[0][3]
        room_condition = output[0][5]
        room_beds = output[0][6]
        room_description = output[0][7]

        status.config(text='')
        room_number_lable2.config(text=room_number)
        room_id_lable2.config(text=room_id)
        room_type_lable2.config(text=room_type)
        room_price_lable2.config(text=room_price)
        room_status_lable2.config(text=room_status)
        room_condition_lable2.config(text=room_condition)
        room_total_beds_lable2.config(text=room_beds)
        room_description_lable2.config(text=room_description)


status = tk.Label(Rooms_frame, font='-family {Consolas} -size 9', fg = sections_fg_colors, bg = sections_bg_colors,)
status.place(relx=0.15, rely=0.051, relwidth=0.25, relheight=0.03)
search_label = tk.Label(Rooms_frame, text='ENTER ROOM NO : ', font='-family {Consolas} -size 12', fg = sections_fg_colors, bg = sections_bg_colors,)
search_label.place(relx=0.03, rely=0.08, relheight=0.03)
search_entry = tk.Entry(Rooms_frame, textvariable=room_search, font='-family {Times New Roman} -size 12', bg='#E9D7AB')
search_entry.place(relx=0.16, rely=0.085, relheight=0.026, relwidth=0.15)
changeOnHover(search_entry, '#D0F0C0', '#E9D7AB')
tk.Button(Rooms_frame, text='⌕ SEARCH', borderwidth=2, command=lambda: search(room_search.get())).place(relx=0.32,
                                                                                                     rely=0.084,
                                                                                                        relheight=0.027,
                                                                                                        relwidth=0.0741)

room_number_lable1 = tk.Label(Rooms_frame, text='Room number', font='-family {Times New Roman} -size 12 ',      fg = sections_fg_colors, bg = sections_bg_colors)
room_number_lable1.place(relx=0.03, rely=0.13, relheight=0.03)
room_number_lable2 = tk.Label(Rooms_frame, text='', fg='green', font='-family {Courier New} -size 11 -weight bold', bg = sections_bg_colors)
room_number_lable2.place(relx=0.15, rely=0.13, relheight=0.03)

room_id_lable1 = tk.Label(Rooms_frame, text='Room id ', font='-family {Times New Roman} -size 12 ',    fg = sections_fg_colors, bg = sections_bg_colors)
room_id_lable1.place(relx=0.03, rely=0.18, relheight=0.03)
room_id_lable2 = tk.Label(Rooms_frame, text='', fg='green', font='-family {Courier New} -size 11 -weight bold',   bg = sections_bg_colors)
room_id_lable2.place(relx=0.15, rely=0.18, relheight=0.03)

room_type_lable1 = tk.Label(Rooms_frame, text='Room type ', font='-family {Times New Roman} -size 12 ', fg = sections_fg_colors, bg = sections_bg_colors)
room_type_lable1.place(relx=0.03, rely=0.23, relheight=0.03)
room_type_lable2 = tk.Label(Rooms_frame, text='', fg='green', bg = sections_bg_colors, font='-family {Courier New} -size 11 -weight bold')
room_type_lable2.place(relx=0.15, rely=0.23, relheight=0.03)

room_price_lable1 = tk.Label(Rooms_frame, text='Room price ', fg = sections_fg_colors, bg = sections_bg_colors, font='-family {Times New Roman} -size 12 ')
room_price_lable1.place(relx=0.03, rely=0.28, relheight=0.03)
room_price_lable2 = tk.Label(Rooms_frame, text='', fg='green', bg = sections_bg_colors, font='-family {Courier New} -size 11 -weight bold')
room_price_lable2.place(relx=0.15, rely=0.28, relheight=0.03)

room_status_lable1 = tk.Label(Rooms_frame, text='Room status', fg = sections_fg_colors, bg = sections_bg_colors,font='-family {Times New Roman} -size 12 ')
room_status_lable1.place(relx=0.03, rely=0.33, relheight=0.03)
room_status_lable2 = tk.Label(Rooms_frame, text='', fg='green', bg = sections_bg_colors, font='-family {Courier New} -size 11 -weight bold')
room_status_lable2.place(relx=0.15, rely=0.33, relheight=0.03)

room_condition_lable1 = tk.Label(Rooms_frame, text='Room condition ', fg = sections_fg_colors, bg = sections_bg_colors, font='-family {Times New Roman} -size 12 ')
room_condition_lable1.place(relx=0.03, rely=0.38, relheight=0.03)
room_condition_lable2 = tk.Label(Rooms_frame, text='', fg='green',  bg = sections_bg_colors,font='-family {Courier New} -size 11 -weight bold')
room_condition_lable2.place(relx=0.15, rely=0.38, relheight=0.03)

room_total_beds_lable1 = tk.Label(Rooms_frame, text='total beds', fg = sections_fg_colors, bg = sections_bg_colors,font='-family {Times New Roman} -size 12 ')
room_total_beds_lable1.place(relx=0.03, rely=0.43, relheight=0.03)
room_total_beds_lable2 = tk.Label(Rooms_frame, text='', fg='green',  bg = sections_bg_colors, font='-family {Courier New} -size 11 -weight bold')
room_total_beds_lable2.place(relx=0.15, rely=0.43, relheight=0.03)

room_description_lable1 = tk.Label(Rooms_frame, text='room_description', fg = sections_fg_colors, bg = sections_bg_colors, font='-family {Times New Roman} -size 12 ')
room_description_lable1.place(relx=0.03, rely=0.48, relheight=0.03)
room_description_lable2 = tk.Label(Rooms_frame, text='', fg='green',  bg = sections_bg_colors, font='-family {Courier New} -size 11 -weight bold')
room_description_lable2.place(relx=0.15, rely=0.48)



# --------------------------- REPORTS FRAME ----------------------------------------------------------------------------
Reports_frame = tk.Frame(root, bg = sections_bg_colors,)
Reports_frame.place(relx=0.173, rely=0, relwidth=0.83, relheight=1)

def log_report_gen():
            import webbrowser
            from fpdf import FPDF
            class PDF(FPDF):
                pass

            pdf = PDF('P', 'mm')  # pdf object
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            pdf.set_font('helvetica', 'UB', 16)
            pdf.cell(0, 10, 'HOSTEL  SYSTEM  LOG REPORT ', ln=True, align='C')
            pdf.ln(15)  # line break

            pdf.set_font('times', 'B', 10)
            pdf.cell(20, 8, 'Log ID', border=True)  # Add text (width, height, text, ln=True/False)
            pdf.set_font('courier', 'B', 10)
            pdf.cell(20, 8, 'user ID', border=True)  # Add text (width, height, text, ln=True/False)
            pdf.set_font('courier', 'B', 10)
            pdf.cell(50, 8, 'username', border=True)
            pdf.set_font('courier', 'B', 10)
            pdf.cell(22, 8, 'user_role', border=True)
            pdf.set_font('courier', 'B', 10)
            pdf.cell(25, 8, 'Login_date', border=True)
            pdf.set_font('courier', 'B', 10)
            pdf.cell(35, 8, 'Login_time', border=True)
            pdf.set_font('courier', 'B', 10)
            pdf.cell(35, 8, 'LogOut_time', ln=True, border=True)
            pdf.ln(5)
            mycursor.execute("SELECT * FROM hostel.log_rept where user_id = 12;")
            log_u_out = mycursor.fetchall()
            print(len(log_u_out))
            i = len(log_u_out)-1
            while i >= 0:
                pdf.set_font('times', '', 10)
                pdf.cell(20, 8, f'{log_u_out[i][0]}', border=True)  # Add text (width, height, text, ln=True/False)
                pdf.set_font('courier', '', 10)
                pdf.cell(20, 8, f'{log_u_out[i][1]}', border=True)
                pdf.set_font('courier', '', 10)
                pdf.cell(50, 8, f'{log_u_out[i][2]}', border=True)
                pdf.set_font('courier', '', 10)
                pdf.cell(20, 8, f'{log_u_out[i][3]}', border=True)
                pdf.set_font('courier', '', 10)
                pdf.cell(30, 8, f'{log_u_out[i][4]}', border=True)
                pdf.set_font('courier', '', 10)
                pdf.cell(30, 8, f'{log_u_out[i][5]}', border=True)
                pdf.set_font('courier', '', 10)
                pdf.cell(30, 8, f'{log_u_out[i][6]}', ln=True, border=True)
                i = i - 1

            pdf_file_name = 'hostel_log_report.pdf'
            pdf.output(pdf_file_name)
            webbrowser.get('windows-default').open(pdf_file_name)

log_bt_repot = tk.Button(Reports_frame, text='LOG REPORT', borderwidth=0, fg = sections_fg_colors,  bg=side_bar_frame_bg_button_color, command=log_report_gen)
log_bt_repot.place(relx=0.1, rely=0.3, relheight=0.05, relwidth=0.15)
changeOnHover(log_bt_repot, '#8A9A5B', side_bar_frame_bg_button_color)


def room_report_gen():
                datei = ty.today()
                import webbrowser
                from fpdf import FPDF
                class PDF(FPDF):
                     pass

                pdf = PDF('P', 'mm')  # pdf object
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()

                pdf.set_font('helvetica', 'UB', 16)
                pdf.cell(0, 10, 'ROOM REPORT', ln=True, align='C')
                pdf.ln(15)  # line break

                pdf.set_font('times', 'B', 10)
                pdf.cell(150, 8, f'Printed On: {datei}', ln=True)

                mycursor.execute("SELECT * FROM hostel.room;")
                log_u_out = mycursor.fetchall()
                i = len(log_u_out)-1
                while i >= 0 :

                        pdf.set_font('times', 'B', 10)
                        pdf.cell(40, 8, 'room_id', border=True)                 # Add text (width, height, text, ln=True/False)
                        pdf.cell(40, 8, f'{log_u_out[0][0]} ', ln=True, border=True)
                        pdf.set_font('courier', 'B', 10)
                        pdf.cell(40, 8, 'room_number', border=True)
                        pdf.cell(40, 8, f'{log_u_out[0][2]} ', ln=True, border=True)
                        pdf.set_font('courier', 'B', 10)
                        pdf.cell(40, 8, 'room_type', border=True)
                        pdf.cell(40, 8, f'{log_u_out[0][1]} ', ln=True, border=True)
                        pdf.set_font('courier', 'B', 10)
                        pdf.cell(40, 8, 'room_price (ksh)',  border=True)
                        pdf.cell(40, 8,  f'{log_u_out[0][3]} ', ln=True, border=True)
                        pdf.set_font('courier', 'B', 10)
                        pdf.cell(40, 8, 'room_status', border=True)
                        pdf.cell(40, 8, f'{log_u_out[0][4]} ', ln=True, border=True)
                        pdf.set_font('courier', 'B', 10)
                        pdf.cell(40, 8, 'room_condition',  border=True)
                        pdf.cell(40, 8, f'{log_u_out[0][5]} ', ln=True, border=True)
                        pdf.set_font('courier', 'B', 10)
                        pdf.cell(40, 8, 'total_beds',  border=True)
                        pdf.cell(40, 8, f'{log_u_out[0][6]} ', ln=True, border=True)
                        pdf.set_font('courier', 'B', 10)
                        pdf.cell(40, 8, 'gender_room_type', border=True)
                        pdf.cell(40, 8, f'{log_u_out[0][8]} ', ln=True, border=True)
                        pdf.ln(5)
                        i = i -1



                pdf_file_name = 'room_report.pdf'
                pdf.output(pdf_file_name)
                webbrowser.get('windows-default').open(pdf_file_name)

room_bt_repot = tk.Button(Reports_frame, text='ROOM REPORT', borderwidth=0, fg = sections_fg_colors,  bg=side_bar_frame_bg_button_color, command=room_report_gen)
room_bt_repot.place(relx=0.1, rely=0.37, relheight=0.05, relwidth=0.15)
changeOnHover(room_bt_repot, '#8A9A5B', side_bar_frame_bg_button_color)






# =========================== COMPLAINTS FRAME =========================================================================
Complaints_frame = tk.Frame(root, bg = sections_bg_colors,)
Complaints_frame.place(relx=0.173, rely=0, relwidth=0.83, relheight=1)

section1 = tk.LabelFrame(Complaints_frame, fg = sections_fg_colors, bg = sections_bg_colors, text="Complants list", font='-family {Georgia} -size 12')
section1.place(relx=0.03, rely=0.04, relwidth=0.94, relheight=0.3)


def utdate(rows):
    for item in tree.get_children():
        tree.delete(item)
    for row in rows:
        tree.insert("", 'end', values=row)


from tkinter import ttk

tree = ttk.Treeview(section1, columns=("c1", "c2", "c3"), show='headings')
tree.column("#1",  anchor=tk.CENTER, width=90, minwidth=50)
tree.heading("#1", text="COMPLAINT ID")
tree.column("#2", anchor=tk.CENTER, width=90, minwidth=50)
tree.heading("#2", text="STUDENT ID")
tree.column("#3", anchor=tk.CENTER, width=90, minwidth=50)
tree.heading("#3", text="COMPLAINT_MESSAGE")
tree.place(relheight=1, relwidth=1)
mycursor.execute("SELECT * FROM hostel.complaint;")
rows = mycursor.fetchall()
utdate(rows)


def clear():
    for item in tree.get_children():
        tree.delete(item)


def refresh_c():
    for row in rows:
        tree.insert("", 'end', values=row)


def search_c(num):
    if num != 0:
        q = num
        mycursor.execute(
            "SELECT complaint_id, student_id, complaint_massage, status FROM hostel.complaint WHERE complaint_id = %s or student_id LIKE %s ;",
            (q, q))
        C_rows = mycursor.fetchall()
        utdate(C_rows)
        if C_rows != []:

            y = 0.1
            j = len(C_rows) - 1
            print(C_rows)
            while j > -1:
                mycursor.execute("SELECT * FROM hostel.student where student_id = %s ;", [C_rows[j][1]])
                S_row = mycursor.fetchall()
                yui = tk.Label(section3,fg = sections_fg_colors,  text=f'C_ID: {C_rows[j][0]}', anchor='w', bg='blue')
                yui.place(relx=0.01, rely=y, relwidth=0.15, relheight=0.06)
                yuw = tk.Label(section3, fg = sections_fg_colors,text=f'ROOM: {C_rows[j][1]}', anchor='w', bg='blue')
                yuw.place(relx=0.161, rely=y, relwidth=0.15, relheight=0.06)
                yur = tk.Label(section3, fg = sections_fg_colors, text=f'S_Name:{S_row[0][1]} {S_row[0][2]} {S_row[0][3]}', anchor='w',
                               bg='blue')
                yur.place(relx=0.312, rely=y, relwidth=0.3, relheight=0.06)
                if C_rows[j][3] == 'pending':
                    uji = tk.Button(section3, text=f'PENDING', bg='GREEN', command=lambda: solve_c(C_rows[j][0]))
                    uji.place(relx=0.614, rely=y, relwidth=0.15, relheight=0.06)
                else:
                    jyt = tk.Button(section3, text=f'SOLVED', bg='blue')
                    jyt.place(relx=0.614, rely=y, relwidth=0.15, relheight=0.06)
                y = y + 0.1
                j = j - 1


def solve_c(num):
    pass


section2 = tk.LabelFrame(Complaints_frame, fg = sections_fg_colors, bg = sections_bg_colors, text="SEARCH", font='-family {Georgia} -size 12')
section2.place(relx=0.03, rely=0.36, relwidth=0.94, relheight=0.06)
tk.Label(section2, text='Search',fg = sections_fg_colors, bg = sections_bg_colors, font='-family {Times New Roman} -size 12 -weight bold').place(relx=0.1, rely=0.1)
complaint_search = tk.IntVar()
tk.Entry(section2, textvariable=complaint_search, fg = sections_fg_colors, bg = sections_bg_colors, font='-family {Times New Roman} -size 12 -weight bold').place(
    relx=0.16, rely=0.11, relwidth=0.17)
tk.Button(section2, text="Search",  fg = sections_fg_colors, bg = sections_bg_colors, font='-family {Times New Roman} -size 10',
          command=lambda: search_c(complaint_search.get())).place(relx=0.35, rely=0.11, relwidth=0.05)
tk.Button(section2, text="Clear", fg = sections_fg_colors, bg = sections_bg_colors, font='-family {Times New Roman} -size 10', command=clear).place(relx=0.42, rely=0.11,
                                                                                                  relwidth=0.05)
tk.Button(section2, text="Show",  fg = sections_fg_colors, bg = sections_bg_colors,font='-family {Times New Roman} -size 10', command=refresh_c).place(relx=0.52,
                                                                                                     rely=0.11,
                                                                                                     relwidth=0.08)

section3 = tk.LabelFrame(Complaints_frame, fg = sections_fg_colors, bg = sections_bg_colors, text="", font='-family {Georgia} -size 12')
section3.place(relx=0.03, rely=0.44, relwidth=0.94, relheight=0.55)

# =========================== NOTICE_BOARD FRAME =======================================================================

Notice_Board_frame = tk.Frame(root, bg = sections_bg_colors,)
Notice_Board_frame.place(relx=0.173, rely=0, relwidth=0.83, relheight=1)

section_n1 = tk.LabelFrame(Notice_Board_frame, fg = sections_fg_colors, bg = sections_bg_colors, text="Message", font='-family {Georgia} -size 11')
section_n1.place(relwidth=0.47, relheight=0.4, relx=0.031, rely=0.041)

section_n2 = tk.LabelFrame(Notice_Board_frame, fg = sections_fg_colors, bg = sections_bg_colors, text="Preview", font='-family {Georgia} -size 11')
section_n2.place(relwidth=0.47, relheight=0.4, relx=0.51, rely=0.041)

text_box_message = tk.Text(section_n1, height=12, fg = sections_fg_colors, bg = sections_bg_colors, width=40, wrap='word')
text_box_message.place(relwidth=1, relheight=1)

text_box_preview = tk.Text(section_n2, height=12,  width=40, fg = sections_fg_colors,  wrap='word', state='disabled', bg='light blue')
text_box_preview.place(relwidth=1, relheight=1)


def pre_view():
    text_box_preview.config(state='normal')
    message = text_box_message.get(1.0, 'end')
    text_box_preview.insert(1.0, message)
    text_box_preview.config(state='disabled')


def post():
    message = text_box_message.get(1.0, 'end')
    mycursor.execute("INSERT INTO `hostel`.`notice_board` (`notice_message`, `date`) VALUES ( %s,  SYSDATE());",
                     [message])
    mydb.commit()


def fetch():
    mycursor.execute("Select * from `hostel`.`notice_board`")
    i = mycursor.fetchall()
    num = 0
    for row in i:
        num + 1
    print(num)


def delete():
    text_box_preview.config(state='normal')
    text_box_preview.delete(1.0, 'end')
    text_box_message.delete(1.0, 'end')
    text_box_preview.config(state='disabled')


tk.Button(Notice_Board_frame, text='PREVIEW',  fg = sections_fg_colors, bg = sections_bg_colors, command=pre_view, activeforeground=sections_fg_colors,
          activebackground='light green', borderwidth=4, font='-family {Consolas} -size 9 -weight bold').place(relx=0.4,
                                                                                                               relwidth=0.07,
                                                                                                               rely=0.452)
tk.Button(Notice_Board_frame, text='POST',  fg = sections_fg_colors, bg = sections_bg_colors, command=post, activeforeground=sections_fg_colors, activebackground='green',
          borderwidth=4, font='-family {Consolas} -size 9 -weight bold').place(relx=0.26, relwidth=0.07, rely=0.452)
tk.Button(Notice_Board_frame, text='CLEAR', fg = sections_fg_colors, bg = sections_bg_colors,  command=delete, activeforeground=sections_fg_colors, activebackground='red',
          borderwidth=4, font='-family {Consolas} -size 9 -weight bold').place(relx=0.56, relwidth=0.07, rely=0.452)

section_n3 = tk.LabelFrame(Notice_Board_frame, text="Search",  fg = sections_fg_colors, bg = sections_bg_colors)
section_n3.place(relx=0.031, relwidth=0.944, relheight=0.06, rely=0.49)
tk.Label(section_n3, text='DATE',  fg = sections_fg_colors, bg = sections_bg_colors, borderwidth=0, font='-family {Georgia} -size 12 -weight bold').place(relx=0.25,
                                                                                                       relwidth=0.1,
                                                                                                       relheight=0.7,
                                                                                                       rely=0)
date = tk.IntVar()


def search_notice():
    for i in tree2.get_children():
        tree2.delete(i)
    date = cal_date.get_date()
    mycursor.execute("SELECT * FROM hostel.notice_board WHERE date = %s;", [date])
    rows = mycursor.fetchall()
    for row in rows:
        tree2.insert("", tk.END, values=row)


cal_date = DateEntry(section_n3, fg = sections_fg_colors, bg = sections_bg_colors,)
cal_date.place(relx=0.36, relwidth=0.25, relheight=0.7, rely=0)
tk.Button(section_n3, text='search',  fg = sections_fg_colors, bg = sections_bg_colors, borderwidth=-4, activebackground='green', foreground='Green',
          font='-family {Consolas} -size 12 -weight bold', command=search_notice).place(relx=0.62, relwidth=0.06,
                                                                                        relheight=0.7, rely=0)

section_n4 = tk.LabelFrame(Notice_Board_frame, fg = sections_fg_colors, bg = sections_bg_colors,)
section_n4.place(relx=0.031, relwidth=0.944, relheight=0.3, rely=0.562)
tree2 = ttk.Treeview(section_n4, columns=("c1", "c2", "c3"), show='headings')
tree2.column("#1", anchor=tk.CENTER, width=90, minwidth=50)
tree2.heading("#1", text="Notice ID")
tree2.column("#2", anchor=tk.CENTER, width=90, minwidth=50)
tree2.heading("#2", text="Massage")
tree2.column("#3", anchor=tk.CENTER, width=90, minwidth=50)
tree2.heading("#3", text="DATE")
tree2.place(relx=0, rely=0, relwidth=1, relheight=1)


def delete_notice():
    mycursor.execute('DELETE FROM hostel.notice_board WHERE notice_id = %s;', [del_id.get()])
    mydb.commit()


def clear_all_notice():
    mycursor.execute('TRUNCATE table notice_board')
    mydb.commit()


section_n5 = tk.LabelFrame(Notice_Board_frame, fg = sections_fg_colors, bg = sections_bg_colors,)
section_n5.place(relx=0.031, relwidth=0.944, relheight=0.1, rely=0.88)
tk.Label(section_n5, fg = sections_fg_colors, bg = sections_bg_colors, text='Notice Id', font='-family {Consolas} -size 10 -weight bold').place(rely=0.3, relheight=0.35,
                                                                                              relwidth=0.1)
del_id = tk.IntVar()
tk.Entry(section_n5, fg = sections_fg_colors, bg = sections_bg_colors,  textvariable=del_id, font='-family {Courier New} -size 10 ').place(relx=0.11, rely=0.3,
                                                                                                  relheight=0.35,
                                                                                                  relwidth=0.1)
tk.Button(section_n5, fg = sections_fg_colors, bg = sections_bg_colors,   text='Del', command=delete_notice).place(relx=0.22, rely=0.3, relheight=0.35, relwidth=0.05)
tk.Button(section_n5,  fg = sections_fg_colors, bg = sections_bg_colors, text='Clear all', command=clear_all_notice).place(relx=0.62, rely=0.3, relheight=0.35,
                                                                        relwidth=0.05)

# =========================== VISITOR LOG FRAME ========================================================================
Visitor_log_frame = tk.Frame(root, bg = sections_bg_colors,)
Visitor_log_frame.place(relx=0.173, rely=0, relwidth=0.83, relheight=1)

section_v1 = tk.LabelFrame(Visitor_log_frame, fg = sections_fg_colors, bg = sections_bg_colors, text='VISITOR LOG',
                           font='-family {Consolas} -size 10 -weight bold')
section_v1.place(relwidth=0.86, relheight=0.51, relx=0.07, rely=0.041)

visitor_log_tree = ttk.Treeview(section_v1, columns=("c1", "c2", "c3", "c4", "c5"), show='headings')
visitor_log_tree.column("#1", anchor=tk.CENTER, width=90, minwidth=50)
visitor_log_tree.heading("#1", text="visitor_name")
visitor_log_tree.column("#2", anchor=tk.CENTER, width=90, minwidth=50)
visitor_log_tree.heading("#2", text="Time_in")
visitor_log_tree.column("#3", anchor=tk.CENTER, width=90, minwidth=50)
visitor_log_tree.heading("#3", text="time_out")
visitor_log_tree.column("#4", anchor=tk.CENTER, width=90, minwidth=50)
visitor_log_tree.heading("#4", text="Date")
visitor_log_tree.column("#5", anchor=tk.CENTER, width=90, minwidth=50)
visitor_log_tree.heading("#5", text="student_id")
visitor_log_tree.place(relx=0, rely=0, relwidth=1, relheight=1)


def visitor():
    mycursor.execute("SELECT * FROM hostel.visitors_log;")
    rows = mycursor.fetchall()
    for row in rows:
        visitor_log_tree.insert("", tk.END, values=row)


visitor()

# =========================== TRANSACTION FRAME ========================================================================

Transaction_frame = tk.Frame(root,  bg = sections_bg_colors,)
Transaction_frame.place(relx=0.173, rely=0, relwidth=0.83, relheight=1)

section_T1 = tk.LabelFrame(Transaction_frame, fg = sections_fg_colors, bg = sections_bg_colors, text='STUDENT TRANSACTION LOG')
section_T1.place(relx=0.025, rely=0.02, relheight=0.3, relwidth=0.95)

Tr_log_tree = ttk.Treeview(section_T1, columns=("c1", "c2", "c3", "c4", "c5", 'c6', 'c7'), show='headings')
Tr_log_tree.column("#1", anchor=tk.CENTER, width=90, minwidth=50)
Tr_log_tree.heading("#1", text="PAYMENT ID")
Tr_log_tree.column("#2", anchor=tk.CENTER, width=90, minwidth=50)
Tr_log_tree.heading("#2", text="STUDENT ID")
Tr_log_tree.column("#3", anchor=tk.CENTER, width=90, minwidth=50)
Tr_log_tree.heading("#3", text="ROOM ID")
Tr_log_tree.column("#4", anchor=tk.CENTER, width=90, minwidth=50)
Tr_log_tree.heading("#4", text="MPESA TRANSACTION ID")
Tr_log_tree.column("#5", anchor=tk.CENTER, width=90, minwidth=50)
Tr_log_tree.heading("#5", text="PAYMENT FOR")
Tr_log_tree.column("#6", anchor=tk.CENTER, width=90, minwidth=50)
Tr_log_tree.heading("#6", text="PAYMENT STATUS")
Tr_log_tree.column("#7", anchor=tk.CENTER, width=90, minwidth=50)
Tr_log_tree.heading("#7", text="TRANSACTION DATE")
Tr_log_tree.place(relx=0, rely=0, relwidth=1, relheight=1)


def Trs_log():
    mycursor.execute("SELECT * FROM hostel.payment;")
    rows = mycursor.fetchall()
    for row in rows:
        Tr_log_tree.insert("", tk.END, values=row)


Trs_log()

section_T2 = tk.Frame(Transaction_frame,  bg = sections_bg_colors,)
section_T2.place(relx=0.025, rely=0.325, relheight=0.65, relwidth=0.95)


def student_trans(num):
    def t_pending(pay_id):
                def confirm_tans():
                    mycursor.execute("UPDATE  hostel.payment set Payment_status ='complete' WHERE Payment_id = %s ;", [pay_id])
                    mydb.commit()
                    ky = tk.Label(yu,  text='transaction confirmed successfully', bg='#FFE4C4', fg='#2E8B57', font='-family {Forte} -size 17')
                    ky.place(relx=0.5, rely=0.5, relwidth=0.5,relheight=0.18)
                    ky.after(4000, lambda : ky.place_forget())

                def reject_tans():
                    mycursor.execute("UPDATE  hostel.payment set Payment_status ='rejected' WHERE Payment_id = %s ;", [pay_id])
                    mydb.commit()
                    ky = tk.Label(yu,  text='transaction rejected successfully', bg='#FFE4C4', fg='red',font='-family {Forte} -size 17')
                    ky.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.18)
                    ky.after(4000, lambda: ky.place_forget())
                def close_f():
                    yu.destroy()

                mycursor.execute("SELECT * FROM hostel.payment WHERE Payment_id = %s;", [pay_id])
                out = mycursor.fetchall()
                mycursor.execute('SELECT * FROM hostel.student where student_id = %s;', [out[0][1]])
                s_detail = mycursor.fetchall()
                yu = tk.Frame(Transaction_frame, bg='#FFE4C4')
                yu.place(relx=0.1, rely=0.2, relwidth=0.85, relheight=0.4)
                tk.Button(yu, text="X", bg='#FFE4C4', activebackground='#FFE4C4', activeforeground='red',borderwidth=0, font='-family {Forte} -size 13', command=close_f).place(relx=0.9, rely=0, relwidth=0.1, relheight=0.07)
                tk.Label(yu, text='Transaction Detail', bg=side_bar_frame_bg_color,font='-family {Georgia} -size 14 -weight bold').place(relx=0, rely=0.07, relheight=0.1, relwidth=1)

                tk.Label(yu, text=f'NAME :', bg='#FFE4C4', anchor='e', font='-family {Cascadia Code} -size 9 -weight bold').place(relx=0.01, rely=0.2, relheight=0.1, relwidth=0.1)
                tk.Label(yu, text=f' {s_detail[0][1]} {s_detail[0][2]} {s_detail[0][3]}', bg='#FFE4C4', anchor='w', font='-family {Georgia} -size 12').place(relx=0.12, rely=0.2, relheight=0.1, relwidth=0.2)

                tk.Label(yu, text=f'STUDENT ID :', bg='#FFE4C4', anchor='e',font='-family {Cascadia Code} -size 9 -weight bold').place(relx=0.35, rely=0.2, relheight=0.1,relwidth=0.1)
                tk.Label(yu, text=f' {s_detail[0][0]}', bg='#FFE4C4', anchor='w', font='-family {Georgia} -size 12').place(relx=0.46, rely=0.2, relheight=0.1, relwidth=0.1)

                tk.Label(yu, text=f'PHONE NO :', bg='#FFE4C4', anchor='e', font='-family {Cascadia Code} -size 9 -weight bold').place(relx=0.01, rely=0.32, relheight=0.1, relwidth=0.1)
                tk.Label(yu, text=f'{s_detail[0][6]} ', bg='#FFE4C4', anchor='w', font='-family {Georgia} -size 12').place( relx=0.12, rely=0.32, relheight=0.1, relwidth=0.26)

                tk.Label(yu, text=f'ROOM ID :', bg='#FFE4C4', anchor='e',font='-family {Cascadia Code} -size 9 -weight bold').place(relx=0.59, rely=0.2, relheight=0.1, relwidth=0.1)
                tk.Label(yu, text=f'{s_detail[0][12]} ', bg='#FFE4C4', anchor='w', font='-family {Georgia} -size 12').place( relx=0.7, rely=0.2, relheight=0.1, relwidth=0.1)

                tk.Label(yu, text=f'ROOM NO :', bg='#FFE4C4', anchor='e', font='-family {Cascadia Code} -size 9 -weight bold').place(relx=0.81, rely=0.2, relheight=0.1, relwidth=0.1)
                tk.Label(yu, text=f'{s_detail[0][12]} ', bg='#FFE4C4', anchor='w', font='-family {Georgia} -size 12').place( relx=0.92, rely=0.2, relheight=0.1, relwidth=0.1)

                tk.Label(yu, text=f'Email ID :', bg='#FFE4C4', anchor='e', font='-family {Cascadia Code} -size 9 -weight bold').place(relx=0.35, rely=0.32, relheight=0.1,relwidth=0.1)
                tk.Label(yu, text=f'{s_detail[0][7]} ', bg='#FFE4C4', anchor='w', font='-family {Georgia} -size 12').place(relx=0.46, rely=0.32, relheight=0.1, relwidth=0.32)

                tk.Label(yu, text=f'Mpesa Transaction Detail', fg=side_bar_frame_bg_color, bg='#FFE4C4', anchor='w', font='-family {Georgia} -size 13 -weight bold').place(relx=0.01, rely=0.44, relheight=0.078,   relwidth=0.6)
                tk.Label(yu, text=f'MPESA TRANSACTION CODE :', bg='#FFE4C4', anchor='e', font='-family {Cascadia Code} -size 9 -weight bold').place(relx=0.01, rely=0.54, relheight=0.1,  relwidth=0.21)
                tk.Label(yu, text=f'{out[0][3]}: ', bg='#FFE4C4', anchor='w', font='-family {Georgia} -size 12').place(relx=0.23, rely=0.54, relheight=0.1, relwidth=0.3)
                tk.Label(yu, text=f'MPESA TRANSACTION DATE :', bg='#FFE4C4', anchor='e',font='-family {Cascadia Code} -size 9 -weight bold').place(relx=0.01, rely=0.65, relheight=0.1, relwidth=0.21)
                tk.Label(yu, text=f'{out[0][6]} ', bg='#FFE4C4', anchor='w', font='-family {Georgia} -size 12').place(relx=0.23,rely=0.65,relheight=0.1,  relwidth=0.3)
                tk.Label(yu, text=f'PAYMENT FOR :', bg='#FFE4C4', anchor='e',font='-family {Cascadia Code} -size 9 -weight bold').place(relx=0.01, rely=0.76, relheight=0.1, relwidth=0.21)
                tk.Label(yu, text=f'{out[0][4]} ', bg='#FFE4C4', anchor='w', font='-family {Georgia} -size 12').place(relx=0.23, rely=0.76,relheight=0.1,relwidth=0.3)
                tk.Label(yu, text=f'PAYMENT STATUS :', bg='#FFE4C4', anchor='e', font='-family {Cascadia Code} -size 9 -weight bold').place(relx=0.01, rely=0.87, relheight=0.1, relwidth=0.21)
                tk.Label(yu, text=f'{out[0][5]} ', bg='#FFE4C4', anchor='w', font='-family {Georgia} -size 12').place(relx=0.23, rely=0.87, relheight=0.1, relwidth=0.3)
                conf_bt = tk.Button(yu, text=f'CONFIRM PAYMENT', bg='#708238', borderwidth=0, activebackground='#1C352D', activeforeground='white', anchor='center', font='-family {Consolas} -size 10 -weight bold', command=confirm_tans)
                conf_bt.place(relx=0.543, rely=0.87, relheight=0.1, relwidth=0.16)
                changeOnHover(conf_bt, '#0B6623', '#708238')
                conf_bt1 = tk.Button(yu, text=f'REJECT PAYMENT', bg='#708238', borderwidth=0, activebackground='#1C352D', activeforeground='white', anchor='center', font='-family {Consolas} -size 10 -weight bold', command=reject_tans)
                conf_bt1.place(relx=0.71, rely=0.87, relheight=0.1, relwidth=0.16)
                changeOnHover(conf_bt1, 'RED', '#708238')




    mycursor.execute("SELECT * FROM hostel.payment where Student_id = %s;", [num])
    payment_out = mycursor.fetchall()
    j = len(payment_out)
    i = j - 1
    h = 0.2

    while j != 0:
        tk.Label(section_T2, bg='#212122', text=f"{payment_out[i][0]}", anchor='w', borderwidth=0, fg='white',font='-family {Consolas} -size 10').place(relx=0.01, rely=h, relheight=0.05, relwidth=0.1)
        tk.Label(section_T2, bg='#212122', text=f"{payment_out[i][2]}", borderwidth=0, fg='white', font='-family {Consolas} -size 10').place(relx=0.113, rely=h, relheight=0.05, relwidth=0.11)
        tk.Label(section_T2, bg='#212122', text=f"{payment_out[i][3]}", borderwidth=0, fg='white', font='-family {Consolas} -size 10').place(relx=0.225, rely=h, relheight=0.05, relwidth=0.152)
        tk.Label(section_T2, bg='#212122', text=f"{payment_out[i][6]}", borderwidth=0, fg='white',font='-family {Consolas} -size 10').place(relx=0.38, rely=h, relheight=0.05, relwidth=0.152)
        tk.Label(section_T2, bg='#212122', text=f"{payment_out[i][4]}", borderwidth=0, fg='white', font='-family {Consolas} -size 10').place(relx=0.535, rely=h, relheight=0.05, relwidth=0.152)
        if payment_out[i][5] == 'pending':
               p_b = tk.Button(section_T2, bg='#212122', activebackground='#212122',text=f"{payment_out[i][5]}", borderwidth=0, fg='red',font='-family {Georgia} -size 11', command=lambda k= i: t_pending(payment_out[k][0]))
               p_b.place(relx=0.7034, rely=h, relheight=0.05, relwidth=0.17)
               changeOnHover(p_b, 'yellow', '#212122')
        elif payment_out[i][5] == 'complete':
               tk.Label(section_T2, bg='#212122', text=f"{payment_out[i][5]}", borderwidth=0, fg='green', font='-family {Georgia} -size 11').place(relx=0.7034, rely=h, relheight=0.05, relwidth=0.17)
        elif payment_out[i][5] == 'rejected':
               tk.Label(section_T2, bg='#212122', text=f"{payment_out[i][5]}", borderwidth=0, fg='pink',font='-family {Georgia} -size 11').place(relx=0.7034, rely=h, relheight=0.05, relwidth=0.17)
        h = h + 0.06
        j = j-1
        i = i - 1

serch_var = tk.IntVar()
tk.Label(section_T2, text='STUDENT ID', fg = sections_fg_colors, bg = sections_bg_colors, anchor='w', font='-family {Consolas} -size 10 -weight bold').place(relx=0.01, rely=0.02, relheight=0.05,relwidth=0.1)
tk.Entry(section_T2, bg='gray', textvariable=serch_var).place(relx=0.115, rely=0.02, relheight=0.05, relwidth=0.12)
tk.Button(section_T2, text='search',  fg = sections_fg_colors, bg = sections_bg_colors,  borderwidth=0, command=lambda :student_trans(serch_var.get())).place(relx=0.24, rely=0.02, relheight=0.05, relwidth=0.06)







root.mainloop()
