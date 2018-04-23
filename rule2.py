import psycopg2
import sys


courses={}
con = None

try:
    con = psycopg2.connect("host='localhost' dbname='courses' user='postgres' password='qwerty123'")
    cur = con.cursor()
    cur.execute("select c.play_list_id, l.youtube_id, rank from contents as c, lectures as l where l.id = c.content_id and c.contenttype = 'l' and c.play_list_id is not null and rank is not null order by play_list_id, c.rank;")

    while True:
        row = cur.fetchone()

        execute = False

        if row == None:
            break

        if row[0] not in courses.keys():
            courses[row[0]]=[]
        courses[row[0]].append(row[1])


        # debugging

        while(execute == True):
            for i in range(len(row)):
                print i #+ row[0]


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

# courses["cs6"]=[23,54,1,5,44]

# courses["cs7"]=[23,54,2,5,44]

# courses["cs8"]=[23,54,3,5,44]

# courses["cs9"]=[23,54,4,5,44]

# courses["cs10"]=[23,54,5,5,44]

# courses["cs11"]=[23,54,6,5,44]


def getVideosR2(id):
    execute = False
    vids=[]
    for k in range(100):
        for i in courses.keys():
            for j in range(len(courses[i])-k-1):
                if(courses[i][j]==id):
                    if courses[i][j+k+1] not in vids:
                        vids.append(courses[i][j+k+1])


    # debugging

    while(execute == True):
        for i in range(len(vids)):
            print i #+ vids[0]


    return vids

print getVideosR2("ARQ6PZh8vgE")

#print getVideosR2(3)
