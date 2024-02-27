import tkinter as tk
from tkcalendar import *
from PIL import Image, ImageTk
import base64
import io
import subprocess
import json
import threading
import mysql.connector
# Create an instance of tkinter frame
root = tk.Tk()
root.state('zoomed')
root.minsize(1050, 800)
session_user_id = None

# ============================ Functions ==============================================================================
def frame_changer(frame):
    frame.tkraise()

def changeOnHover(button, colorOnHover, colorOnLeave):
    button.bind("<Enter>", func=lambda e: button.config( background=colorOnHover))
    button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))

def restart_g():
    def restart_instance():
        try:
            cmd = 'python Student_Module.py'
            p = subprocess.Popen(cmd, shell=True)
            out, err = p.communicate()
            print(err)
            print(out)
        except Exception as e:
            pass

    threading.Thread(target=restart_instance).start()
    root.destroy()

def Exit_program():
    mycursor.execute("UPDATE hostel.log_rept SET logout_time = CURTIME() WHERE Log_id = %s;", [log_id])
    mydb.commit()
    def open_Home_instance():
        cmd = 'python Home_Module.py'
        p = subprocess.Popen(cmd, shell=True)
        out, err = p.communicate()
        print(err)
        print(out)

    threading.Thread(target=open_Home_instance).start()
    root.destroy()

# =====================================================================================================================================================================

side_bar_color = '#317873'
side_frame = tk.Frame(root, bg=side_bar_color)
side_frame.place(relx=0, rely=0,relheight=1,relwidth=0.155)

sb1 = tk.Button(side_frame, fg='white',bg=side_bar_color, text="✤ Dashboard", activeforeground='#043927', borderwidth=0, anchor='w' ,font='-family {Cambria} -size 13', command=lambda:frame_changer(Dashboard_frame))
sb1.place(rely=0.15, relwidth=1, relheight=0.03)
changeOnHover(sb1, '#9DC183', side_bar_color)

sb2 = tk.Button(side_frame, fg='white', bg=side_bar_color, text="⍜ Profile & Documentation ", activeforeground='#043927',borderwidth=0, anchor='w',font='-family {Cambria} -size 13', command=lambda : frame_changer(Profile_Documentation_frame))
sb2.place(rely=0.2, relwidth=1, relheight=0.03)
changeOnHover(sb2, '#9DC183', side_bar_color)

sb3 = tk.Button(side_frame, fg='white', bg=side_bar_color, text="∾ Notice Board", activeforeground='#043927',borderwidth=0, anchor='w',font='-family {Cambria} -size 13', command=lambda : frame_changer(notice_board_frame))
sb3.place(rely=0.25, relwidth=1, relheight=0.03)
changeOnHover(sb3, '#9DC183', side_bar_color)

sb4 = tk.Button(side_frame, fg='white',bg=side_bar_color, text="∞ Complaint", activeforeground='#043927',borderwidth=0, anchor='w',font='-family {Cambria} -size 13', command=lambda : frame_changer(Complaint_frame))
sb4.place(rely=0.3, relwidth=1, relheight=0.03)
changeOnHover(sb4, '#9DC183', side_bar_color)

sb5 = tk.Button(side_frame, fg='white',bg=side_bar_color, text="⌘ Visitor log", activeforeground='#043927',borderwidth=0, anchor='w',font='-family {Cambria} -size 13', command=lambda : frame_changer(visitor_log_frame))
sb5.place(rely=0.35, relwidth=1, relheight=0.03)
changeOnHover(sb5, '#9DC183', side_bar_color)

sb6 = tk.Button(side_frame, fg='white',bg=side_bar_color, text="✆ Make Payment", activeforeground='#043927',borderwidth=0, anchor='w',font='-family {Cambria} -size 13', command=lambda : frame_changer(Financials_frame))
sb6.place(rely=0.4, relwidth=1, relheight=0.03)
changeOnHover(sb6, '#9DC183', side_bar_color)


sb7 = tk.Button(side_frame, fg='white',bg=side_bar_color, text="⌭ Exit", activeforeground='red',borderwidth=0, anchor='w',font='-family {Cambria} -size 13', command=lambda : Exit_program())
sb7.place(rely=0.5, relwidth=1, relheight=0.03)
changeOnHover(sb7, 'red', side_bar_color)

sb7 = tk.Button(side_frame, fg='white',bg=side_bar_color, text="⟳ Restart", activeforeground='#043927',borderwidth=0, anchor='w',font='-family {Cambria} -size 13', command= restart_g)
sb7.place(rely=0.55, relwidth=1, relheight=0.03)
changeOnHover(sb7, '#1C352D', side_bar_color)



try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12hezron12",
        database="hostel"
    )
    mycursor = mydb.cursor()
except:
    cmd = 'python Home_Module.py'
    p = subprocess.Popen(cmd, shell=True)
    out, err = p.communicate()
    print(err)
    print(out)
    root.destroy()
