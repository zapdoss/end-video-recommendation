import psycopg2
import sys
import sequential
import fromKenlist
import tags


if __name__ == '__main__':
    video_id = raw_input()

    con = psycopg2.connect("host='localhost' dbname='logs' user='postgres' password='qwerty123'")
    cur = con.cursor()
    cur.execute("select * from rank_rule where video_id = " + video_id)

    row = cur.fetchone()
    videos = []
    rule_1 = []
    rule_2 = []
    rule_3 = []

    rule_1 = fromKenlist.fromKenlist(video_id)
    rule_2 = tags.tags(video_id)
    rule_3 = sequential.sequential(video_id)

    if(row == None):
        for i in range(min(len(rule_1), 4)):
            videos.append(i)
        for i in range(min(len(rule_2), 4)):
            videos.append(i)
        for i in range(min(len(rule_3), 4)):
            videos.append(i)
    else:
        if(row[0] >= row[1] and row[0] >= row[2]):
            for i in range(min(len(rule_1), 4)):
                videos.append(i)
            if(row[1] >= row[2]):
                for i in range(min(len(rule_2), 4)):
                    videos.append(i)
                for i in range(min(len(rule_3), 4)):
                    videos.append(i)
            else:
                for i in range(min(len(rule_3), 4)):
                    videos.append(i)
                for i in range(min(len(rule_2), 4)):
                    videos.append(i)
        elif(row[1] > row[0] and row[1] >= row[2]):
            for i in range(min(len(rule_2), 4)):
                videos.append(i)
            if(row[0] >= row[2]):
                for i in range(min(len(rule_1), 4)):
                    videos.append(i)
                for i in range(min(len(rule_3), 4)):
                    videos.append(i)
            else:
                for i in range(min(len(rule_3), 4)):
                    videos.append(i)
                for i in range(min(len(rule_1), 4)):
                    videos.append(i)
        elif(row[2] > row[0] and row[2] > row[1]):
            for i in range(min(len(rule_3), 4)):
                videos.append(i)
            if(row[0] >= row[1]):
                for i in range(min(len(rule_1), 4)):
                    videos.append(i)
                for i in range(min(len(rule_2), 4)):
                    videos.append(i)
            else:
                for i in range(min(len(rule_2), 4)):
                    videos.append(i)
                for i in range(min(len(rule_1), 4)):
                    videos.append(i)
    print rule_1, rule_2, rule_3
