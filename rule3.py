import psycopg2
import operator
import sys
from datetime import datetime

con = None
needed = "lq_xzBRIWm4"
user1 = ""
time1 = ""
FMT = '%H:%M:%S'

try:
    con = psycopg2.connect("host='localhost' dbname='logs' user='postgres' password='qwerty123'")
    cur = con.cursor()
    cur.execute("select user_id, video_id, date, time from user_video group by user_id,video_id,date, time order by user_id, date, time")

    myDict = {}
    start = False

    while True:
        row = cur.fetchone()

        if row == None:
            break

        if start == True:
            if row[0] == user1 && datetime.strptime(row[2], FMT) - datetime.strptime(time1, FMT) < 30
                if row[1] not in myDict:
                    myDict[row[1]] = 0
                    myDict[row[1]] += 1
            start = False

        if row[1] == needed:
            time1 = row[2]
            user1 = row[0]
            start = True

    sorted_dict = sorted(myDict.items(), key=operator.itemgetter(1), reverse = True)

    counter = 0

    for i in sorted_dict:
        print i
        counter += 1
        if(counter > 6):
            break



except psycopg2.DatabaseError, e:
    if con:
        con.rollback()

    print 'Error %s' % e
    sys.exit(1)

finally:
    if con:
        con.close()
