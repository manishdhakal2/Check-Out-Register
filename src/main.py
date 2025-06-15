from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QVBoxLayout, QLayout, QHBoxLayout, QPushButton, QLineEdit, QApplication, QScrollArea, QSpacerItem, QSizePolicy, QTextEdit, QStackedLayout
from PyQt5.QtGui import QIcon, QImage, QKeyEvent, QKeyEvent, QResizeEvent, QPixmap, QPainterPath, QRegion, QIntValidator, QPalette, QBrush
from PyQt5.QtCore import Qt, QSize, QRect, QPoint
import sys
from PyQt5.QtSvg import QSvgWidget
import MySQLdb
import json
from PyQt5.QtWidgets import QInputDialog
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox




class ClickableLabel(QLabel):
    def __init__(self, name, parent=None,func=None,cleanName=None):
        super().__init__(name, parent)
        self.name = name
        self.func=func
        self.cleanName=cleanName

    def mousePressEvent(self, ev):
        if self.func:
            self.func(ev,self.cleanName)



class AddEmployeeWindow(QWidget):
    def __init__(self,win):
        super().__init__()
        self.setWindowTitle("Add Employee")
        self.setGeometry(300, 100, 500, 400)
        self.setWindowIcon(QIcon("resources/icon.ico"))
        with open("resources/dbinfo.json", "r") as file:
            db_info = json.load(file)
        self.adminPin=db_info["admin"]
        self.win=win
        self.init_ui1()
    

    def init_ui1(self): 
        # Layout for admin password verification
        layout = QVBoxLayout()

        admin_label = QLabel("Enter Admin Pin :")
        admin_label.setStyleSheet("font-size: 18px; color: black;")
        admin_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(admin_label)

        # Password input field with show/hide icon
        pass_layout = QHBoxLayout()
        self.admin_pass_input = QLineEdit()
        self.admin_pass_input.setPlaceholderText("Admin Pin")
        validator = QIntValidator(0, 9999)
        self.admin_pass_input.setValidator(validator)
        self.admin_pass_input.setEchoMode(QLineEdit.Password)
        self.admin_pass_input.setStyleSheet("""
            QLineEdit {
            font-size: 18px;
            padding: 10px;
            border: 2px solid #FD850C;
            border-radius: 5px;
            }
            QLineEdit:focus {
            border-color: #FF9A3D;
            }
        """)
        pass_layout.addWidget(self.admin_pass_input)

        show_pass_btn = QPushButton()
        show_pass_btn.setCheckable(True)
        show_pass_btn.setFixedSize(24, 24)
        show_pass_btn.setIcon(QIcon("resources/show.png"))
        show_pass_btn.setStyleSheet("border: none;")



        def toggle_admin_pass():
            if show_pass_btn.isChecked():
                self.admin_pass_input.setEchoMode(QLineEdit.Normal)
                show_pass_btn.setIcon(QIcon("resources/hide.png"))
            else:
                self.admin_pass_input.setEchoMode(QLineEdit.Password)
                show_pass_btn.setIcon(QIcon("resources/show.png"))

        show_pass_btn.clicked.connect(toggle_admin_pass)


        pass_layout.addWidget(show_pass_btn)

        layout.addLayout(pass_layout)

        submit_btn = QPushButton("Verify")
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #FD850C;
                color: white;
                font-size: 18px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover { 
                background-color: #FF9A3D;
            }           
            QPushButton:pressed {
                background-color: #FF7A00;
            }
        """)
        def verify_admin():
            if self.admin_pass_input.text() == self.adminPin:
                self.init_ui2()
            else:
                QMessageBox.critical(self, "Access Denied", "Incorrect admin PIN.")
                self.admin_pass_input.clear()
        submit_btn.clicked.connect(verify_admin)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def init_ui2(self):
        self.clearLayout(self.layout())  # Clear the previous layout

        # Layout for the Add Employee form
        layout = QVBoxLayout()

        # Name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter employee name")
        self.name_input.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                padding: 10px;
                border: 2px solid #FD850C;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #FF9A3D;
            }
        """)
        employeeName= QLabel("Employee Name:")
        employeeName.setStyleSheet("font-size: 18px; color: black;")
        employeeName.setAlignment(Qt.AlignCenter)
        layout.addWidget(employeeName)

        layout.addWidget(self.name_input)


        # Submit button
        submit_btn = QPushButton("Add Employee")

        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #FD850C;
                color: white;
                font-size: 18px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover { 
                background-color: #FF9A3D;
            }           
            QPushButton:pressed {
                background-color: #FF7A00;
            }
        """)
        submit_btn.clicked.connect(self.add_employee_to_db)
    
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def add_employee_to_db(self):
            # Validate inputs
        name = self.name_input.text().strip()
        #Validate IF FIRST AND LAST NAME ARE PROVIDED
        if len(name.split()) < 2:
            QMessageBox.warning(self, "Input Error", "Please enter both first and last name.")
            return

        
        

        # Check if name and password are provided
        if not name:
            QMessageBox.warning(self, "Input Error", "Name Required.")
            return

        filepath = r"resources/dbinfo.json"
        try:
            with open(filepath, 'r') as file:
                db_info = json.load(file)
            dbConnection = MySQLdb.connect(
                host=db_info["host"],
                user=db_info["username"],
                passwd=db_info["password"],
                database=db_info["database"]
            )
            cursor = dbConnection.cursor()
            insert_query = "INSERT INTO employee_table (Name,Password) VALUES (%s,%s)"
            cursor.execute(insert_query, (name, "1234"))

#Logic for checking SN
            cursor.execute("SELECT * FROM employee_table WHERE Name = %s", (name,))
            result = cursor.fetchone()
            if result:
                employee_id = result[0]
                print(f"Employee ID: {employee_id}")
            else:
                QMessageBox.warning(self, "Database Error", "Failed to retrieve employee ID.")
                return
            insert_query = "INSERT INTO checkInOut (SN,Name) VALUES (%s,%s)"
            cursor.execute(insert_query, (employee_id, name))
            dbConnection.commit()
            QMessageBox.information(self, "Success", "Employee added successfully.")
            self.init_ui2()

            

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to add employee: {e}")

    #---------#

    def pinValidator(self, pin):
            # Check if the pin meets the criteria
            if len(pin) != 4:
                QMessageBox.warning(self, "PIN Error", "PIN must be exactly 4 digits long.")
                return False
            if not pin.isdigit():
                QMessageBox.warning(self, "PIN Error", "PIN must contain only digits.")
                return False
            return True
    

    def clearLayout(self, layout):
        # Remove all widgets and layouts from the given layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            child_layout = item.layout()
            if child_layout is not None:
                self.clearLayout(child_layout)
        # If this layout is the main layout of the window, unset it to avoid "already has layout" error
        if self.layout() is layout:
            QWidget().setLayout(self.layout())


#The Main Window
class MainAppWindow(QMainWindow):

    def __init__(self)->None:

        #Call the parent Constructor
        super(MainAppWindow,self).__init__()
        #Set the title
        self.setWindowTitle("CHECK-OUT REGISTER")
        self.setWindowIcon(QIcon("resources/icon.ico"))
        self.setGeometry(0,0,1280,720)
        #Run in Fullscreen
        self.showFullScreen()
        self.init_ui()
                
    def init_ui(self):
        # Create central widget and set to main window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Set layout on central widget
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create QLabel for background image as a child of central widget
        bg_label = QLabel(central_widget)
        bg_pixmap = QPixmap("resources/background.jpg")
        bg_label.setPixmap(bg_pixmap)
        bg_label.setScaledContents(True)
        bg_label.setGeometry(0, 0, self.width(), self.height())  # full size of window
        bg_label.lower()  # send to back, behind everything

        # Connect resize event to keep bg_label filling central widget
        def on_resize(event):
            bg_label.setGeometry(0, 0, central_widget.width(), central_widget.height())
            event.accept()
        central_widget.resizeEvent = on_resize

        # Now create your nav bar widget normally and add it to main_layout
        navBarLayout = QHBoxLayout()
        # -- setup nav bar buttons and labels exactly as before --
        addEmployeeButton = QPushButton()
        img = QPixmap("resources/addProfile.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        addEmployeeButton.setIcon(QIcon(img))
        addEmployeeButton.setIconSize(QSize(40, 40))
        addEmployeeButton.setStyleSheet("background-color: transparent; border: none;")
        addEmployeeButton.setFixedSize(50, 50)
        addEmployeeButton.setToolTip("Add Employee")
        addEmployeeButton.clicked.connect(lambda: self.addEmployee())
        navBarLayout.addWidget(addEmployeeButton, alignment=Qt.AlignLeft)

        titleLabel = QLabel("CHECK-OUT REGISTER")
        titleLabel.setStyleSheet("font-size: 40px; font-weight: bold; color: #FD850C; background-color: transparent; padding: 5px;")
        navBarLayout.addWidget(titleLabel, alignment=Qt.AlignCenter)

        collegeLogo = QPixmap("resources/collegeLogo.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        collegeLogoLabel = QLabel()
        collegeLogoLabel.setPixmap(collegeLogo)
        navBarLayout.addWidget(collegeLogoLabel, alignment=Qt.AlignRight)

        navBarWidget = QWidget()
        navBarWidget.setLayout(navBarLayout)
        navBarWidget.setStyleSheet("background-color: white;")  # nav bar opaque to see text clearly
        main_layout.addWidget(navBarWidget)

        # Now create scroll area widget for employees, make its background transparent:
        employeeDatas = self.connectToEmployeeDb()
        checkDatas = self.connectToCheckDb()
        employeeVerticalLayout = QVBoxLayout()
        employeeRowLayout = QHBoxLayout()

        if employeeDatas:
            for idx, data in enumerate(employeeDatas, start=1):
                name = data[1].split()
                if len(name) == 3:
                    newName = [name[0] + " " + name[1], name[2]]
                else:
                    newName = name

                nameLabel = ClickableLabel(f"{newName[0]}\n{newName[1]}", func=self.label_clicked, cleanName=" ".join(newName))
                nameLabel.setStyleSheet("""
                    QLabel {
                        background-color: white;
                        border: 12px solid #FD850C;
                        border-radius: 10px;
                        font-size: 20px;
                        color: black;
                        padding: 5px;
                        border-style: outset;
                    }
                """)
                nameLabel.setAlignment(Qt.AlignCenter)
                nameLabel.setFixedSize(200, 150)

                employeeRowLayout.addWidget(nameLabel)
                employeeRowLayout.addSpacing(20)

                if idx % 3 == 0:
                    employeeVerticalLayout.addLayout(employeeRowLayout)
                    employeeVerticalLayout.addSpacing(20)
                    employeeRowLayout = QHBoxLayout()
        else:
            nameLabel = ClickableLabel("No Employees Found")
            nameLabel.setAlignment(Qt.AlignCenter)
            nameLabel.setStyleSheet("font-size: 24px; font-weight: bold; color: red;")
            nameLabel.setFixedSize(430, 380)
            employeeRowLayout.addWidget(nameLabel)

        if employeeRowLayout.count() > 0:
            employeeVerticalLayout.addLayout(employeeRowLayout)
            employeeVerticalLayout.addSpacing(20)

        scrollContent = QWidget()
        scrollContent.setLayout(employeeVerticalLayout)
        scrollContent.setStyleSheet("background-color: transparent;")

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical { width: 10px; background: transparent; }
        """)
        scrollArea.setWidget(scrollContent)

        main_layout.addWidget(scrollArea)

        



    def label_clicked(self, event ,name:str):

        print(name)
        #Remove the newline character if it exists
        name = " ".join(name.split())
        


        # Create a new InfoWindow instance and pass the name

        self.nextWindow= InfoWindow(name)
        self.nextWindow.show()  
     

    def addEmployee(self):
        # Create an instance of AddEmployeeWindow and show it
        self.addEmployeeWindow = AddEmployeeWindow(self)
        self.addEmployeeWindow.show()   
    



    #Connect to the Database and Create the Table if it does not exist

    def connectToEmployeeDb(self):

        #Import the JSON File
        filepath=r"resources/dbinfo.json"
        with open(filepath, 'r') as file:
            db_info = json.load(file)
        
        print(db_info)
        try:
            #Connect to db
            dbConnection = MySQLdb.connect(
                host=db_info["host"],
                user=db_info["username"],
                passwd=db_info["password"],
                database=db_info["database"]
            )
            print("Database connection successful")
        except MySQLdb.Error as err:
            print(f"Error: {err}")
            return
        cursor=dbConnection.cursor()

        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS employee_table(
                SN INTEGER PRIMARY KEY AUTO_INCREMENT,      
                Name TEXT NOT NULL,
                Password TEXT NOT NULL
 
            )''')
        except MySQLdb.Error as e:
            print(f"Error: Unable to create the table. Please check your SQL syntax.{e}")

        cursor.execute("SELECT * FROM employee_table")
        rows = cursor.fetchall()
        return rows
    

    def connectToCheckDb(self):

        #Import the JSON File
        filepath=r"resources/dbinfo.json"
        with open(filepath, 'r') as file:
            db_info = json.load(file)
        
        print(db_info)
        try:
            #Connect to db
            dbConnection = MySQLdb.connect(
                host=db_info["host"],
                user=db_info["username"],
                passwd=db_info["password"],
                database=db_info["database"]
            )
            print("Database connection successful")
        except MySQLdb.Error as err:
            print(f"Error: {err}")
            return
        cursor=dbConnection.cursor()

        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS checkInOut(
                SN INTEGER NOT NULL, 
                Name TEXT NOT NULL,
                CheckOut_Status BOOLEAN NOT NULL DEFAULT FALSE,
                CheckOut_Message TEXT DEFAULT NULL,
                CheckIn_Time DATETIME DEFAULT NULL,
                CheckOut_Time DATETIME DEFAULT NULL
 
            )''')
        except MySQLdb.Error as e:
            print(f"Error: Unable to create the table. Please check your SQL syntax.{e}")

        cursor.execute("SELECT * FROM checkInOut")
        rows = cursor.fetchall()
        dbConnection.close()
        return rows

        
        
        




        
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close() # Optional: let Escape key close the app
        else:
            super().keyPressEvent(event)





