import datetime
import time
from mysql import connector as sql

HOSTNAME = "204.10.192.213"
USERNAME = "u53921_iZQb7sDtfi"
PASSWORD = "cF3xy2jk2bUWphB5xDwQt84w"
DATABASE = "s53921_analrp"

def printex(string: str):
    # TimeStamp
    time_ = time.localtime()
    timestamp = f"[{time_.tm_hour}:{time_.tm_min}:{time_.tm_sec}]       "
    print(f"{timestamp}{string}")
    return True

databaseinfo = {'user': USERNAME, 'password': PASSWORD, 'host': HOSTNAME, 'database': DATABASE, 'raise_on_warnings': True}

def ConnectToDatabase():
    try:
        knowledgebase = sql.connect(**databaseinfo)
        cursor = knowledgebase.cursor()
        printex("MySQL Connection Created Successfully")
        knowledgebase.disconnect()
    except Exception as e:
        printex(f"Could not connect to MySQL DataBase. Exitting...")
        exit()

def CheckQuery(query):
    try:
        knowledgebase = sql.connect(**databaseinfo)
        cursor = knowledgebase.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
    except Exception as e:
        printex(f"NewLife Manager can't execute a query becasue: {e}")
        knowledgebase.disconnect()
        return False
    else:
        if result:
            return True
        else:
            return False
    
    
def GetResult(query):
    try:
        knowledgebase = sql.connect(**databaseinfo)
        cursor = knowledgebase.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
    except Exception as e:
        printex(f"NewLife Manager can't execute a query becasue: {e}")
        knowledgebase.disconnect()
        return False
    else:
        knowledgebase.disconnect()
        if result:
            return result
        else:
            return False
    
    
def sql_query(query):
    try:
        knowledgebase = sql.connect(**databaseinfo)
        cursor = knowledgebase.cursor()
        cursor.execute(query)
        knowledgebase.commit()
        knowledgebase.disconnect()
        return True
    except Exception as e:
        printex(f"A query isn't executed fully beacuse '{e}'")
        knowledgebase.disconnect()
        return 
    
def GetGender(id:int):
    if id == 1:
        return "Male"
    else:
        return "Female"

def GetFactionName(id:int):
    if id == 0:
        return "Civilian"
    else:
        result = GetResult(f"SELECT `factionName` FROM `factions` WHERE `factionID` = '{id}'")
        for x in result:
            name = x[0]
        return name
    
def ReturnAge(date:str):
    birthdate = datetime.datetime.strptime(date, "%d/%m/%Y")
    current_date = datetime.datetime.now()
    age = current_date.year - birthdate.year - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))
    return age

def ReturnHour(seconds:int):
    formattime = datetime.timedelta(seconds=seconds)
    hours, extra = divmod(formattime.seconds, 3600)
    return extra

def ReturnDays(seconds:int):
    formattime = datetime.timedelta(seconds=seconds)
    days = formattime.days
    return days