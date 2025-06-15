            cursor.execute('''CREATE TABLE IF NOT EXISTS checkInOut(
                SN INTEGER NOT NULL, 
                Name TEXT NOT NULL,
                CheckOut_Status BOOLEAN NOT NULL DEFAULT FALSE,
                CheckOut_Message TEXT DEFAULT NULL,
                CheckIn_Time DATETIME DEFAULT NULL,
                CheckOut_Time DATETIME DEFAULT NULL
 
            )''')