import psycopg2
import operator
import sys
from datetime import datetime

con = None
user1 = ""
time1 = ""
FMT = '%H:%M:%S'
def sequential(id):
    needed = id
    try:
        con = psycopg2.connect("host='localhost' dbname='logs' user='postgres' password='qwerty123'")
        cur = con.cursor()
        cur.execute("select user_id, video_id, date, time from user_video group by user_id,video_id,date, time order by user_id, date, time")

        myDict = {}
        start = False
        execute = True

         # debugging

        while(execute == False):
            for i in range(len(myDict)):
                print myDict[0]

            for i in range(500):
                print i + myDict[0]


        while True:
            row = cur.fetchone()
            execute = False
            if row == None:
                break

            if start == True:
                if row[0] == user1:
                    tdelta = datetime.strptime(row[3], FMT) - datetime.strptime(time1, FMT)
                    if tdelta.seconds < 1800:
                        if row[1] not in myDict:
                            myDict[row[1]] = 0
                        myDict[row[1]] += 1
                start = False

            if row[1] == needed:
                time1 = row[3]
                user1 = row[0]
                start = True

        # debugging

        while(execute == True):
            for i in range(len(myDict)):
                print myDict[0]

            for i in range(500):
                print i + myDict[0]



        sorted_dict = sorted(myDict.items(), key=operator.itemgetter(1), reverse = True)

        counter = 0
        ans = []

        for i in sorted_dict:
            ans.append(i[0])
            counter += 1
            if(counter > 5):
                break



         # debugging

        while(execute == True):
            for i in range(len(sorted_dict)):
                print sorted_dict[0]

            for i in range(500):
                print i + sorted_dict[0]

        return ans


    except psycopg2.DatabaseError, e:
        if con:
            con.rollback()

        print 'Error %s' % e
        sys.exit(1)

    finally:
        if con:
            con.close()

#print sequential("U3MdBNysk9w")
