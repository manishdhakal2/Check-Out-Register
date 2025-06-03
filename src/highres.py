from PyQt5.QtWidgets import QWidget,QLabel, QVBoxLayout,QLayout, QHBoxLayout, QPushButton, QLineEdit,QApplication, QScrollArea, QSpacerItem, QSizePolicy, QTextEdit
from PyQt5.QtGui import QIcon, QImage, QKeyEvent, QKeyEvent, QResizeEvent, QPixmap, QPainterPath, QRegion
from PyQt5.QtCore import Qt, QSize, QRect, QPoint
import sys
from PyQt5.QtSvg import QSvgWidget
import MySQLdb
import json
from PyQt5.QtWidgets import QInputDialog
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
        self.adminPassword = "checkoutAdminSWSC"
        self.win=win
        self.init_ui1()
    

    def init_ui1(self): 
        # Layout for admin password verification
        layout = QVBoxLayout()

        admin_label = QLabel("Enter Admin Password :")
        admin_label.setStyleSheet("font-size: 18px; color: black;")
        admin_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(admin_label)

        # Password input field with show/hide icon
        pass_layout = QHBoxLayout()
        self.admin_pass_input = QLineEdit()
        self.admin_pass_input.setPlaceholderText("Admin Password")
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
            if self.admin_pass_input.text() == self.adminPassword:
                self.init_ui2()
            else:
                QMessageBox.critical(self, "Access Denied", "Incorrect admin password.")
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
        employeeName.setAlignment(Qt.AlignLeft)
        layout.addWidget(employeeName)

        layout.addWidget(self.name_input)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
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
        passwordLabel = QLabel("Password:")
        passwordLabel.setStyleSheet("font-size: 18px; color: black;")
        passwordLabel.setAlignment(Qt.AlignLeft)
        layout.addWidget(passwordLabel)
        layout.addWidget(self.password_input)

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

        password = self.password_input.text().strip()
        # Validate password
        if not self.passwordValidator(password):
            self.close()
            self.init_ui()

        # Check if name and password are provided
        if not name or not password:
            QMessageBox.warning(self, "Input Error", "Both name and password are required.")
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
            insert_query = "INSERT INTO Employees (Name, Password) VALUES (%s, %s)"
            cursor.execute(insert_query, (name, password))
            dbConnection.commit()
            QMessageBox.information(self, "Success", "Employee added successfully.")

            self.win.close()
            win=MainAppWindow()  # Refresh the main window to show the new employee
            win.show()  
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to add employee: {e}")

    #---------#
        
    def passwordValidator(self, password):
            # Check if the password meets the criteria
            if len(password) < 8:
                QMessageBox.warning(self, "Password Error", "Password must be at least 8 characters long.")
                return False
            if not any(char.isdigit() for char in password):
                QMessageBox.warning(self, "Password Error", "Password must contain at least one digit.")
                return False
            if not any(char.isalpha() for char in password):
                QMessageBox.warning(self, "Password Error", "Password must contain at least one letter.")
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
class MainAppWindow(QWidget):

    def __init__(self)->None:

        #Call the parent Constructor
        super(MainAppWindow,self).__init__()
        #Set the title
        self.setWindowTitle("Check-Out Register")
        self.setGeometry(0,0,1280,720)
        #Run in Fullscreen
        self.showFullScreen()
        self.init_ui()
    
    def init_ui(self)->None:

        #Use the Vertical Approach
        self.mainLayout=QVBoxLayout()

        #Define the Layout For Top Title
        navBarLayout=QHBoxLayout()

        #Define the layout for Rows of 3 Employees Each
        self.employeeRowLayout=QVBoxLayout()

        #Define the layout for columns containing 3 employees
        self.employeeColumnLayout=QHBoxLayout()


        #-------------------------------NavBar Section---------------------------------#

        #Add the Logo
        addEmployeeButton=QPushButton()
        img=QPixmap("resources/addProfile.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        addEmployeeButton.setIcon(QIcon(img))
        addEmployeeButton.setIconSize(QSize(40, 40))
        addEmployeeButton.setStyleSheet("background-color: transparent; border: none;")
        addEmployeeButton.setFixedSize(50, 50)
        addEmployeeButton.setToolTip("Add Employee")
        addEmployeeButton.clicked.connect(lambda: self.addEmployee())
        navBarLayout.addWidget(addEmployeeButton,alignment=Qt.AlignLeft)


        #Add the Title
        titleLabel=QLabel( "Check-Out Register")
        titleLabel.setStyleSheet("font-size: 30px; font-weight: bold; color: black;")
        navBarLayout.addWidget(titleLabel,alignment=Qt.AlignCenter)

        #Add College Logo
        collegeLogo=QPixmap("resources/collegeLogo.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        collegeLogoLabel=QLabel(self)
        collegeLogoLabel.setPixmap(collegeLogo)
        navBarLayout.addWidget(collegeLogoLabel,alignment=Qt.AlignRight)

        #--------------------------------End of NavBar Section---------------------------------#

        #-------------------------------Employee Section---------------------------------#

        
        datas=self.connectToDb()
        print("Here")

        labelStyleIn='''
        QLabel {
                            font-size:20px;
                            background-color:white;
                            border: 10px solid #FD850C;
                            color:green;
                            
        }
        QLabel:hover {
        background-color:grey;
        }
        '''
        labelStyleOut='''
        QLabel {
                            font-size:20px;
                            background-color:white;
                            border: 10px solid #FD850C;
                            color:red;
                            
        }
        QLabel:hover {
        background-color:grey;
        }
        '''

        #Layout for displaying employee names 3 in a r
        employeeRowLayout=QHBoxLayout()
        employeeVerticalLayout=QVBoxLayout()
        if datas is not None:

            for idx,data in enumerate(datas, start=1):
            

                name= data[1]
                #Check if the name is a single word or two words
                
                name=name.split()
                if(len(name)==3):
                    newName = [name[0] + " " + name[1], name[2]]
                else:
                    newName=name

                nameLabel= ClickableLabel(f"{newName[0]}\n{newName[1]}",func=self.label_clicked,cleanName=" ".join(newName))
                nameLabel.setStyleSheet("""
                    QLabel {
                        border: 12px solid #FD850C;
                        border-radius: 10px;
                        background-color: white;
                        font-size: 20px;
                        color: black;
                        padding: 5px;
                        border-style: outset;
                    }
                """)

                nameLabel.setAlignment(Qt.AlignCenter)
                nameLabel.setFixedSize(200,150)

                employeeRowLayout.addWidget(nameLabel)
                spacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)
                employeeRowLayout.addSpacerItem(spacer)
                if idx % 3 == 0:
                    employeeVerticalLayout.addLayout(employeeRowLayout)

                    spacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
                    employeeVerticalLayout.addSpacerItem(spacer)
                    employeeRowLayout= QHBoxLayout()
        else:
           
            nameLabel= ClickableLabel("No Employees Found")
            nameLabel.setAlignment(Qt.AlignCenter)
            nameLabel.setStyleSheet("font-size: 24px; font-weight: bold; color: red;")
            nameLabel.setFixedSize(430,380)
            employeeRowLayout.addWidget(nameLabel)
        


        if employeeRowLayout.count() > 0:
            employeeVerticalLayout.addLayout(employeeRowLayout)
            # Add spacing after each row except the last one
            if employeeRowLayout is not employeeVerticalLayout.itemAt(employeeVerticalLayout.count() - 1):
                employeeVerticalLayout.addSpacing(20)
              

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setLayout(employeeVerticalLayout)
        self.scroll_area.setWidget(self.scroll_area_widget)

        self.mainLayout.addLayout(navBarLayout)
        self.mainLayout.addWidget(self.scroll_area)
        self.setLayout(self.mainLayout)
    
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

    def connectToDb(self):

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
            cursor.execute('''CREATE TABLE IF NOT EXISTS employees(
                SN INTEGER PRIMARY KEY AUTO_INCREMENT,  
                Name TEXT NOT NULL,
                Password TEXT NOT NULL,
                CheckOut_Status BOOLEAN NOT NULL DEFAULT FALSE,
                CheckOut_Message TEXT DEFAULT NULL
            )''')
        except MySQLdb.Error as e:
            print(f"Error: Unable to create the table. Please check your SQL syntax.{e}")

        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
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
        self.setWindowTitle("Authentication Required")
        
        self.init_ui()

    def init_ui(self):
        # Create the main vertical layout for the InfoWindow
        layout = QVBoxLayout()


        # Prompt the user to enter their password
        promptLabel = QLabel("Please enter your password:")
        promptLabel.setStyleSheet("font-size: 18px; color: black;")
        promptLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(promptLabel)

        # Password input field 
        # Password input field with show/hide icon
        passwordLayout = QHBoxLayout()
        promptEdit = QLineEdit()
        promptEdit.setEchoMode(QLineEdit.Password)
        promptEdit.setPlaceholderText("Enter your password")
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
            layout=QVBoxLayout()

            # Display the employee's name and status
            labelStyleIn='''
            QLabel {
                                font-size:20px;
                                background-color:white;
                                border: 10px solid #FD850C;
                                color:green;
                                
            }

            '''
            labelStyleOut='''
            QLabel {
                                font-size:20px;
                                background-color:white;
                                border: 10px solid #FD850C;
                                color:red;
                                
            }

            '''

            nameLabel = QLabel(f" {result[1]}")
            nameLabel.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")   
            nameLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(nameLabel)

            # Display the check-out status
            statusLabel = QLabel("Status: " + ("Checked Out" if result[3] else "Checked In"))
            statusLabel.setStyleSheet(labelStyleOut if result[3] else labelStyleIn)
            statusLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(statusLabel)

            # Display the check-out message if available
            if result[4]:
                messageLabel = QLabel(f"Latest Check-Out Message:\n ")
                messageLabel.setAlignment(Qt.AlignCenter)
                message = QTextEdit()
                message.setReadOnly(True)
                message.setText(str(result[4]))
                message.setStyleSheet("font-size: 18px; color: black;")
                message.setAlignment(Qt.AlignCenter)
                message.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
                layout.addWidget(messageLabel)
                layout.addWidget(message)
            else:
                messageLabel = QLabel("No message available.")
                messageLabel.setAlignment(Qt.AlignCenter)
                layout.addWidget(messageLabel)
            messageLabel.setStyleSheet("font-size: 18px; color: black;")
            # Add a button to return to Check in if checked out and vice versa
            actionButton = QPushButton("Check In" if result[3] else "Check Out")    
            actionButton.setStyleSheet("""
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
            actionButton.clicked.connect(lambda: self.performAction(result[0], result[3]))
            layout.addWidget(actionButton)  
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
            print("Database connection successful")
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
            nameLabel = QLabel("Enter Check-Out Message:")
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

                # Get the message from the QTextEdit and validate it
                message = messageEdit.toPlainText().strip()

                # If the message is empty, show a warning and return
                if not message:
                    QMessageBox.warning(self, "Check Out Failed", "Check out message is required.")
                    
                    return
                try:
                    # Update the database with the check-out status and message
                    update_query = "UPDATE Employees SET CheckOut_Status = %s, CheckOut_Message = %s WHERE SN = %s"
                    cursor.execute(update_query, (True, message, employee_id))
                    dbConnection.commit()
                    
                    
                    QMessageBox.information(self, "Check Out Successful", "Message stored successfully.")
                    self.clearLayout(self.layout())
                    self.close()
                    
                except Exception as e:
                    QMessageBox.critical(self, "Check Out Failed", f"An error occurred: {e}")
                    submitBtn.clicked.connect(submit_message)
                    layout.addWidget(submitBtn)
                    
                
                    
                    return
            
        else:
            try:
                # If checking in, update the status without a message
                update_query = "UPDATE Employees SET CheckOut_Status = %s WHERE SN = %s"
                # Execute the update query to set CheckOut_Status to False
                cursor.execute(update_query, (False, employee_id))
                dbConnection.commit()
                QMessageBox.information(self, "Check In Successful", "You have checked in successfully.")
                

                #@# Clear the current layout and close the window
                self.clearLayout(self.layout())
                self.close()
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
        name_query = "SELECT * FROM Employees WHERE Name = %s"
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
        pass_query = "SELECT * FROM Employees WHERE Name = %s AND Password = %s"
        cursor.execute(pass_query, (name, password))
        result = cursor.fetchone()
        dbConnection.close()
        if result:

            return result
        else:
            # Show GUI feedback for incorrect password
            self.clearLayout(self.layout())
            layout = QVBoxLayout()
            passLabel = QLabel("Incorrect password.")
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
    