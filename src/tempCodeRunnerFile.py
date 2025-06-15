import MySQLdb
import json
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

#Logic for checking SN
    cursor.execute("DELETE FROM CheckInOut")
    cursor.execute("DELETE FROM employee_table")
    dbConnection.commit()

except:
    pass