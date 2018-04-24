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
        cur.execute("INSERT INTO rank_rule (video_id, rule_1, rule_2, rule_3) VALUES ({} ,{}, {},{})".format(video_id, 5, 3, 0))
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

    len_video = len(videos)
    for i in range(12-len_video):
        videos.append(rule_2[4+i])
        
    url = "https://www.googleapis.com/youtube/v3/videos?key=AIzaSyCjXSaAJchstnrxGPXd9yR73kp4dIjjNU8&fields=items(snippet(title,description,tags))&part=snippet&id="

    for i in videos:
        url += i+','


    data = json.loads((requests.get(url)).content)["items"]

    description = []

    for i in data:
        description.append(i["title"])

    for i in range(len(videos)):
        print videos[i] +" "+description[i]

    con.commit()
    selected = raw_input()
    mod = 0;

    if(selected in rule_1):
        cur.execute("update rank_rule set rule_1 = {} where video_id = {}".format(row[0] + 1, video_id))
        mod = 1

    if(selected in rule_2):
        cur.execute("update rank_rule set rule_2 = {} where video_id = {}".format(row[1] + 1, video_id))
        mod = 1

    elif(selected in rule_3 and mod == 0):
        cur.execute("update rank_rule set rule_3 = {} where video_id = {}".format(row[2] + 1, video_id))

    con.commit()
    cur.close()
    con.close()