#-----------------------------View Window Part----------------------------------------#




class InfoWindow(QWidget):
    def __init__(self, name):
        super().__init__()
        self.setGeometry(300, 100, 500, 400)
        self.name=name
        self.setWindowIcon(QIcon("resources/icon.ico"))  # Set the window icon
        self.setWindowTitle("Status")
        
        self.init_ui()

    def init_ui(self):
        # Create the main vertical layout for the InfoWindow
        layout = QVBoxLayout()


        # Prompt the user to enter their password
        promptLabel = QLabel("Please enter your PIN:")
        promptLabel.setStyleSheet("font-size: 18px; color: black;")
        promptLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(promptLabel)

        # Password input field 
        # Password input field with show/hide icon
        passwordLayout = QHBoxLayout()
        validator = QIntValidator(0, 9999)
        promptEdit = QLineEdit()
        promptEdit.setValidator(validator)  # Set the validator to allow only digits
        promptEdit.setEchoMode(QLineEdit.Password)
        promptEdit.setPlaceholderText("Enter your PIN")
        promptEdit.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                padding: 10px;
                border: 2px solid #FD850C;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #FF9A3D;
            }
        """)    
        passwordLayout.addWidget(promptEdit)

        showPassButton = QPushButton()
        showPassButton.setCheckable(True)
        showPassButton.setFixedSize(24, 24)
        showPassButton.setIcon(QIcon("resources/show.png"))  # Use your show/hide icon paths
        showPassButton.setStyleSheet("border: none;")
        def toggle_password():
            if showPassButton.isChecked():
                promptEdit.setEchoMode(QLineEdit.Normal)
                showPassButton.setIcon(QIcon("resources/hide.png"))
            else:
                promptEdit.setEchoMode(QLineEdit.Password)
                showPassButton.setIcon(QIcon("resources/show.png"))
        showPassButton.clicked.connect(toggle_password)
        passwordLayout.addWidget(showPassButton)
        layout.addLayout(passwordLayout)

        # Submit button to trigger database lookup
        submitButton = QPushButton("Submit")
        submitButton.clicked.connect(lambda:self.assignPassword(promptEdit.text()))
        submitButton.setStyleSheet("""
            QPushButton {
                background-color: #FD850C;
                color: white;
                font-size: 18px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover { 
                background-color: #FF9A3D;
            }           
            QPushButton:pressed {
                background-color: #FF7A00;
            }
        """)
        # Add the submit button to the layout
        layout.addWidget(submitButton)  
        self.setLayout(layout)


     #----------#   


    def assignPassword(self, password):
        self.password = password
        # Call the database lookup function with the name and password
        result = self.databaseLookup(self.name, self.password)
        if result:
            #Clear the old layout
            self.clearLayout(self.layout())

            #Define new layout
            layout = QVBoxLayout()

            # Display the employee's name at the top
            nameLabel = QLabel(f"{result[1]}")
            nameLabel.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
            nameLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(nameLabel)

           

            # Spacer to push the message to the middle




            # Two buttons side by side at the bottom: Check In and Check Out
            buttonLayout = QVBoxLayout()
            checkInBtn = QPushButton("Check In")
            checkOutBtn = QPushButton("Check Out")
            

            changePinBtn = QPushButton("Change PIN")
            changePinBtn.setStyleSheet("""
                QPushButton {
                    background-color: #CCCCCC;
                    color: #333;
                    font-size: 14px;
                    padding: 6px 12px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #BBBBBB;
                }
            """)
            changePinBtn.setFixedWidth(160)
            changePinBtn.setFixedHeight(32)
            # You can connect this to a change PIN dialog if needed
            # changePinBtn.clicked.connect(self.changePinDialog)
            
            changePinBtn.clicked.connect(lambda: self.changePinDialog(result[0], result[1]))

            btnStyle = """
                QPushButton {
                    background-color: #FD850C;
                    color: white;
                    font-size: 18px;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover { 
                    background-color: #FF9A3D;
                }           
                QPushButton:pressed {
                    background-color: #FF7A00;
                }
            """
            checkInBtn.setStyleSheet(btnStyle)
            checkOutBtn.setStyleSheet(btnStyle)
            try:
                checkInBtn.clicked.disconnect()
                checkOutBtn.clicked.disconnect()
            except TypeError:
                pass  # No connections yet, ignore

            # Now connect only one handler based on status
            filepath=r"resources/dbinfo.json"
            with open(filepath, 'r') as file:
                db_info = json.load(file)
            try:
            #Connect to db
                dbConnection = MySQLdb.connect(
                    host=db_info["host"],
                    user=db_info["username"],
                    passwd=db_info["password"],
                    database=db_info["database"]
                )
                print("Database connection successful")
            except MySQLdb.Error as err:
                print(f"Error: {err}")
                return
            cursor=dbConnection.cursor()

            cursor.execute("SELECT * FROM checkInOut WHERE SN = %s", (result[0],))

            checkResult=cursor.fetchall()
            print(checkResult)
            

            status=0
            if result:  # If there are any records for this employee
                for i in checkResult:
                    if i[2] == 1:
                        status = 1
            else:
                return
    


            if status:  # Already checked out
                # Clicking Check Out shows info, does NOT call performAction
                checkOutBtn.clicked.connect(lambda: QMessageBox.information(self, "Already Checked Out", "You are already checked out."))

                # Check In button performs action normally
                checkInBtn.clicked.connect(lambda: self.performAction(result[0], True))

            else:  # Already checked in
                # Clicking Check In shows info, does NOT call performAction
                checkInBtn.clicked.connect(lambda: QMessageBox.information(self, "Already Checked In", "You are already checked in."))

                # Check Out button performs action normally
                checkOutBtn.clicked.connect(lambda: self.performAction(result[0], False))

            buttonLayout.addWidget(checkInBtn)
            buttonLayout.addWidget(checkOutBtn)
            layout.addLayout(buttonLayout)
            layout.addWidget(changePinBtn, alignment=Qt.AlignHCenter | Qt.AlignBottom)

            self.setLayout(layout)
    
    def changePinDialog(self, SN, name):
        # Clear the current layout and set up a new one for changing PIN
        self.clearLayout(self.layout())
        layout = QVBoxLayout()

        # Current Name
        nameLabel = QLabel(f"Current Name: {name}")
        nameLabel.setStyleSheet("font-size: 18px; color: black;")
        nameLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(nameLabel)

        # Old PIN Input
        oldPinLayout = QHBoxLayout()
        oldPinInput = QLineEdit()
        oldPinInput.setPlaceholderText("Enter current PIN")
        oldPinInput.setEchoMode(QLineEdit.Password)
        oldPinInput.setValidator(QIntValidator(0, 9999))
        oldPinInput.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                padding: 10px;
                border: 2px solid #FD850C;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #FF9A3D;
            }
        """)
        oldPinToggle = QPushButton()
        oldPinToggle.setCheckable(True)
        oldPinToggle.setFixedSize(24, 24)
        oldPinToggle.setIcon(QIcon("resources/show.png"))
        oldPinToggle.setStyleSheet("border: none;")
        def toggle_old_pin():
            if oldPinToggle.isChecked():
                oldPinInput.setEchoMode(QLineEdit.Normal)
                oldPinToggle.setIcon(QIcon("resources/hide.png"))
            else:
                oldPinInput.setEchoMode(QLineEdit.Password)
                oldPinToggle.setIcon(QIcon("resources/show.png"))
        oldPinToggle.clicked.connect(toggle_old_pin)
        oldPinLayout.addWidget(oldPinInput)
        oldPinLayout.addWidget(oldPinToggle)
        layout.addLayout(oldPinLayout)

        # New PIN Input
        newPinLayout = QHBoxLayout()
        newPinInput = QLineEdit()
        newPinInput.setPlaceholderText("Enter new PIN")
        newPinInput.setEchoMode(QLineEdit.Password)
        newPinInput.setValidator(QIntValidator(0, 9999))
        newPinInput.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                padding: 10px;
                border: 2px solid #FD850C;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #FF9A3D;
            }
        """)
        newPinToggle = QPushButton()
        newPinToggle.setCheckable(True)
        newPinToggle.setFixedSize(24, 24)
        newPinToggle.setIcon(QIcon("resources/show.png"))
        newPinToggle.setStyleSheet("border: none;")
        def toggle_new_pin():
            if newPinToggle.isChecked():
                newPinInput.setEchoMode(QLineEdit.Normal)
                newPinToggle.setIcon(QIcon("resources/hide.png"))
            else:
                newPinInput.setEchoMode(QLineEdit.Password)
                newPinToggle.setIcon(QIcon("resources/show.png"))
        newPinToggle.clicked.connect(toggle_new_pin)
        newPinLayout.addWidget(newPinInput)
        newPinLayout.addWidget(newPinToggle)
        layout.addLayout(newPinLayout)

        # Confirm New PIN Input
        confirmPinLayout = QHBoxLayout()
        confirmPinInput = QLineEdit()
        confirmPinInput.setPlaceholderText("Confirm new PIN")
        confirmPinInput.setEchoMode(QLineEdit.Password)
        confirmPinInput.setValidator(QIntValidator(0, 9999))
        confirmPinInput.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                padding: 10px;
                border: 2px solid #FD850C;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #FF9A3D;
            }
        """)
        confirmPinToggle = QPushButton()
        confirmPinToggle.setCheckable(True)
        confirmPinToggle.setFixedSize(24, 24)
        confirmPinToggle.setIcon(QIcon("resources/show.png"))
        confirmPinToggle.setStyleSheet("border: none;")
        def toggle_confirm_pin():
            if confirmPinToggle.isChecked():
                confirmPinInput.setEchoMode(QLineEdit.Normal)
                confirmPinToggle.setIcon(QIcon("resources/hide.png"))
            else:
                confirmPinInput.setEchoMode(QLineEdit.Password)
                confirmPinToggle.setIcon(QIcon("resources/show.png"))
        confirmPinToggle.clicked.connect(toggle_confirm_pin)
        confirmPinLayout.addWidget(confirmPinInput)
        confirmPinLayout.addWidget(confirmPinToggle)
        layout.addLayout(confirmPinLayout)

        # Submit Button
        submitBtn = QPushButton("Submit")
        submitBtn.setStyleSheet("""
            QPushButton {
                background-color: #FD850C;
                color: white;
                font-size: 18px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover { 
                background-color: #FF9A3D;
            }           
            QPushButton:pressed {
                background-color: #FF7A00;
            }
        """)

        def handle_submit():
            old_pin = oldPinInput.text().strip()
            new_pin = newPinInput.text().strip()
            confirm_pin = confirmPinInput.text().strip()
            # Validate old pin
            if not old_pin or len(old_pin) != 4 or not old_pin.isdigit():
                QMessageBox.warning(self, "PIN Error", "Please enter your current 4-digit PIN.")
                return
            # Validate new pin
            if not new_pin or len(new_pin) != 4 or not new_pin.isdigit():
                QMessageBox.warning(self, "PIN Error", "New PIN must be exactly 4 digits.")
                return
            if new_pin != confirm_pin:
                QMessageBox.warning(self, "PIN Error", "New PIN and confirmation do not match.")
                return
            if new_pin == old_pin:
                QMessageBox.warning(self, "PIN Error", "New PIN must be different from the old PIN.")
                return
            # Check old pin in DB
            filepath = r"resources/dbinfo.json"
            with open(filepath, 'r') as file:
                db_info = json.load(file)
            try:
                dbConnection = MySQLdb.connect(
                    host=db_info["host"],
                    user=db_info["username"],
                    passwd=db_info["password"],
                    database=db_info["database"]
                )
            except MySQLdb.Error as err:
                QMessageBox.critical(self, "Database Error", f"Error: {err}")
                return
            cursor = dbConnection.cursor()
            cursor.execute("SELECT Password FROM employee_table WHERE SN = %s", (SN,))
            db_pin = cursor.fetchone()
            if not db_pin or db_pin[0] != old_pin:
                QMessageBox.critical(self, "PIN Error", "Current PIN is incorrect.")
                dbConnection.close()
                return
            # Update pin
            try:
                cursor.execute("UPDATE employee_table SET Password = %s WHERE SN = %s", (new_pin, SN))
                dbConnection.commit()
                dbConnection.close()
                self.clearLayout(self.layout())
                layout2 = QVBoxLayout()
                successLabel = QLabel("PIN changed successfully!")
                successLabel.setStyleSheet("font-size: 24px; color: green; font-weight: bold;")
                successLabel.setAlignment(Qt.AlignCenter)
                layout2.addWidget(successLabel)
                self.setLayout(layout2)
            except Exception as e:
                dbConnection.close()
                QMessageBox.critical(self, "Database Error", f"Failed to update PIN: {e}")
        submitBtn.clicked.connect(handle_submit)
        layout.addWidget(submitBtn)

        self.setLayout(layout)

    def performAction(self, employee_id, current_status):
        # Connect to the database and toggle the check-out status
        filepath = r"resources/dbinfo.json"
        with open(filepath, 'r') as file:
            db_info = json.load(file)
        
        try:
            dbConnection = MySQLdb.connect(
                host=db_info["host"],
                user=db_info["username"],
                passwd=db_info["password"],
                database=db_info["database"]
            )
            
        except MySQLdb.Error as err:
            print(f"Error: {err}")
            return
        
        cursor = dbConnection.cursor()
        # If checking out (current_status is False), prompt for a message

        if not current_status:
            # Clear the current layout and set up a new one for message input
            self.clearLayout(self.layout())
            layout = QVBoxLayout()

            # Create a label and text edit for the check-out message
            nameLabel = QLabel("Please provide a reason for checking out:")
            nameLabel.setStyleSheet("font-size: 20px; color: black; font-weight: bold;")    
            nameLabel.setAlignment(Qt.AlignCenter)


            # Create a QTextEdit for the message input

            messageEdit = QTextEdit()
            messageEdit.setPlaceholderText("Enter your message here")
            messageEdit.setStyleSheet("""
                QTextEdit {
                    font-size: 18px;
                    padding: 10px;
                    border: 2px solid #FD850C;
                    border-radius: 5px;
                } 
                QTextEdit:focus {
                    border-color: #FF9A3D;
                }
            """)


            layout.addWidget(nameLabel)
            layout.addWidget(messageEdit)   
            # Add a submit button to store the message
            submitBtn = QPushButton("Submit")
            submitBtn.setStyleSheet("""
                QPushButton {
                    background-color: #FD850C;
                    color: white;
                    font-size: 18px;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover { 
                    background-color: #FF9A3D;
                }           
                QPushButton:pressed {
                    background-color: #FF7A00;
                }
            """)
            # Connect the submit button to the function that handles message submission
            submitBtn.clicked.connect(lambda: submit_message(employee_id, messageEdit, cursor, dbConnection, layout))
            layout.addWidget(submitBtn) 
            self.setLayout(layout)

        
 
            def submit_message(employee_id, messageEdit, cursor, dbConnection, layout):

                employees=cursor.execute("SELECT * FROM employee_table WHERE SN = %s", (employee_id,))
                name=cursor.fetchone()[1]
                if not employees:
                    QMessageBox.warning(self, "Check Out Failed", "Employee not found.")
                    return  

                # Get the message from the QTextEdit and validate it
                message = messageEdit.toPlainText().strip()

                # If the message is empty, show a warning and return
                if not message:
                    QMessageBox.warning(self, "Check Out Failed", "Check out message is required.")
                    
                    return
                try:
                    # Update the database with the check-out status and message
                    checkOutTime = self.getCurrentDateTime()
                    update_query = "INSERT INTO checkInOut (SN,Name,CheckOut_Status, CheckOut_Message, CheckOut_Time) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(update_query, (employee_id, name, True, message, checkOutTime))
                    dbConnection.commit()
                    
                    
                    self.clearLayout(self.layout())
                    layout = QVBoxLayout()
                    #format checkintime to date and time 2 diff variables
                    time = checkOutTime.split(" ")[1]  # Get only the time part
                    date=    checkOutTime.split(" ")[0]  # Get only the date part
                    successLabel = QLabel(f"Check Out Successful!\n\nChecked-Out Date :  {date}\nChecked-Out Time :  {time}")
                    successLabel.setStyleSheet("font-size: 30px; color: green; font-weight: bold;")
                    successLabel.setAlignment(Qt.AlignCenter)
                    layout.addWidget(successLabel)
                    self.setLayout(layout)
                    
                except Exception as e:
                    QMessageBox.critical(self, "Check Out Failed", f"An error occurred: {e}")
                    submitBtn.clicked.connect(submit_message)
                    layout.addWidget(submitBtn)
                    
                
                    
                    return
            
        else: #If current status is False, it means the employee is checking in
            try:
                # If checking in, update the status without a message
                checkInTime = self.getCurrentDateTime()
                update_query = "UPDATE checkInOut SET CheckIn_Time = %s, CheckOut_Status = %s WHERE SN = %s AND CheckOut_Status = %s"
                cursor.execute(update_query, (checkInTime, False, employee_id, True))
                if cursor.rowcount == 0: 
                    QMessageBox.warning(self, "Check In Failed", "Employee not found or already checked in.")
                    return
                
                dbConnection.commit()

                # Clear the current layout and show success message in the window
                self.clearLayout(self.layout())
                layout = QVBoxLayout()
                #format checkintime to date and time 2 diff variables
                time = checkInTime.split(" ")[1]  # Get only the time part
                date=    checkInTime.split(" ")[0]  # Get only the date part
                successLabel = QLabel(f"Check In Successful!\n\nChecked-In Date :  {date}\nChecked-In Time :  {time}")
                successLabel.setStyleSheet("font-size: 30px; color: green; font-weight: bold;")
                successLabel.setAlignment(Qt.AlignCenter)
                layout.addWidget(successLabel)
                self.setLayout(layout)
            except Exception as e:
                QMessageBox.critical(self, "Check In Failed", f"An error occurred: {e}")
            finally:
                dbConnection.close()
    
    def clearLayout(self, layout):
        # Remove all widgets and layouts from the given layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            child_layout = item.layout()
            if child_layout is not None:
                self.clearLayout(child_layout)
        # If this layout is the main layout of the window, unset it to avoid "already has layout" error
        if self.layout() is layout:
            QWidget().setLayout(self.layout())
    
    def getCurrentDateTime(self):
        
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")



    def databaseLookup(self,name,password):
        #Import the JSON File
        filepath=r"resources/dbinfo.json"
        with open(filepath, 'r') as file:
            db_info = json.load(file)
        
        try:
            #Connect to db
            dbConnection = MySQLdb.connect(
                host=db_info["host"],
                user=db_info["username"],
                passwd=db_info["password"],
                database=db_info["database"]
            )
            print("Database connection successful")
        except MySQLdb.Error as err:
            print(f"Error: {err}")
            return
        
        cursor = dbConnection.cursor()
        # First, check if the name exists
        name_query = "SELECT * FROM employee_table WHERE Name = %s"
        cursor.execute(name_query, (name,))
        name_result = cursor.fetchone()
        if not name_result:
            # Show GUI feedback for name not found
            self.clearLayout(self.layout())
            layout = QVBoxLayout()
            nameLabel = QLabel("Name not found.")
            nameLabel.setStyleSheet("font-size: 20px; color: red; font-weight: bold;")
            nameLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(nameLabel)
            self.setLayout(layout)
            return None

        # Then, check if the password matches for that name
        pass_query = "SELECT * FROM employee_table WHERE Name = %s AND Password = %s"
        cursor.execute(pass_query, (name, password))
        result = cursor.fetchone()
        
        dbConnection.close()
        if result:
            

            return result
        else:
            # Show GUI feedback for incorrect password
            self.clearLayout(self.layout())
            layout = QVBoxLayout()
            passLabel = QLabel("Incorrect PIN.")
            passLabel.setStyleSheet("font-size: 20px; color: red; font-weight: bold;")
            passLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(passLabel)
            self.setLayout(layout)
            return None


    
        

#---------------------------------------------------------------------#

if __name__=="__main__":
    app=QApplication([])
    window=MainAppWindow()
    window.show()
    sys.exit(app.exec_())
    