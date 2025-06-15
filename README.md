
# 🧾 Check-Out Register (Employee Time Tracking System)

A PyQt5-based **Check-In/Check-Out Register System** that tracks employee attendance using a secure PIN system. Ideal for educational institutions, offices, or labs where quick and visual tracking of employee activity is essential.

---

## 🎯 Features

- 🔐 **PIN-Protected Logins** for employees and admin  
- ➕ **Add New Employees** with admin verification  
- ✅ **Check-In / Check-Out** with timestamp logging  
- 📝 **Custom Check-Out Message Input**  
- 🔁 **Change PIN Functionality**  
- 🧾 **Automatic MySQL Logging** of actions  
- 🖼️ Clean GUI with background imagery and intuitive layout  
- 📚 **Separate tables** for employees and check-in/out status  

---



## 🛠️ Tech Stack

| Tech       | Purpose           |
|------------|-------------------|
| Python     | Core logic        |
| PyQt5      | GUI framework     |
| MySQL      | Data storage      |
| QSS        | GUI styling       |
| JSON       | Config handling   |

---

---

## ⚙️ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/Check-Out-Register.git
cd Check-Out-Register
```
2. **Install Dependencies**

```bash
pip install -r requirements.txt

```
2. **Configure MySQL and Admin PIN**

```json
{
  "host": "localhost",
  "username": "your_mysql_user",
  "password": "your_mysql_password",
  "database": "your_database_name",
  "admin": "1234"
}

```
2. **Run The App**

```bash
python main.py


```

---

## 🔐 Admin Controls

- The **Admin PIN** is required to access restricted features like **adding new employees**.
- The admin PIN is securely stored in `resources/dbinfo.json`.
- New employees are assigned a **default PIN of `1234`**, which they can change after login.

---

## 🗃️ Database Tables

### `employee_table`

| Column   | Type                   | Description              |
|----------|------------------------|--------------------------|
| SN       | INT (AUTO_INCREMENT)   | Unique employee ID       |
| Name     | TEXT                   | Full name of employee    |
| Password | TEXT                   | 4-digit PIN (string)     |

### `checkInOut`

| Column           | Type     | Description                          |
|------------------|----------|--------------------------------------|
| SN               | INT      | Employee ID (foreign key)            |
| Name             | TEXT     | Full name of employee                |
| CheckOut_Status  | BOOLEAN  | `True` if checked out                |
| CheckOut_Message | TEXT     | Reason for checking out              |
| CheckIn_Time     | DATETIME | Timestamp of last check-in           |
| CheckOut_Time    | DATETIME | Timestamp of last check-out          |

---

## 🤝 Contributions

Contributions are welcome!  
If you’d like to add features, fix bugs, or improve the UI/UX, feel free to:

- Fork this repo
- Create a new branch
- Make your changes
- Open a pull request 🎉

Found a bug? Open an issue.

---

## 📜 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute this software with proper attribution.

---

## 👨‍💻 Author

**Manish Dhakal**  
GitHub: [@manishdhakal2](https://github.com/manishdhakal2)  


---