try:
    with open('SessionInfo.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    session_user_id = json_object['session_id']
    log_id =  json_object['log_id']
except:
    cmd = 'python Home_Module.py'
    p = subprocess.Popen(cmd, shell=True)
    out, err = p.communicate()
    print(err)
    print(out)
    root.destroy()

mycursor.execute("select * from users where user_id = %s", [session_user_id])
output = mycursor.fetchall()
db_username = output[0][0]
db_userpassword = output[0][1]
db_userid = output[0][2]
db_userrole = output[0][3]
db_image = output[0][4]

mycursor.execute("SELECT * FROM hostel.student WHERE user_id = %s ;", [db_userid])
output = mycursor.fetchall()

try:
    student_id = output[0][0]
except:
    cmd = 'python Home_Module.py'
    p = subprocess.Popen(cmd, shell=True)
    out, err = p.communicate()
    print(err)
    print(out)
    root.destroy()

first_name = output[0][1]
second_name = output[0][2]
last_name = output[0][3]
date_of_birth = output[0][4]
gender = output[0][5]
phone_no = output[0][6]
email_id = output[0][7]
year_of_study = output[0][8]
institution = output[0][9]
national_id = output[0][10]
user_id = output[0][11]
room_id =output[0][12]

mycursor.execute("SELECT * FROM hostel.room WHERE room_id = %s ;", [room_id])
output = mycursor.fetchall()

room_type = output[0][1]
room_number = output[0][2]
room_price =  output[0][3]
room_status = output[0][4]
room_condition = output[0][5]
total_beds = output[0][6]
room_amenities = output[0][7]

mycursor.execute('SELECT * FROM hostel.hostel_stay WHERE student_id = %s ;', [student_id])
stay_days = mycursor.fetchall()
if stay_days != []:
    check_in_date = stay_days[0][1]
    check_out_date = stay_days[0][2]
else:
    mycursor.execute("insert into  hostel.hostel_stay  (student_id, check_in, check_out) values( %s, CURDATE(), CURDATE());", [student_id])
    mydb.commit()
    mycursor.execute('SELECT * FROM hostel.hostel_stay WHERE student_id = %s ;', [student_id])
    stay_days = mycursor.fetchall()
    check_in_date = stay_days[0][1]
    check_out_date = stay_days[0][2]
    
# ===================================== Dashboard_frame ================================================================
Dashboard_frame = tk.Frame(root, bg='#26282A')
Dashboard_frame.place(relx=0.155, relheight=1, relwidth=0.845)

top_dash = tk.Frame(Dashboard_frame, bg='#1b1811')
top_dash.place(relheight=0.05, relwidth=1)
full_name = f' {first_name} { second_name } { last_name}'
tk.Label(top_dash, text = f'Welcome : {full_name}', anchor='w', bg='#1b1811', foreground='white', borderwidth=100).place(relx=0.02,relheight=1, relwidth=0.3)

profil_photo_frame = tk.Frame(Dashboard_frame, bg='#212122')
profil_photo_frame.place(relx=0.05, rely=0.1, relwidth=0.16, relheight=0.16)
if db_image != None:
    binary_data = base64.b64decode(db_image) # Decode the string
    profile_image = Image.open(io.BytesIO(binary_data)) # Convert the bytes into a PIL image
    Resized_image = profile_image.resize((204, 160), Image.ANTIALIAS)
    new_image = ImageTk.PhotoImage(Resized_image)
    tk.Label(profil_photo_frame, image=new_image, bg='#212122', border=100, justify='center').place(relx=0, rely=0, relwidth=1, relheight=1)
else:
    tk.Label(profil_photo_frame, text='NO PROFILE IMAGE',fg=side_bar_color, bg='#212122', border=100, justify='center', font='-family {Times New Roman} -size 10 -weight bold').place(relx=0, rely=0, relwidth=1, relheight=1)

tk.Label(Dashboard_frame,text='Profile Image', fg='#8A9A5B', bg='#212122',font='-family {Times New Roman} -size 13').place(relx=0.05, rely=0.26, relwidth=0.16, relheight=0.03)


frame_1 = tk.Frame(Dashboard_frame, borderwidth=10, bg='#212122')
frame_1.place(relx=0.05, rely=0.3, relheight=0.2, relwidth=0.9)
tk.Label(frame_1, text=f'User Id   : {user_id}', bg='#212122', fg='white', anchor='w', font='-family {Times New Roman} -size 13').place(rely= 0, relheight=0.15, relwidth=0.3)
tk.Label(frame_1, text=f'Room id   : {room_id}', bg='#212122',fg='white', anchor='w', font='-family {Times New Roman} -size 13').place(rely= 0.16, relheight=0.15, relwidth=0.3)
tk.Label(frame_1, text=f'Room No   : {room_number} - {room_type} ', bg='#212122',fg='white', anchor='w', font='-family {Times New Roman} -size 13').place(rely= 0.32, relheight=0.15, relwidth=0.3)
tk.Label(frame_1, text=f'Room Price   : {room_price}', bg='#212122',fg='white', anchor='w', font='-family {Times New Roman} -size 13').place(rely= 0.48, relheight=0.15, relwidth=0.3)
tk.Label(frame_1, text=f'|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n', bg='#212122', fg=side_bar_color, font='-size 10 -weight bold').place(rely= 0, relx=0.31, relheight=1, relwidth=0.02)
tk.Label(frame_1, text=f'First Name    : {first_name}', bg='#212122', fg='white', anchor='w', font='-family {Times New Roman} -size 13').place(rely= 0,  relx=0.34, relheight=0.15, relwidth=0.32)
tk.Label(frame_1, text=f'Second Name   : {second_name}', bg='#212122', fg='white', anchor='w', font='-family {Times New Roman} -size 13').place(rely= 0.16,  relx=0.34, relheight=0.15, relwidth=0.32)
tk.Label(frame_1, text=f'Sir Name      : {last_name}', bg='#212122', fg='white', anchor='w', font='-family {Times New Roman} -size 13').place(rely= 0.32,  relx=0.34, relheight=0.15, relwidth=0.32)
tk.Label(frame_1, text=f'Date of Birth : {date_of_birth}', bg='#212122', fg='white', anchor='w', font='-family {Times New Roman} -size 13').place(rely= 0.48,  relx=0.34, relheight=0.15, relwidth=0.32)
tk.Label(frame_1, text=f'ID No         : {national_id}', bg='#212122', fg='white', anchor='w', font='-family {Times New Roman} -size 13').place(rely= 0.64,  relx=0.34, relheight=0.15, relwidth=0.32)
tk.Label(frame_1, text=f'Year Of Study : {year_of_study} year', bg='#212122', fg='white', anchor='w',font='-family {Times New Roman} -size 13').place(rely= 0.64,  relx=0.34, relheight=0.15, relwidth=0.32)
tk.Label(frame_1, text=f'Phone No      :  (+254) {phone_no}', bg='#212122', fg='white', anchor='w', font='-family {Times New Roman} -size 13').place(rely= 0.8,  relx=0.34, relheight=0.15, relwidth=0.32)
tk.Label(frame_1, text=f'|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n', bg='#212122', fg=side_bar_color, font='-size 10 -weight bold').place(rely= 0, relx=0.67, relheight=1, relwidth=0.02)
tk.Label(frame_1, text=f'Checked In   :  {check_in_date}', bg='#212122', fg='white', anchor='w', font='-family {Times New Roman} -size 13').place(rely= 0, relx=0.7, relheight=0.25, relwidth=0.3)
tk.Label(frame_1, text=f'Check   Out  :  {check_out_date}', bg='#212122', fg='white', anchor='w', font='-family {Times New Roman} -size 13').place(rely= 0.27, relx=0.7, relheight=0.25, relwidth=0.3)

frame_2 = tk.Frame(Dashboard_frame, borderwidth=10, bg='#212122')
frame_2.place(relx=0.05, rely=0.52, relheight=0.2, relwidth=0.9)
mycursor.execute("SELECT * FROM hostel.parent_info WHERE student_id = %s;", [student_id])
parent_info = mycursor.fetchall()
parent_fist_name = parent_info[0][0]
parent_second_name = parent_info[0][1]
parent_phone_no = parent_info[0][2]
parent_Email_id = parent_info[0][3]

tk.Label(frame_2, text=' Guarantor Information ', anchor='w', bg='#212122',  fg='white', font='-family {Georgia} -underline true -size 13 ').place(relx=0,rely=0, relheight=0.1, relwidth=0.32)
tk.Label(frame_2, text=f'First_name     :    {parent_fist_name} ', bg='#212122', fg='white', anchor='w', font='-family {Times New Roman} -size 11').place(relx=0,rely=0.15, relheight=0.1, relwidth=0.32)
tk.Label(frame_2, text=f'Second_name    :    {parent_second_name}', bg='#212122',  fg='white', anchor='w', font='-family {Times New Roman} -size 11').place(relx=0,rely=0.29, relheight=0.1, relwidth=0.32)
tk.Label(frame_2, text=f'Phone_number   :    {parent_phone_no}', bg='#212122', fg='white', anchor='w', font='-family {Times New Roman} -size 11').place(relx=0,rely=0.42, relheight=0.1, relwidth=0.32)
tk.Label(frame_2, text=f'Email_Address  :    {parent_Email_id}', bg='#212122', fg='white', anchor='w', font='-family {Times New Roman} -size 11').place(relx=0,rely=0.56, relheight=0.1, relwidth=0.32)
tk.Label(frame_2, text=f'|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n', bg='#212122', fg=side_bar_color, font='-size 10 -weight bold').place(rely=0, relx=0.31, relheight=1, relwidth=0.02)

from datetime import datetime, date
date_checked_in = datetime.strptime(str(check_in_date), "%Y-%m-%d")
date_checked_out = datetime.strptime(str(check_out_date), "%Y-%m-%d")
date_today = datetime.strptime(str(date.today()), "%Y-%m-%d")
total_days_to_stay = abs((date_checked_out - date_checked_in).days)
total_days_stayed = abs((date_today - date_checked_in).days)
total_days_remaining = abs((date_checked_out - date_today).days)

print(total_days_stayed)

frame_3 = tk.Frame(Dashboard_frame, borderwidth=10, bg='#212122')
frame_3.place(relx=0.05, rely=0.75, relheight=0.2, relwidth=0.27)
tk.Label(frame_3,text=f'{total_days_to_stay}', anchor='w', fg='gold',  bg='#212122', font='-family {Cascadia Code} -size 20').place(rely=0.1, relwidth=1, relheight=0.3)
tk.Label(frame_3,text=' Days intended to Stay', bg='#212122',fg='white', anchor='w', font='-family {Goudy Old Style} -size 11').place(rely=0.34, relwidth=1, relheight=0.3)

frame_4 = tk.Frame(Dashboard_frame, borderwidth=10, bg='#212122')
frame_4.place(relx=0.35, rely=0.75, relheight=0.2, relwidth=0.27)
tk.Label(frame_4,text=f'{total_days_stayed}', anchor='w',fg='gold',  bg='#212122', font='-family {Cascadia Code} -size 20').place(rely=0.1, relwidth=1, relheight=0.3)
tk.Label(frame_4,text='Days Stayed in current booking', bg='#212122',fg='white', anchor='w', font='-family {Goudy Old Style} -size 11').place(rely=0.34, relwidth=1, relheight=0.3)


frame_5 = tk.Frame(Dashboard_frame, borderwidth=10, bg='#212122')
frame_5.place(relx=0.65, rely=0.75, relheight=0.2, relwidth=0.27)
tk.Label(frame_5,text=f'{total_days_remaining}', anchor='w',fg='gold', bg='#212122', font='-family {Cascadia Code} -size 20').place(rely=0.1, relwidth=1, relheight=0.3)
tk.Label(frame_5,text='Days Remaining in current booking', bg='#212122',fg='white', anchor='w', font='-family {Goudy Old Style} -size 11').place(rely=0.34, relwidth=1, relheight=0.3)


# ======================================= Profile & Documentation frame ================================================
Profile_Documentation_frame = tk.Frame(root, bg='#26282A')
Profile_Documentation_frame.place(relx=0.155, relheight=1, relwidth=0.845)

top_bar = tk.Frame(Profile_Documentation_frame, bg='gold')
top_bar.place(relx=0, rely=0.1, relwidth=1, relheight=0.04)
ppt = tk.Button(top_bar, text='Profile', borderwidth=0,relief='sunken', activeforeground='Blue',activebackground='gold', bg='gold', font='-family {Cascadia Code} -size 11 -weight bold', command=lambda :frame_changer(proile))
ppt.place(rely=0, relx=0.05, relheight=1, relwidth=0.1)
changeOnHover(ppt, '#C2B280', 'gold')
pdt = tk.Button(top_bar, text='Documentation', borderwidth=0,relief='sunken', activeforeground='Blue',activebackground='gold', bg='gold', font='-family {Cascadia Code} -size 11 -weight bold', command=lambda :frame_changer(Docu))
pdt.place(rely=0, relx=0.25, relheight=1, relwidth=0.14)
changeOnHover(pdt, '#C2B280', 'gold')

Docu = tk.Frame(Profile_Documentation_frame, bg='#26282A')
Docu.place(rely=0.15,relx=0, relheight=0.84, relwidth=1)

proile = tk.Frame(Profile_Documentation_frame, bg='#26282A')
proile.place(rely=0.15,relx=0, relheight=0.84, relwidth=1)

proile_frame_1 = tk.Frame(proile, bg='#1C1C1C')
proile_frame_1.place(relwidth=0.26,relheight=0.5, relx=0.05, rely=0.05)
if db_image != None:
    Resized_image_1 = profile_image.resize((320, 230), Image.ANTIALIAS)
    new_image_1 = ImageTk.PhotoImage(Resized_image_1)
    cg_lable = tk.Label(proile_frame_1,image = new_image_1, relief='sunken',borderwidth=0)
    cg_lable.place(relwidth=1,relheight=0.5, relx=0, rely=0)
else:
    cg_lable = tk.Label(proile_frame_1, text='choose Profile Image', fg=side_bar_color,bg='#1C1C1C', relief='sunken', borderwidth=0,font='-family {Consolas} -size 11 -weight bold')
    cg_lable.place(relwidth=1, relheight=0.5, relx=0, rely=0)

tk.Label(proile_frame_1, text=f"WELCOME: {full_name}",bg='#1C1C1C', fg='white', anchor='w', font='-family {Segoe UI} -size 9 -weight bold').place(relx=0.032, rely=0.54, relwidth=0.9, relheight=0.07)
tk.Label(proile_frame_1, text=f"ID: {student_id}",bg='#8A9A5B', fg='white', anchor='w', font='-family {Segoe UI} -size 9 -weight bold').place(relx=0.05, rely=0.6, relheight=0.05)
tk.Label(proile_frame_1, text="Mobile Number", bg='#1C1C1C', anchor='w', fg='white', font='-family {Segoe UI} -size 10 -weight bold').place(relx=0.032, rely=0.65, relwidth=0.9, relheight=0.07)
tk.Label(proile_frame_1, text=f" (254 ) {phone_no}", bg='#043927', fg='white', anchor='w', font='-family {Consolas} -size 10 -weight bold').place(relx=0.032, rely=0.724, relwidth=0.9, relheight=0.08)
tk.Label(proile_frame_1, text=f"Email ID", bg='#1C1C1C', fg='white', anchor='w', font='-family {Segoe UI} -size 10 -weight bold').place(relx=0.032, rely=0.84, relwidth=0.9, relheight=0.06)
tk.Label(proile_frame_1, text=f"{email_id}", bg='#043927', fg='white',anchor='w', font='-family {Consolas} -size 10 -weight bold').place(relx=0.032, rely=0.91, relwidth=0.9, relheight=0.07)


def open_file():
   from tkinter import filedialog
   filepath = filedialog.askopenfilename(title="Select Profile Photo", filetypes=((" ","*.jpg"), (" ","*.png")))
   if filepath != None:
       file = open(filepath, 'rb').read()
       file = base64.b64encode(file)
       mycursor.execute('UPDATE hostel.users SET user_image = %s WHERE user_id = %s', [file,user_id])
       mydb.commit()
       kut = tk.Label(Profile_Documentation_frame, text='Profile Photo Added Successfully',font='-family {Georgia} -size 11 -weight bold', bg='green')
       kut.place(relwidth=0.25,relheight=0.1,relx=0.35,rely=0.4)
       kut.after(4000, lambda : kut.place_forget())

def Change_Password():
    def close(frame):
        frame.destroy()

    def Change_Password_confirm(curr_p, new_p, conf_p):
        print(curr_p)
        print(new_p)
        print(conf_p)
        print(db_userpassword)
        if str(db_userpassword) == str(curr_p):
            if str(new_p) == str(conf_p):
                 if  str(new_p) != '' and str(conf_p) != '':
                            mycursor.execute('Update hostel.users SET user_passwd = %s WHERE user_id = %s;', [new_p, user_id])
                            mydb.commit()
                            change_pass.destroy()
                 else:
                     print("Empty new or confirm password")
            else:
                print('confirm password does not match new password')
        else:
            print('wrong current password')

    Current_Password = tk.StringVar()
    New_Password = tk.StringVar()
    Confirm_Password = tk.StringVar()

    change_pass = tk.Frame(proile, bg='#1C1C1C')
    change_pass.place(relheight=0.43, relwidth=0.6, relx=0.17, rely=0.2)
    tk.Button(change_pass, text='X', fg='#4B3621', activebackground='#1C1C1C', activeforeground='red', bg='#1C1C1C', borderwidth=0, font='-family {Forte} -size 23 -weight bold', command=lambda: close(change_pass)).place(relx=0.898, relwidth=0.1, relheight=0.112)
    tk.Label(change_pass, bg='#1C1C1C', fg='white', text='----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', font='-size 12 ').place(relx=0.01, rely=0.11, relwidth=1, relheight=0.03)
    entry_bg_color = '#A9BA9D'
    tk.Label(change_pass, text='Current Password', anchor='w', fg='white', bg='#1C1C1C', font='-family {Georgia} -size 14 -weight bold').place(relx=0.01, rely=0.15, relwidth=0.35, relheight=0.06)
    yti1 = tk.Entry(change_pass, textvariable=Current_Password, borderwidth=0, bg=entry_bg_color, fg='#000000', font='-family {Calibri} -size 12')
    yti1.place(relx=0.01, rely=0.23, relwidth=0.95, relheight=0.1)
    tk.Label(change_pass, text='Current Password is required', anchor='w', fg='red', bg='#1C1C1C', font='-family {Calibri} -size 8').place(relx=0.01, rely=0.33, relwidth=0.9, relheight=0.06)
    changeOnHover(yti1, '#B6B6B4', entry_bg_color)

    tk.Label(change_pass, text='New Password', anchor='w', fg='white', bg='#1C1C1C', font='-family {Georgia} -size 14 -weight bold').place(relx=0.01, rely=0.42, relwidth=0.35, relheight=0.06)
    yti2 = tk.Entry(change_pass, textvariable=New_Password, borderwidth=0, bg=entry_bg_color, fg='#000000',  font='-family {Calibri} -size 12')
    yti2.place(relx=0.01, rely=0.5, relwidth=0.95, relheight=0.1)
    tk.Label(change_pass, text='Current Password is required', anchor='w', fg='red', bg='#1C1C1C', font='-family {Calibri} -size 8').place(relx=0.01, rely=0.6, relwidth=0.9, relheight=0.06)
    changeOnHover(yti2, '#B6B6B4', entry_bg_color)

    tk.Label(change_pass, text='Confirm Password', anchor='w', fg='white', bg='#1C1C1C', font='-family {Georgia} -size 14 -weight bold').place(relx=0.01, rely=0.69, relwidth=0.35, relheight=0.06)
    yti3 =tk.Entry(change_pass, textvariable=Confirm_Password, borderwidth=0, bg=entry_bg_color, fg='#000000',  font='-family {Calibri} -size 12')
    yti3.place(relx=0.01, rely=0.77, relwidth=0.95, relheight=0.1)
    tk.Label(change_pass, text='Current Password is required', anchor='w', fg='red', bg='#1C1C1C', font='-family {Calibri} -size 8').place(relx=0.01, rely=0.87, relwidth=0.9, relheight=0.06)
    changeOnHover(yti3, '#B6B6B4', entry_bg_color)

    chbc = tk.Button(change_pass, text='CONFIRM', bg='#E97451', activebackground=side_bar_color, borderwidth=0, font='-family {Calibri} -size 9', command=lambda :Change_Password_confirm(Current_Password.get(), New_Password.get(), Confirm_Password.get()))
    chbc.place(relx=0.8, rely=0.91, relheight=0.07,relwidth=0.15)
    changeOnHover(chbc, '#9DC183', '#E97451')
def chang_phone():
    new_phone_n = tk.StringVar()
    def update_phone(new_num):
        if new_num != '':
                num = int(new_num)
                num_len = len(str(num))
                if num != 0 and num_len > 8:
                    mycursor.execute('Update hostel.student SET phone_no = %s WHERE user_id = %s;', [num, user_id])
                    mydb.commit()
                    c_phone_frame.config(bg='green')
                    c_phone_frame.destroy()
                else:
                    print("Error: wrong number format")
        else:
            print("Error: Empty Phone NumberEntry")

    c_phone_frame = tk.Frame(proile,  bg='#1C1C1C')
    c_phone_frame.place(relwidth=0.46,relheight=0.08, relx=0.35, rely=0.13)
    tk.Button(c_phone_frame, text='X', borderwidth=0,  bg='#1C1C1C', fg='red', activebackground='#1C1C1C', font='-family {Forte} -size 9 -weight bold', command= lambda:c_phone_frame.destroy()).place(rely=0, relx=0.9, relwidth=0.1, relheight=0.3)
    tk.Label(c_phone_frame, text='New Phone (+254)', anchor='w', fg='white', bg='#1C1C1C', font='-family {Cascadia Code} -size 10').place(rely=0.14, relx=0.025, relwidth=0.6, relheight=0.31)
    pch = tk.Entry(c_phone_frame,bg='#292929', fg='white', textvariable=new_phone_n, borderwidth=0, font='-family {Cascadia Code} -size 9')
    pch.place(rely=0.5, relx=0.025, relwidth=0.75, relheight=0.4)
    u_pch = tk.Button(c_phone_frame, text='Update', borderwidth=0, bg='#E97451', font='-family {Cascadia Code} -size 9', command=lambda:update_phone(new_phone_n.get()))
    u_pch.place(rely=0.5, relx=0.776, relwidth=0.2, relheight=0.4)
    changeOnHover(pch, '#B6B6B4', '#292929')
    changeOnHover(u_pch, '#B0BF1A', '#E97451')
def chang_parent_info():
    parent_info_frame = tk.Frame(proile,  bg='#1C1C1C')
    parent_info_frame.place(relwidth=0.46,relheight=0.33, relx=0.35, rely=0.165)
    tk.Button(parent_info_frame, text='X', borderwidth=0,   bg='#1C1C1C', fg='red', activebackground='#1C1C1C',activeforeground='brown', font='-family {Forte} -size 14 -weight bold', command= lambda:parent_info_frame.destroy()).place(rely=0, relx=0.82, relwidth=0.17, relheight=0.15)
    entry_bg_color = '#A9BA9D'
    tk.Label(parent_info_frame, text='First_name', anchor='w', fg='white', bg='#1C1C1C', font='-family {Cascadia Code} -size 10').place(relx=0.025,rely=0.07, relwidth=0.5,relheight=0.1)
    k23 = tk.Entry(parent_info_frame, bg=entry_bg_color)
    k23 .place(relx=0.025,rely=0.18, relwidth=0.9,relheight=0.1)
    changeOnHover(k23 , '#B6B6B4', entry_bg_color)
    tk.Label(parent_info_frame, text='Second_name', anchor='w', fg='white', bg='#1C1C1C', font='-family {Cascadia Code} -size 10').place(relx=0.025,rely=0.29, relwidth=0.5,relheight=0.1)
    k24 = tk.Entry(parent_info_frame, bg=entry_bg_color)
    k24.place(relx=0.025,rely=0.4, relwidth=0.9,relheight=0.1)
    changeOnHover(k24, '#B6B6B4', entry_bg_color)
    tk.Label(parent_info_frame, text='Phone_number', anchor='w', fg='white', bg='#1C1C1C', font='-family {Cascadia Code} -size 10').place(relx=0.025,rely=0.51, relwidth=0.5,relheight=0.1)
    k25 = tk.Entry(parent_info_frame, bg=entry_bg_color)
    k25.place(relx=0.025,rely=0.62, relwidth=0.9,relheight=0.1)
    changeOnHover(k25, '#B6B6B4', entry_bg_color)
    tk.Label(parent_info_frame, text='Email_Address', anchor='w', fg='white', bg='#1C1C1C', font='-family {Cascadia Code} -size 10').place(relx=0.025,rely=0.73, relwidth=0.5,relheight=0.1)
    k26 = tk.Entry(parent_info_frame, bg=entry_bg_color)
    k26.place(relx=0.025,rely=0.84, relwidth=0.9, relheight=0.1)
    changeOnHover(k26, '#B6B6B4', entry_bg_color)
    tk.Button(parent_info_frame, text="Update", borderwidth=0, fg='white',  bg='#1C1C1C',activebackground='#1C1C1C',activeforeground='green',font='-family {Forte} -size 14').place(relx=0.47,rely=0, relwidth=0.34,relheight=0.15)
def account_detail():
    account_detail_frame = tk.Frame(proile, relief='sunken', borderwidth=0,bg='#1C1C1C' )
    account_detail_frame.place(relwidth=0.46, relheight=0.4, relx=0.35, rely=0.2)
    tk.Button(account_detail_frame, text='X', borderwidth=0,   bg='#1C1C1C', fg='red', activebackground='#1C1C1C',activeforeground='brown', font='-family {Forte} -size 14 -weight bold', command= lambda:account_detail_frame.destroy()).place(rely=0, relx=0.86, relwidth=0.14, relheight=0.12)

pd1 = tk.Button(proile, text='Change Profile', relief='sunken',borderwidth=0, bg=side_bar_color, activeforeground='green', font='-family {Cascadia Code} -size 11 -weight bold', command=open_file)
pd1.place(relwidth=0.46,relheight=0.03, relx=0.35, rely=0.06)
changeOnHover(pd1, '#004B49', side_bar_color)
pd2 = tk.Button(proile, text='Change Password', relief='sunken',borderwidth=0, bg=side_bar_color, activeforeground='green', font='-family {Cascadia Code} -size 11 -weight bold', command=Change_Password)
pd2.place(relwidth=0.46,relheight=0.03, relx=0.35, rely=0.095)
changeOnHover(pd2, '#004B49', side_bar_color)
pd3 = tk.Button(proile, text='Change Phone Number', relief='sunken',borderwidth=0, bg=side_bar_color, activeforeground='green', font='-family {Cascadia Code} -size 11 -weight bold', command=chang_phone)
pd3.place(relwidth=0.46,relheight=0.03, relx=0.35, rely=0.13)
changeOnHover(pd3, '#004B49', side_bar_color)
pd4 = tk.Button(proile, text='Guarantor Information', relief='sunken',borderwidth=0, bg=side_bar_color, activeforeground='green', font='-family {Cascadia Code} -size 11 -weight bold', command=chang_parent_info)
pd4.place(relwidth=0.46,relheight=0.03, relx=0.35, rely=0.165)
changeOnHover(pd4, '#004B49', side_bar_color)
pd5 = tk.Button(proile, text='Account details', relief='sunken',borderwidth=0, bg=side_bar_color, activeforeground='green', font='-family {Cascadia Code} -size 11 -weight bold', command=account_detail)
pd5.place(relwidth=0.46,relheight=0.03, relx=0.35, rely=0.2)
changeOnHover(pd5, '#004B49', side_bar_color)



# ================ doc page =========================



def Agreement_download():
            import webbrowser
            from fpdf import FPDF
            class PDF(FPDF):
                pass
            pdf = PDF('P', 'mm')  # pdf object
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            pdf.set_font('helvetica', '', 16)
            pdf.cell(0, 10, 'Tenancy Agreement!', ln=True, align='C')
            pdf.ln(15)  # line break
            pdf.page_no()
            pdf.set_font('helvetica', 'UB', 16)
            pdf.cell(90, 10, 'Tenant Details', align='R', ln=True)  # Add text (width, height, text, ln=True/False)

            pdf.set_font('times', 'B', 10)
            pdf.cell(90, 8, 'Name  :', align='R')  # Add text (width, height, text, ln=True/False)
            pdf.set_font('courier', '', 10)
            pdf.cell(105, 8, f'{full_name}  ', ln=True)

            pdf.set_font('times', 'B', 10)
            pdf.cell(90, 8, 'Date Of Birth  :', align='R')  # Add text (width, height, text, ln=True/False)
            pdf.set_font('courier', '', 10)
            pdf.cell(105, 8, f' {date_of_birth} ', ln=True)

            pdf.set_font('times', 'B', 10)
            pdf.cell(90, 8, 'Gender  :', align='R')  # Add text (width, height, text, ln=True/False)
            pdf.set_font('courier', '', 10)
            pdf.cell(105, 8, f' {gender} ', ln=True)

            pdf.set_font('times', 'B', 10)
            pdf.cell(90, 8, 'Phone NO  :', align='R')  # Add text (width, height, text, ln=True/False)
            pdf.set_font('courier', '', 10)
            pdf.cell(105, 8, f' {phone_no} ', ln=True)

            pdf.set_font('times', 'B', 10)
            pdf.cell(90, 8, 'Email ID  :', align='R')  # Add text (width, height, text, ln=True/False)
            pdf.set_font('courier', '', 10)
            pdf.cell(105, 8, f'{email_id} ', ln=True)

            pdf.set_font('times', 'B', 10)
            pdf.cell(90, 8, 'Year Of Study  :', align='R')  # Add text (width, height, text, ln=True/False)
            pdf.set_font('courier', '', 10)
            pdf.cell(105, 8, f' {year_of_study} ', ln=True)

            pdf.set_font('times', 'B', 10)
            pdf.cell(90, 10, 'Institution  :', align='R')  # Add text (width, height, text, ln=True/False)
            pdf.set_font('courier', '', 10)
            pdf.cell(105, 10, f' {institution}', ln=True)

            pdf.set_font('times', 'B', 10)
            pdf.cell(90, 10, 'National ID  :', align='R')  # Add text (width, height, text, ln=True/False)
            pdf.set_font('courier', '', 10)
            pdf.cell(105, 10, f' {national_id} ', ln=True)


            pdf.ln(5)
            pdf.set_font('helvetica', 'B', 14)
            pdf.cell(90, 10, 'Sponsor/Guardian', align='R', ln=True)  # Add text (width, height, text, ln=True/False)
            pdf.set_font('times', '', 10, )
            pdf.cell(90, 1, '')
            pdf.cell(105, 1, '', ln=True)
            pdf.cell(90, 10, 'Name  :', align='R')
            pdf.cell(105, 10, f' {parent_fist_name} {parent_second_name} ', ln=True)
            pdf.cell(90, 10, 'phone number  :', align='R')
            pdf.cell(105, 10, f'(+254)  {parent_phone_no} ', ln=True)
            pdf.cell(90, 10, 'Email Address  :', align='R')
            pdf.cell(105, 10, f'  {parent_Email_id} ', ln=True)
            pdf.cell(90, 10, '')
            pdf.set_font('courier', 'I', 8)
            pdf.multi_cell(105, 10, 'An individual or an entity that agrees to be responsible for the compliance with any and all of the obligations created under this Agreement and imposed upon the Tenant, whether pecuniary or otherwise, should the Tenant fail to meet such obligations ')


            pdf.ln(5)
            pdf.set_font('helvetica', 'B', 14)
            pdf.cell(90, 10, 'Room Details', align='R', ln=True)
            pdf.set_font('times', '', 10)
            pdf.cell(90, 1, '')
            pdf.cell(105, 1, '', ln=True)
            pdf.cell(90, 10, 'Apartment No  :', align='R')
            pdf.cell(105, 10, f'    {room_number}', ln=True)
            pdf.cell(90, 10, ' Room Type  :', align='R')
            pdf.cell(105, 10, f'    {room_type}', ln=True)
            pdf.cell(90, 10, 'Rent Price  :', align='R')
            pdf.cell(105, 10, f'    {room_price}', ln=True)
            pdf.cell(90, 10, 'Term', align='R')
            pdf.cell(105, 10, f' The period from {check_in_date} to {check_out_date}', ln=True)



            pdf.ln(14)

            pdf.set_font('helvetica', 'UB', 12)
            pdf.cell(90, 10, 'Terms', ln=True)
            pdf.set_font('times', '', 10)
            pdf.multi_cell(0, 10, '\
            Length of Agreement: Month-to-Month Either party may cancel or change terms of this agreement upon thirty (30) days WRITTEN notice. The notice period may be lengthened or shortened by WRITTEN agreement, but no less than 7 days')
            pdf.ln(9)

            pdf.set_font('helvetica', 'UB', 12)
            pdf.cell(90, 10, 'Conflict Resolution', ln=True)
            pdf.set_font('times', '', 10)
            pdf.multi_cell(0, 10, 'Each housemate will strive to develop mutual cooperation with all other housemates. Should disagreements arise, each shall try to resolve the dispute in good faith using clear communication. If disputes continue thereafter, the housemates agree to the following methods of conflict resolution: \n    1.Decision by household consensus\n     2.Decision by Principal Tenant\n     3.Binding mediation by impartial third party\n    4.Decision by Owner \n    5.Decision by household majority vote')
            pdf.ln(3)

            pdf.set_font('helvetica', 'UB', 12)
            pdf.cell(90, 10, 'Privacy', ln=True)
            pdf.set_font('times', '', 10)
            pdf.multi_cell(0, 10, "As required by law, the landlord may enter the tenant's room only for the following reasons: (a) in case of emergency; (b) to make necessary or agreed-upon repairs, decorations, or improvements, supply necessary or agreed-upon services, or exhibit the dwelling unit to prospective or actual purchasers, mortgagees, tenants, workers, or contractors; (c) when the tenant has abandoned or surrendered the premises; or (d) pursuant to court order. The landlord must give the tenant WRITTEN twenty-four (24) hours notice of intent to enter and may enter only during normal business hours, excepting by necessity, cases (a) and (c) above. ")

            pdf.ln(4)
            pdf.set_font('helvetica', 'B', 12)
            pdf.cell(0, 10, 'GENERAL CONDITIONS FOR ACCOMMODATION BOOKING', align='C', ln=True)
            pdf.set_font('times', '', 10)
            pdf.multi_cell(0, 10, "\
            1. Rooms are allocated on a first-come-first-serve-basis.\n\
            2. Booking confirmations by payment equivalent to one (1) month deposit and pro-rated rent up to the end of the month must be received by the Finance and Accounts Division of the University, failing which the University will not be able to guarantee the accommodation requested. Thereafter, rent must be paid on a calendar month basis on or before the 7th day of each month.\n\
            3. All applicants are required to sign a tenancy agreement for a minimum period of one (1) academic year (12 months) ")

            pdf.ln(10)
            pdf.set_font('helvetica', 'UB', 11)
            pdf.cell(0, 10, 'Declaration', align='L', ln=True)
            pdf.set_font('times', '', 10)
            pdf.multi_cell(0, 10, "\
            Declaration\n\
            1. I understand and accept the general conditions for booking of hostel accommodation.\n\
            2. I declare that the particulars in this application form are true to the best of my knowledge, and I have not wilfully suppressed any material fact. Any misrepresentation or omission of information will render me ineligible for student accommodation.\n\
            3. I undertake to abide by the Tenancy Agreement and Hostel Accommodation Code of Conduct")

            pdf.ln(5)
            pdf.set_font('helvetica', 'UB', 11)
            pdf.cell(0, 10, 'CODE OF CONDUCT', align='C', ln=True)
            pdf.set_font('times', '', 10)
            pdf.multi_cell(0, 10, "\
            1. All residents are required to carry their valid identity card issued to them by the University\n\
            2. Residents must ensure that the doors are locked and all electrical switches are switched off when not in use.\n\
            3. The responsibility for overall cleanliness of their unit lies with the residents of the respective unit\n\
            4. All residents are expected to be in the hostel before 10.00pm and residents who wishes to be away from the hostel after that time, must obtain prior permission from the Student Affairs Division (SAD).\n\
            5. All visitors must register at the security station upon arrival and departure. No visitors are allowed after 9.00pm\n\
            6. Residents are strictly prohibited from admitting strangers or persons of the opposite sex (except parents/guardians) into the hostel room.\n\
            7. Only immediate family members can visit the resident. The resident must inform and seek approval from SAD\n\
            8. Residents are personally responsible for ensuring all visitors comply with the rules and regulations and they would not cause any inconvenience to other residents\n\
            9. Visitors are strictly prohibited from staying overnight\n\
            10. Residents must seek prior approval to leave the hostel at any other times\n\
            11. Residents are not permitted to give their hostel keys to any other person to use while they are away. Residents found committing such an offence will be evicted\n\
            12. Smoking, consumption of alcohol and drugs are strictly prohibited\n\
            13. Gambling/gaming which involves betting is strictly not allowed within the hostel premises\n\
            14. Vandalism or removing hostel/university property is a very serious offence. Residents found guilty can or will be evicted from the residence. The cost of making good any items vandalized will be charged accordingly to the resident\n\
            15. Viewing, possession and or dissemination of pornographic materials are strictly prohibited\n\
            16. Residents found causing embarrassment, unsolicited compliments, sexually tainted jokes, spreading false rumours will be evicted from the residence\n\
            17. Fighting or any physical violence is not allowed. Residents found committing such an offence will be evicted.\n\
            18. Residents must obtain prior permission before organizing any social events in the hostel.\n\
            19. The University reserves the right to alter, amend, add or delete any of the rules and regulations at anytime without prior notice\n\
            20. The University reserves the right for its designees to enter and inspect a residence in the interests of safety and proper conduct of the students. Entry can be made at any time, whether or not the students are present, and without prior notice to the students.")

            pdf.ln(10)
            pdf.set_font('helvetica', 'UB', 11)
            pdf.cell(0, 10, 'NOTE:', align='C', ln=True)
            pdf.set_font('times', '', 10)
            pdf.multi_cell(0, 10, "\
            I confirm and agree that I have read the Code of Conduct and shall abide with the said Hostel Code of Conduct. In the event I fail to make payments for two (2) consecutive months, I hereby agree that the University can terminate my accommodation contract and request me to vacate the hostel premises immediately.\n\
            I agree that I will not take any action against the University in the event the above action is taken against me as a result of default in payment.\n\
            Witness by Parent/Guardian:\n\
            Student's Name : __________________________________________  No: _____________________\n\
            Signature : __________________________________________ Date: ________________________\n\
            Name : ________________________________________  No: _____________________\n\
            Signature : ___________________________________________Date: ________________________")
            # First_name, Second_name, Phone_number, Email_Address, student_id
            pdf_file_name = f'{first_name}_Tenancy_Agreement.pdf'
            pdf.output(pdf_file_name)
            webbrowser.get('windows-default').open(pdf_file_name)





ag_d = tk.Button(Docu,text='Download Agreement',borderwidth=0, bg=side_bar_color,activebackground='#006600', activeforeground='#3D0C02', font='-family {Cascadia Code} -size 12 -weight bold', command=Agreement_download)
ag_d.place(relx=0.4,rely=0.3,relwidth=0.2, relheight=0.05)
changeOnHover(ag_d, '#C2B280', side_bar_color)






# ========================================= notice_board_frame =========================================================
notice_board_frame = tk.Frame(root, bg='#26282A')
notice_board_frame.place(relx=0.155, relheight=1, relwidth=0.845)

mycursor.execute("SELECT * FROM hostel.notice_board;")
notice_output = mycursor.fetchall()
i = len(notice_output) - 1

def next():
    global i
    i = i + 1
    if i < len(notice_output) and i != len(notice_output):
       message_n = notice_output[i][1]
       text_box.configure(state='normal')
       text_box.delete(1.0, 'end')
       text_box.insert(0.1, message_n)
       text_box.configure(state='disabled')
       notice_date.config(text=notice_output[i][2])
       return
    i = i - 1

def prev():
    global i
    i = i - 1
    if i > 0 or i == 0:
        message_n = notice_output[i][1]
        text_box.configure(state='normal')
        text_box.delete(1.0, 'end')
        text_box.insert(0.1, message_n)
        text_box.configure(state='disabled')
        notice_date.config(text=notice_output[i][2])
        return
    i = i + 1
try:
    date_n = notice_output[i][2]
    message_n = notice_output[i][1]
except:
    date_n = ''
    message_n = ''

notice_frame_1 = tk.Frame(notice_board_frame, bg='#343434', padx=9, pady=9)
notice_frame_1.place(relx=0.1, rely=0.05, relheight=0.8, relwidth=0.6)
notice_date = tk.Label(notice_frame_1, text=f'{date_n}', bg='#343434', anchor='w', font='-family {Times New Roman} -size 12', fg='yellow')
notice_date.place(relx=0.01,rely=0, relwidth=0.3, relheight=0.03)
text_box = tk.Text(notice_frame_1, borderwidth=0, height=12, width=40, wrap='word', fg='white', bg='#353839', font='-family {Courier New} -size 12')
text_box.place(relx=0.01, rely=0.0331, relwidth=0.98, relheight=0.95)
text_box.insert('end', message_n)
text_box.configure(state='disabled')
pr_b = tk.Button(notice_board_frame, text='Prev', borderwidth=0,  bg=side_bar_color, activebackground='#CAE00D', font='-family {Times New Roman} -size 12', command=prev)
pr_b.place(relx=0.581, rely=0.86, relwidth=0.054, relheight=0.03)
ne_b = tk.Button(notice_board_frame, text='Next', borderwidth=0,bg=side_bar_color, activebackground='#CAE00D', font='-family {Times New Roman} -size 12', command=next)
ne_b.place(relx=0.65, rely=0.86, relwidth=0.054, relheight=0.03)
changeOnHover(pr_b, '#009B7D', side_bar_color )
changeOnHover(ne_b, '#009B7D', side_bar_color)



# ========================================= visitor_log_frame===========================================================

def invite():
            def close(frame):
                 frame.destroy()


            def insert_guest(v_name,v_phone_no, v_national_id, v_cal_date):
                if v_name != '':
                    if  v_phone_no != 0:
                        if v_national_id != 0:

                                mycursor.execute("insert into hostel.visitors_log (visitor_name, phone_number, visitor_national_id, Date, student_id) values( %s, %s, %s, %s, %s);",[v_name,v_phone_no, v_national_id, v_cal_date,student_id])
                                mydb.commit()
                                stut1 = tk.Label(visitor_log_frame, text='SUCCESSFUL:\n\n invitation successful',bg='#3FFF00', fg='#000000', font='-family {Georgia}  -size 10 -slant italic')
                                stut1.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
                                stut1.after(4100, lambda: stut1.place_forget())
                else:
                        stut1 = tk.Label(visitor_log_frame, text='ERROR:\n\n Fill All Entry', bg='#FF0000', fg='#000000', font='-family {Georgia}  -size 10 -slant italic')
                        stut1.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
                        stut1.after(4100, lambda: stut1.place_forget())

            visitor_name = tk.StringVar()
            visitor_phone_no = tk.IntVar()
            visitor_national_id = tk.IntVar()
            check_in_time = tk.IntVar()
            check_out_time = tk.IntVar()
            invite = tk.Frame(visitor_log_frame, bg='#1C1C1C')
            invite.place(relheight=0.43, relwidth=0.65, relx=0.17, rely=0.2)
            tk.Button(invite, text='X', fg='#4B3621', activebackground='#1C1C1C', activeforeground='red', bg='#1C1C1C', borderwidth=0, font='-family {Forte} -size 23 -weight bold', command= lambda:close(invite)).place(relx=0.898, relwidth=0.1, relheight=0.112)
            tk.Label(invite, bg='#1C1C1C', fg=side_bar_color, text='----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------',font='-size 12 ').place(relx=0.01, rely=0.11, relwidth=1, relheight=0.03)
            tk.Label(invite, text='Guest Name', anchor='w', fg='white', bg='#1C1C1C', font='-family {Georgia} -size 14 -weight bold').place(relx=0.01, rely=0.15, relwidth=0.35, relheight=0.06)
            opr1 = tk.Entry(invite, textvariable=visitor_name, borderwidth=0, bg='#292929', fg='white', font='-family {Calibri} -size 10')
            opr1.place(relx=0.01, rely=0.21, relwidth=0.35, relheight=0.07)
            changeOnHover(opr1, '#555D50', '#292929')
            tk.Label(invite, text='Guest number', anchor='w', fg='white', bg='#1C1C1C', font='-family {Georgia} -size 14 -weight bold').place(relx=0.01, rely=0.37, relwidth=0.35, relheight=0.06)
            opr2 = tk.Entry(invite, textvariable=visitor_phone_no, borderwidth=0, bg='#292929', fg='white', font='-family {Calibri} -size 10')
            opr2.place(relx=0.01, rely=0.43, relwidth=0.35, relheight=0.07)
            changeOnHover(opr2, '#555D50', '#292929')
            tk.Label(invite, text='Guest national_id', anchor='w', fg='white', bg='#1C1C1C', font='-family {Georgia} -size 14 -weight bold').place(relx=0.01, rely=0.58, relwidth=0.35, relheight=0.05)
            opr3 = tk.Entry(invite, textvariable=visitor_national_id, borderwidth=0, bg='#292929', fg='white', font='-family {Calibri} -size 10')
            opr3.place(relx=0.01, rely=0.63, relwidth=0.35, relheight=0.07)
            changeOnHover(opr3, '#555D50', '#292929')

            tk.Label(invite, text='Check in Time', anchor='w', fg='white', bg='#1C1C1C', font='-family {Georgia} -size 14 -weight bold').place(relx=0.6, rely=0.15, relwidth=0.35, relheight=0.06)
            opr4 = tk.Entry(invite, borderwidth=0,textvariable=check_in_time, bg='#292929', fg='white', font='-family {Calibri} -size 10')
            opr4.place(relx=0.6, rely=0.21, relwidth=0.35, relheight=0.07)
            changeOnHover(opr4, '#555D50', '#292929')
            tk.Label(invite, text='Check Out Time', anchor='w', fg='white', bg='#1C1C1C', font='-family {Georgia} -size 14 -weight bold').place(relx=0.6, rely=0.37, relwidth=0.35, relheight=0.06)
            opr5 = tk.Entry(invite, borderwidth=0, textvariable=check_out_time, bg='#292929', fg='white', font='-family {Calibri} -size 10')
            opr5.place(relx=0.6, rely=0.43, relwidth=0.35,relheight=0.07)
            changeOnHover(opr5, '#555D50', '#292929')
            tk.Label(invite, text='Date', anchor='w', fg='white', bg='#1C1C1C', font='-family {Georgia} -size 14 -weight bold').place(relx=0.6, rely=0.58, relwidth=0.35, relheight=0.05)
            cal_date = DateEntry(invite, borderwidth=0, bg='#292929', fg='white', font='-family {Calibri} -size 12')
            cal_date.place(relx=0.6, rely=0.63, relwidth=0.35, relheight=0.07)
            changeOnHover(cal_date, '#555D50', '#292929')
            uir = tk.Button(invite, text='Confirm', borderwidth=0, bg='pink', activebackground='#3FFF00',fg='white', font='-family {Forte} -size 12', command= lambda :insert_guest(visitor_name.get(),visitor_phone_no.get(), visitor_national_id.get(), cal_date.get_date()))
            uir.place(relx=0.88, rely=0.9, relwidth=0.1, relheight=0.08)
            changeOnHover(uir, '#006600', 'pink')

visitor_log_frame = tk.Frame(root, bg='#26282A')
visitor_log_frame.place(relx=0.155, relheight=1, relwidth=0.845)

v_frame1 = tk.Frame(visitor_log_frame, bg='#212122')
v_frame1.place(relheight=0.5, relwidth=0.8,relx=0.1, rely=0.05)
gut = tk.Button(v_frame1, text='invite Guest', borderwidth=0, bg='pink', fg='black', font='-family {Cascadia Mono ExtraLight} -size 10', command=invite)
gut.place(relx=0.82, rely=0.03, relwidth=0.15, relheight=0.06)
changeOnHover(gut, '#009B7D', 'pink')
v_frame1_1 = tk.Frame(v_frame1, bg='#351E1C')
v_frame1_1.place(relx=0.03, rely=0.15, relwidth=0.94, relheight=0.05)
tk.Label(v_frame1_1, bg='#351E1C', text='Visitor Name', borderwidth=0, fg='white', font='-family {Forte} -size 12').place(relx=0, relheight=1, relwidth=0.2 )
tk.Label(v_frame1_1, bg='#351E1C', text='Phone No', borderwidth=0, fg='white', font='-family {Forte} -size 12').place(relx=0.26, relheight=1, relwidth=0.2)
tk.Label(v_frame1_1, bg='#351E1C', text='National Id', borderwidth=0, fg='white', font='-family {Forte} -size 12').place(relx=0.52, relheight=1, relwidth=0.2)
tk.Label(v_frame1_1, bg='#351E1C', text='Date', borderwidth=0, fg='white', font='-family {Forte} -size 12').place(relx=0.78, relheight=1, relwidth=0.2)


def visitor_log():
    show_v = tk.Frame(v_frame1, bg='#212122')
    show_v.place(relheight=0.73, relwidth=0.95, relx=0.027, rely=0.23)

    canvas = tk.Canvas(show_v, bg='#212122')
    canvas.place(relwidth=1, relheight=1)

    vbar = tk.Scrollbar(show_v, orient=tk.VERTICAL, command=canvas.yview)
    vbar.place(relheight=1, relwidth=0.1, relx=0.98)

    canvas.configure(yscrollcommand=vbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    canvas.configure(yscrollcommand=vbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    sec_frame = tk.Frame(canvas, bg='#212122')

    canvas.create_window((0, 0), window=sec_frame)


    mycursor.execute("SELECT * FROM hostel.visitors_log where student_id = %s;", [student_id])
    visitor_logs = mycursor.fetchall()
    j = len(visitor_logs)
    i = j - 1
    h = 0
    global row
    row = 0
    while j != 0:
      tk.Label(sec_frame, bg='#212122', text=f"{visitor_logs[i][0]}", anchor='w',  borderwidth=0, fg='white', font='-family {Calibri} -size 12').grid(row = h, column=1, pady=10, padx=50) #place(relx=0.03, rely=h, relheight=0.05, relwidth=0.19)
      tk.Label(sec_frame, bg='#212122', text=f"(+254) {visitor_logs[i][1]}",  borderwidth=0, fg='white', font='-family {Courier New} -size 12').grid(row = h, column=2, pady=10, padx=70) #.place(relx=0.275, rely=h, relheight=0.05, relwidth=0.19)
      tk.Label(sec_frame, bg='#212122', text=f"{visitor_logs[i][2]}",  borderwidth=0, fg='white', font='-family {Courier New} -size 12').grid(row = h, column=3, pady=10, padx=70) #.place(relx=0.52, rely=h, relheight=0.05, relwidth=0.19)
      tk.Label(sec_frame, bg='#212122', text=f"{visitor_logs[i][5]}",  borderwidth=0, fg='white', font='-family {Consolas} -size 11').grid(row = h, column=4, pady=10, padx=90) #.place(relx=0.765, rely=h, relheight=0.05, relwidth=0.19)
      h = h + 1
      j = j - 1
      i = i -1

visitor_log()


# ============================================ Complaint_frame =========================================================

Complaint_frame = tk.Frame(root, bg='#26282A')
Complaint_frame.place(relx=0.155, relheight=1, relwidth=0.845)

def submit_complaint():

    message = text_box_complaint.get(1.0, 'end')
    print(message)
    print(len(message))

    if len(message) > 30:
            mycursor.execute("INSERT INTO hostel.complaint  (student_id, complaint_massage, status) VALUES ( %s, %s, 'pending')", [student_id, message])
            mydb.commit()
            stut1 = tk.Label(Complaint_frame, text=' Success:\n\n submission complited', bg='#A4C639', fg='#000000', font='-family {Georgia}  -size 10 -slant italic')
            stut1.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
            stut1.after(3100, lambda: stut1.place_forget())
    else:
            stut1 = tk.Label(Complaint_frame, text='✗ Error:\n\n complitent didn\'t submit \n less than 30 words', bg='#F08080', fg='#000000', font='-family {Georgia}  -size 10 -slant italic')
            stut1.place(relx=0.7, rely=0.04, relwidth=0.25, relheight=0.09)
            stut1.after(3100, lambda: stut1.place_forget())

def clear_complaint():
    text_box_complaint.delete(1.0, 'end')


Complaint_section_n1 = tk.LabelFrame(Complaint_frame, text="Message", bg='#26282A', fg="green", font='-family {Georgia} -size 14 -weight bold')
Complaint_section_n1.place(relx=0.14, rely=0.08, relheight=0.6, relwidth=0.75)

text_box_complaint = tk.Text(Complaint_section_n1, bg='#26282A',fg='white', height=12, width=40, wrap='word', borderwidth=10, font='-family {Times New Roman} -size 12')
text_box_complaint.place(relwidth=1, relheight=1)
changeOnHover(text_box_complaint, '#354230', '#26282A')

c_cl = tk.Button(Complaint_frame, text="Clear", bg=side_bar_color, command=clear_complaint, font='-family {Algerian} -size 10')
c_cl.place(rely=0.7, relx=0.76, relwidth=0.06, relheight=0.03)
c_sub = tk.Button(Complaint_frame, text="Submit", bg=side_bar_color,command=submit_complaint, font='-family {Algerian} -size 10')
c_sub.place(rely=0.7, relx=0.83, relwidth=0.06, relheight=0.03)
changeOnHover(c_cl, '#CD5C5C', side_bar_color)
changeOnHover(c_sub, '#354230', side_bar_color)

# ============================================ Financials Frame ========================================================

Financials_frame = tk.Frame(root,  bg='#26282A')
Financials_frame.place(relx=0.155, relheight=1, relwidth=0.845)

financial_frame1 = tk.Frame(Financials_frame, bg="#212122")
financial_frame1.place(relx=0.04,rely=0.1, relwidth=0.5, relheight=0.2)
tk.Label(financial_frame1, text='Your Wallet', anchor='w', bg="#212122",fg="green", font='-family {Georgia} -size 10 -weight bold').place(relx=0.02,rely=0,relheight=0.2,relwidth=1)
tk.Label(financial_frame1, text='Ksh: ', anchor='w',bg="#212122", fg="gold", font='-family {Algerian} -size 16 -weight bold').place(relx=0.02,rely=0.21,relheight=0.2,relwidth=1)
t_box = tk.Text(financial_frame1, wrap='word',bg="#212122", fg="white",borderwidth=0,font = ('Candara Light', 11))
t_box.insert('end',"Available balance\nYour Wallet is the rent advance that we are keeping safe with us for you. You can recharge your Wallet any time by clicking on Make Payment")
t_box.config(state='disabled')
t_box.place(relx=0.02,rely=0.42,relheight=0.55,relwidth=0.81)

financial_frame2 = tk.Frame(Financials_frame, bg="#212122")
financial_frame2.place(relx=0.6,rely=0.1, relwidth=0.34, relheight=0.2)
tk.Label(financial_frame2, text='Amount Deposited', anchor='w', bg="#212122",fg="green", font='-family {Georgia} -size 10 -weight bold').place(relx=0.02,rely=0,relheight=0.2,relwidth=1)
tk.Label(financial_frame2, text='Ksh: ', anchor='w',bg="#212122", fg="gold", font='-family {Algerian} -size 16 -weight bold').place(relx=0.02,rely=0.21,relheight=0.2,relwidth=1)
t_box1 = tk.Text(financial_frame2, wrap='word',bg="#212122", fg="white",borderwidth=0,font = ('Candara Light', 11))
t_box1.insert('end', "Deposit amount will be returned on the checkout date after the necessary deductions.*\n*Conditions Apply")
t_box1.config(state='disabled')
t_box1.place(relx=0.02,rely=0.42,relheight=0.55,relwidth=0.81)

def make_payment():
    def close_f(f):
        f.destroy()

    import requests
    import base64
    from requests.auth import HTTPBasicAuth
    import datetime
    def conf_pay(tans_id, t_discription, tby):
                if tans_id != '':
                    tans_id = tans_id.upper()
                    mycursor.execute("Insert into hostel.payment (Student_id, Room_id, mpesa_transaction_id, payment_for, Payment_status, tansaction_date) VALUES (%s, %s, %s, %s,'pending', CURDATE());", [student_id, room_id, tans_id, t_discription])
                    mydb.commit()
                    tby.config(text='√', borderwidth=0, fg='green', font='-family {Forte} -size 13 -weight bold')
                    tby['state'] = tk.DISABLED

    def mpesa_pay(r_amount, r_phone, r_for):
        if r_amount != '' and r_amount.isnumeric():
                    tk.Label(yur, text='√', fg="green", bg='#1C1C1C', font='-family {Forte} -size 13 -weight bold').place(relx=0.861, rely=0.3, relheight=0.1, relwidth=0.1)
                    if r_phone != '' and r_phone.isnumeric():
                                tk.Label(yur, text='√', fg="green", bg='#1C1C1C',font='-family {Forte} -size 13 -weight bold').place(relx=0.861, rely=0.43,relheight=0.1, relwidth=0.1)
                                if r_for != '':
                                            tk.Label(yur, text='√', fg="green", bg='#1C1C1C',font='-family {Forte} -size 13 -weight bold').place(relx=0.861, rely=0.56, relheight=0.1,relwidth=0.1)
                                            consumer_key = "j03STGaUVRui7xJahkgHOcRGkGcGNpf4"  # Consumer Key from safaricom
                                            consumer_secret = "XnnIXhtJ8H8zeRHC"  # Consumer Secret from safaricom
                                            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

                                            r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
                                            response = r.json()
                                            access_token = response['access_token']
                                            requests_amount = r_amount  # Mount to request
                                            phone = r_phone  # Recipient phone number
                                            saa = datetime.datetime.now()
                                            timestamp_format = saa.strftime("%Y%m%d%H%M%S")

                                            businessshortcode = "174379"
                                            passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"  # pass_key from safaricom
                                            pd_decode = businessshortcode + passkey + timestamp_format
                                            ret = base64.b64encode(pd_decode.encode())
                                            pd = ret.decode('utf-8')

                                            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
                                            headers = {"Authorization": "Bearer %s" % access_token}

                                            request = {
                                                "BusinessShortCode": businessshortcode,  # # Paybill or Buygoods - account number
                                                "Password": pd,  # password used for encrypting the request sent
                                                "Timestamp": timestamp_format,
                                                # Timestamp of the transaction, normaly in the formart of YEAR+MONTH+DATE+HOUR+MINUTE+SECOND (YYYYMMDDHHMMSS)
                                                "TransactionType": "CustomerPayBillOnline",
                                                # used to identify the transaction when sending the request to M-Pesa (CustomerPayBillOnline, CustomerBuyGoodsOnline)
                                                "Amount": requests_amount,  # Money that customer pays to the Shorcode. Only whole numbers are supported
                                                "PartyA": phone,  # The phone number sending money
                                                "PartyB": businessshortcode,  # businessshortcode, # The organization receiving the funds
                                                "PhoneNumber": phone,  # Mobile Number to receive the STK Pin Prompt
                                                "CallBackURL": "https://6a1e-102-68-77-69.eu.ngrok.io/MPESA_TEST/MpesaTest.php",
                                                # "https://41.139.244.238:80/callback", # valid secure URL that is used to receive notifications from M-Pesa API. It is the endpoint to which the results will be sent by M-Pesa API.
                                                "AccountReference": "28774056",
                                                "TransactionDesc": r_for
                                                # information/comment that can be sent along with the request from your system.
                                            }
                                            response = requests.post(api_url, json=request, headers=headers)
                                            if response.status_code == 400:
                                                        tuy = tk.Label(yur, text='Error Initiating the transaction: \n invalid Phone number or No internet-connection', bg='#1C1C1C', fg='red', font='-family {Times New Roman} -size 11 -weight bold')
                                                        tuy.place(relx=0.0, rely=0.83, relheight=0.15, relwidth=1)
                                                        tuy.after(11100, lambda: tuy.place_forget())
                                            elif response.status_code == 200:
                                                        tans_id = tk.StringVar()
                                                        tk.Label(yur, text='Trasaction Code:', bg='#1C1C1C', borderwidth=0, fg=side_bar_color).place(relx=0.03, rely=0.02, relheight=0.1, relwidth=0.22)
                                                        tk.Entry(yur, borderwidth=0, textvariable=tans_id).place(relx=0.26, rely=0.02, relheight=0.1, relwidth=0.35)
                                                        tui = tk.Button(yur, text='Ok', bg='#1C1C1C', activebackground=side_bar_color,fg='green', activeforeground='black', font='-family {Time New Roman} -size 13 -weight bold', command=lambda: conf_pay(tans_id.get(), pay_for.get(), tui))
                                                        tui.place(relx=0.62, rely=0.02,relheight=0.1, relwidth=0.1)

                                                        uio = tk.Label(yur, text='Transaction Process initiated, check your phone and Confirm', bg='#1C1C1C', fg='green', font='-family {Times New Roman} -size 11 -weight bold')
                                                        uio.place(relx=0.0, rely=0.83, relheight=0.15, relwidth=1)
                                                        uio.after(11100, lambda: uio.place_forget())
                                            else:
                                                        urio = tk.Label(yur,text='System Error: unknown error from Mpesa \n try again after a few minutes', bg='#1C1C1C', fg='brown',font='-family {Times New Roman} -size 11 -weight bold')
                                                        urio.place(relx=0.0, rely=0.83, relheight=0.15, relwidth=1)
                                                        urio.after(11100, lambda: urio.place_forget())
                                else:
                                    tk.Label(yur, text='X', fg="red", bg='#1C1C1C', font='-family {Forte} -size 13 -weight bold').place(relx=0.861, rely=0.56, relheight=0.1, relwidth=0.1)
                    else:
                        tk.Label(yur, text='X', fg="red", bg='#1C1C1C', font='-family {Forte} -size 13 -weight bold').place(relx=0.861, rely=0.43, relheight=0.1, relwidth=0.1)
        else:
            tk.Label(yur, text='X', fg="red", bg='#1C1C1C', font='-family {Forte} -size 13 -weight bold').place(relx=0.861, rely=0.3, relheight=0.1, relwidth=0.1)

    pay_amount = tk.StringVar()
    pay_amount.set('1')
    pay_phone_no = tk.StringVar()
    pay_phone_no.set(f'254{phone_no}')
    pay_for = tk.StringVar()
    pay_for.set('Rent')
    yur = tk.Frame(Financials_frame,  bg='#1C1C1C')
    yur.place(relx=0.26, rely=0.33, relwidth=0.47, relheight=0.3)
    tk.Button(yur, text='X', fg='#4B3621', activebackground='#1C1C1C', activeforeground='red', bg='#1C1C1C',borderwidth=0, font='-family {Forte} -size 23 -weight bold', command=lambda: close_f(yur)).place(relx=0.898, relwidth=0.1, relheight=0.112)
    tk.Label(yur, fg=side_bar_color, bg='#1C1C1C',text='---------------------------------------------------------------------------------------------', font='-size 13').place(relx=0,relwidth=1, relheight=0.04, rely=0.13)

    tk.Label(yur,text='Amount :',anchor='w',bg='#1C1C1C', fg='white',  font='-family {Georgia} -size 11 -weight bold').place(relx=0.03, rely=0.3, relheight=0.1, relwidth=0.25)
    pa = tk.Entry(yur, textvariable=pay_amount, borderwidth=0, bg='#4B3621',fg='white', font='-family {Cascadia Code} -size 13 -slant italic')
    pa.place(relx=0.3, rely=0.3, relheight=0.1, relwidth=0.56)
    changeOnHover(pa, side_bar_color, '#4B3621')

    tk.Label(yur, text='Phone No :', anchor='w',bg='#1C1C1C', fg='white', font='-family {Georgia} -size 11 -weight bold').place(relx=0.03, rely=0.43, relheight=0.1, relwidth=0.25)
    pa1 = tk.Entry(yur,textvariable=pay_phone_no, borderwidth=0, bg='#4B3621',fg='white', font='-family {Cascadia Code} -size 13 -slant italic' )
    pa1.place(relx=0.3, rely=0.43, relheight=0.1, relwidth=0.56)
    changeOnHover(pa1, side_bar_color, '#4B3621')

    tk.Label(yur, text='For :', anchor='w',bg='#1C1C1C', fg='white',font='-family {Georgia} -size 11 -weight bold').place(relx=0.03, rely=0.56, relheight=0.1, relwidth=0.25)
    pa2 = tk.Entry(yur, textvariable=pay_for, borderwidth=0, bg='#4B3621',fg='white', font='-family {Cascadia Code} -size 12 -slant italic')
    pa2.place(relx=0.3, rely=0.56, relheight=0.1, relwidth=0.56)
    changeOnHover(pa2, side_bar_color, '#4B3621')

    pa_b = tk.Button(yur, text='Transact', bg=side_bar_color, borderwidth=0, activebackground='#0B6623', activeforeground='gold', font='-family {Georgia} -size 11 -weight bold', command= lambda : mpesa_pay(pay_amount.get(), pay_phone_no.get(), pay_for.get()))
    pa_b.place(relx=0.4, rely=0.69,relheight=0.1, relwidth=0.25)
    changeOnHover(pa_b, '#004B49', side_bar_color)


tpry = tk.Button(Financials_frame, bg=side_bar_color , activebackground='green',activeforeground='gold', text="Make Payment", font='-family {Georgia} -size 11 -weight bold', command=make_payment)
tpry.place(relwidth=0.15,relheight=0.05, rely=0.33, relx=0.425)
changeOnHover(tpry, '#C2B280', side_bar_color)

def re():
            def refresh():
                show_v.destroy()
                sec_frame.destroy()
                canvas.destroy()
                vbar.destroy()
                re()
            show_v = tk.Frame(show_tran_f, bg='#212122')
            show_v.place(relheight=0.73, relwidth=0.97, relx=0.025, rely=0.19)

            canvas = tk.Canvas(show_v, bg='#212122')
            canvas.place(relwidth=1, relheight=1)

            vbar = tk.Scrollbar(show_v, orient=tk.VERTICAL, command=canvas.yview, bg=side_bar_color)
            vbar.place(relheight=1, relwidth=0.1, relx=0.98)

            canvas.configure(yscrollcommand=vbar.set)
            canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

            canvas.configure(yscrollcommand=vbar.set)
            canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

            sec_frame = tk.Frame(canvas, bg='#212122')

            canvas.create_window((0,0), window=sec_frame)

            mycursor.execute('SELECT * FROM hostel.payment where Student_id = %s;',[student_id])
            payment_out = mycursor.fetchall()

            j = len(payment_out)
            i = j - 1
            h = 0
            global row
            row = 0
            while j != 0:
                      tk.Label(sec_frame, bg='#212122', text=f"{payment_out[i][0]}", anchor='w',   borderwidth=0, fg='white', font='-family {Calibri} -size 12').grid(row = h, column=1, pady=10, padx=80) #place(relx=0.03, rely=h, relheight=0.05, relwidth=0.19)
                      tk.Label(sec_frame, bg='#212122', text=f"{payment_out[i][6]}",  borderwidth=0, fg='white', font='-family {Consolas} -size 11').grid(row = h, column=2, pady=10, padx=80) #.place(relx=0.765, rely=h, relheight=0.05, relwidth=0.19)
                      tk.Label(sec_frame, bg='#212122', text=f"{payment_out[i][3]}",  borderwidth=0, fg='white', font='-family {Courier New} -size 12').grid(row = h, column=3, pady=10, padx=80) #.place(relx=0.275, rely=h, relheight=0.05, relwidth=0.19)
                      tk.Label(sec_frame, bg='#212122', text=f"{payment_out[i][4]}",  borderwidth=0, fg='white', font='-family {Courier New} -size 12').grid(row = h, column=4, pady=10, padx=90) #.place(relx=0.52, rely=h, relheight=0.05, relwidth=0.19)
                      if payment_out[i][5] == 'pending':
                          tk.Label(sec_frame, bg='#212122', text=f"{payment_out[i][5]}",  borderwidth=0, fg='pink', font='-family {Consolas} -size 12 -weight bold').grid(row = h, column=5, pady=10, padx=80) #.place(relx=0.765, rely=h, relheight=0.05, relwidth=0.19)
                      elif payment_out[i][5] == 'complete':
                          tk.Label(sec_frame, bg='#212122', text=f"{payment_out[i][5]}", borderwidth=0, fg='green', font='-family {Consolas} -size 12 -weight bold').grid(row=h, column=5, pady=10, padx=80)  # .place(relx=0.765, rely=h, relheight=0.05, relwidth=0.19)
                      else:
                          tk.Label(sec_frame, bg='#212122', text=f"{payment_out[i][5]}", borderwidth=0, fg='red', font='-family {Consolas} -size 12 -weight bold').grid(row=h, column=5, pady=10, padx=80)  # .place(relx=0.765, rely=h, relheight=0.05, relwidth=0.19)

                      h = h + 1
                      j = j - 1
                      i = i -1
            tk.Button(show_tran_f, text='↻', bg='gold', font='-size 10', borderwidth=0, command=lambda: refresh()).place(rely=0.05,relx=0.95, relheight=0.1, relwidth=0.05)



show_tran_f = tk.Frame(Financials_frame, bg="#212122")
show_tran_f.place(rely=0.5,relx=0.05, relheight=0.34, relwidth=0.9)

N_BAR = tk.Frame(show_tran_f, bg='gold')
N_BAR.place(rely=0.05, relx=0, relheight=0.1, relwidth=1)
tk.Label(N_BAR, text='PAYMENT ID', bg='gold', font='-family {Forte} -size 11').place(rely=0, relx=0.03, relheight=1, relwidth=0.14)
tk.Label(N_BAR, text='DATE', bg='gold', font='-family {Forte} -size 12').place(rely=0, relx=0.18, relheight=1, relwidth=0.14)
tk.Label(N_BAR, text='TRANSACTION ID', bg='gold', font='-family {Forte} -size 11').place(rely=0, relx=0.36, relheight=1, relwidth=0.25)
tk.Label(N_BAR, text='PAYMENT FOR', bg='gold', font='-family {Forte} -size 12').place(rely=0, relx=0.64, relheight=1, relwidth=0.15)
tk.Label(N_BAR, text='PAYMENT STATUS', bg='gold', font='-family {Forte} -size 11').place(rely=0, relx=0.81, relheight=1, relwidth=0.16)


re()

root.mainloop()





