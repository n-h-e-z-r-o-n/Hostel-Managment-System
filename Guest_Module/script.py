#!C:\Users\HEZRON WEKESA\AppData\Local\Programs\Python\Python310\python.exe
print("Content-Type: text/html")
print()
print('<html>')
print('<body>')

import cgi,cgitb
cgitb.enable()
form = cgi.FieldStorage()
#receive  values from user form and trim white spaces
guest_name = form.getvalue('guest_name')
guest_phone_number = form.getvalue('guest_phone_number')
guest_email = form.getvalue('guest_email')
guest_room_type = form.getvalue('guest_room_type')


import json
# Data to be written
dictionary ={
    "Guest_name" : guest_name,
    "Guest_Phone" : guest_phone_number,
    "Guest_Email" : guest_email,
    "Guest_room" : guest_room_type
}


with open('guest_detail.json') as json_file:
    data = json.load(json_file)

temp = data['Guests']
temp.append(dictionary)
with open('guest_detail.json','w') as json_file_write:
   json.dump(data,json_file_write, indent=4)

print('<h1 style="text-align: center; display: flex; flex-direction: column; justify-content: center;"> You Have Been Added Successfuly in The Booking List</h1>')

print('</body>')

print('</html>')
