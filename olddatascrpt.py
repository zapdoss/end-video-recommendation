import psycopg2
import sys
import fromKenlist
import tags


usermap={}
con = None

try:
    con = psycopg2.connect("host='localhost' dbname='logs' user='postgres' password='qwerty123'")
    cur = con.cursor()
    cur.execute("SELECT * FROM user_video ORDER BY date,time")

    while True:
        row = cur.fetchone()

        if row == None:
            break

        if row[0] not in usermap.keys():
            usermap[row[0]]=[]
        usermap[row[0]].append(row[1])

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

videos={}
for k in usermap.keys():
    for i in range(len(usermap[k])):
        if usermap[k][i] not in videos.keys():
            videos[usermap[k][i]]=[0,0,0]
        mod=0
        #course rule
        similarVideos=fromKenlist.fromKenlist(usermap[k][i])
        if(i<len(usermap[k])-1):
            if(usermap[k][i+1] in similarVideos):
                videos[usermap[k][i]][0]=videos[usermap[k][i]][0]+1
                mod=1
        if(i<len(usermap[k])-2):
            if(usermap[k][i+2] in similarVideos):
                videos[usermap[k][i]][0]=videos[usermap[k][i]][0]+1
                mod=1
        #tags
        similarVideos=tags.tags(usermap[k][i])
        if(i<len(usermap[k])-1):
            if(usermap[k][i+1] in similarVideos):
                videos[usermap[k][i]][1]=videos[usermap[k][i]][1]+1
                mod=1
        if(i<len(usermap[k])-2):
            if(usermap[k][i+2] in similarVideos):
                videos[usermap[k][i]][1]=videos[usermap[k][i]][1]+1
                mod=1
        #similarusers
        if mod==0:
            videos[usermap[k][i]][2]=videos[usermap[k][i]][2]+1

print videos



#print getVideosR2(3)
