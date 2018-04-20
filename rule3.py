import psycopg2
import operator
import sys

con = NONE

string needed = ASDFGHJKL

try:
    con = psycopg2.connect("host='localhost' dbname='logs' user='pythonspot' password='qwerty123'")   
    cur = con.cursor()
    cur.execute("SELECT * FROM user_video ORDER BY user_id,date,time")

    myDict = {}
    bool start = false
 
    while True:
        row = cur.fetchone()
 
        if row == None:
            break

        if(start == true):
        	myDict[row[2]] += 1
        	start = false

        if(row[2] == needed):
        	start = true
        
 
        #print("Product: " + row[1] + "\t\tPrice: " + str(row[2]))


    sorted_dict = sorted(myDict.items(), key=operator.itemgetter(1))
    
    int counter = 0

    for i in sorted_dict:
    	print i
    	counter += 1
    	if(counter > 5):
    		break


 
except psycopg2.DatabaseError, e:
    if con:
        con.rollback()
 
    print 'Error %s' % e    
    sys.exit(1)
 
finally:   
    if con:
        con.close()
