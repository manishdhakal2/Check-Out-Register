🧾 Check-Out Register (Employee Time Tracking System)
A PyQt5-based Check-In/Check-Out Register System that tracks employee attendance using a secure PIN system. Ideal for educational institutions, offices, or labs where quick and visual tracking of employee activity is essential.

🎯 Features
🔐 PIN-Protected Logins for employees and admin

➕ Add New Employees with admin verification

✅ Check-In / Check-Out with timestamp logging

📝 Custom Check-Out Message Input

🔁 Change PIN Functionality

🧾 Automatic MySQL Logging of actions

🖼️ Clean GUI with background imagery and intuitive layout

📚 Separate tables for employees and check-in/out status

🖼️ Screenshots
(Add screenshots from the app here showing: main window, check-in screen, PIN entry dialog, etc.)

🛠️ Tech Stack
Tech	Purpose
Python	Core language
PyQt5	GUI framework
MySQL	Database backend
QSS	Styling GUI elements
JSON	Secure config loading

📁 Folder Structure
pgsql
Copy
Edit
Check-Out-Register/
├── main.py
├── resources/
│   ├── icon.ico
│   ├── background.jpg
│   ├── show.png
│   ├── hide.png
│   ├── addProfile.png
│   ├── collegeLogo.png
│   └── dbinfo.json   # contains DB credentials and admin pin
├── README.md
└── requirements.txt
⚙️ Setup Instructions
Clone the repo

bash
Copy
Edit
git clone https://github.com/yourusername/Check-Out-Register.git
cd Check-Out-Register
Install required packages

bash
Copy
Edit
pip install -r requirements.txt
Set up your MySQL database

Create a MySQL database and user.

Create a file resources/dbinfo.json with the following format:

json
Copy
Edit
{
  "host": "localhost",
  "username": "your_mysql_user",
  "password": "your_mysql_password",
  "database": "your_database_name",
  "admin": "1234"
}
Run the app

bash
Copy
Edit
python main.py
🔐 Admin Controls
Admin PIN is required to add new employees.

Default employee password is 1234, and employees can change their PIN later.

📌 Database Tables
employee_table
Column	Type
SN	INT (PK, AUTO_INCREMENT)
Name	TEXT
Password	TEXT

checkInOut
Column	Type
SN	INT
Name	TEXT
CheckOut_Status	BOOLEAN
CheckOut_Message	TEXT
CheckIn_Time	DATETIME
CheckOut_Time	DATETIME

🤝 Contributions
Pull requests and feedback are welcome! If you have feature suggestions or encounter bugs, open an issue.

📜 License
This project is licensed under the MIT License.

👨‍💻 Author
Manish Dhakal
GitHub: @manishdhakal2

