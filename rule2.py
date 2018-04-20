import psycopg2
import sys
 

courses={}
con = None
 
try:
    con = psycopg2.connect("host='localhost' dbname='testdb' user='pythonspot' password='password'")   
    cur = con.cursor()
    cur.execute("SELECT * FROM courses ORDER BY seq_no")
 
    while True:
        row = cur.fetchone()
 
        if row == None:
            break

        if row[0] not in courses.keys():
            courses[row[0]]=[]
        courses[row[0]].append(row[1])
 
except psycopg2.DatabaseError, e:
    if con:
        con.rollback()
 
    print 'Error %s' % e    
    sys.exit(1)
 
finally:   
    if con:
        con.close()


# courses["cs1"]=[1,2,3,4,5]
# courses["cs2"]=[6,3,8,9,10]
# courses["cs3"]=[23,54,3,5,44]
# courses["cs4"]=[22,3,2,44,55,66,77,88,99]
# courses["cs5"]=[33,44,2,4,6,7]

def getVideosR2(id):
    vids=[]
    for k in range(100):
        for i in courses.keys():
            for j in range(len(courses[i])-k-1):
                if(courses[i][j]==id):
                    if courses[i][j+k+1] not in vids:
                        vids.append(courses[i][j+k+1])

    return vids

#print getVideosR2(3)

