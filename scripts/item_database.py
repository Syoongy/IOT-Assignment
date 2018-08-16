import MySQLdb
#from gpiozero import MCP3008
from time import sleep


def dbConnect():
    try:
        global db
        global curs
        db = MySQLdb.connect("localhost", "assignmentuser",
                             "P@ssw0rd", "assignmentdb")
        curs = db.cursor()
        print("Successfully connected to database!")
    except:
        print("Error connecting to mySQL database")


def addItem(name, expiry):
    dbConnect()
    try:
        sql = "INSERT into items (name, expiry) VALUES (%s, %s)"
        data_sql = (name, expiry)
        curs.execute(sql, data_sql)
        db.commit()
    except MySQLdb.Error as e:
        print(e)
    curs.close()
    db.close()


def getItems():
    dbConnect()
    returnData = []
    try:
        query = "SELECT name, expiry FROM items"
        curs.execute(query)
        for(name, expiry) in curs:
            tmpReturnData = []
            tmpReturnData.append(name)
            tmpReturnData.append(expiry)
            returnData.append(tmpReturnData)
    except MySQLdb.Error as e:
        print(e)
    curs.close()
    db.close()
    return returnData
