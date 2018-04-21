import json
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import datetime, psycopg2, os, time
import io
import sys
import re
logs = open("logdumps_all" + "/" + "logs.csv",'w')

def copy_to_db(csv_path, cur, table_name):
	if (os.path.exists(csv_path)):
		#cur.execute('DELETE FROM ' + table_name)
		f = open(csv_path, 'r')
		cur.copy_from(f, table_name, sep=',')
		f.close()

def eval_dict(str):
	dict = {}
	parts = str.lstrip().rstrip().lstrip('{').rstrip('}').rstrip('.').split(',')
	for p in parts:
		kv = p.split(':')
		if len(kv) > 1:
			key = kv[0].rstrip().lstrip().rstrip('"').lstrip('"').rstrip("'").lstrip("'")
			if (len(key) > 0):
				dict[key] = kv[1].rstrip().lstrip().rstrip('"').lstrip('"').rstrip("'").lstrip("'")
	return dict


def eval_dict_logger(str):
    string = str.lstrip("log: 'Client log',").rstrip("']").replace(':', '').replace("'", '').replace("of", '')
    dit= {}
    dit['topic_name']= string.split("topic name")[-1].encode('utf-8').strip().replace(",",'')
    string= string.split("topic name")[0]
    dit['msg']=string.split("msg")[-1].split("content_id")[0].strip()
    dit['content_id'] = string.split("content_id")[-1].split("unit")[0].strip()
    dit['unit_id']= string.split("unit")[-1].split("Course")[0].strip()
    dit['course_id']= string.split("Course")[-1].split("video")[0].strip()
    dit['video_id']= string.split("video")[-1].split("kenlistID")[0].strip().lstrip('id').strip()
    dit['kenlist_id']= string.split("kenlistID")[-1].split("at")[0].strip()
    dit['at']= string.split("at")[-1].split("seconds")[0].strip()
    return dit


def parse_eachline(eachline):
	frags = eachline.split(']')
	#print eachline
	info = re.split(" +", frags[0])
	date = info[1]
	timestamp = info[2]

	data_dict = {}
	if len(frags[1]) > 3:
		data = frags[1].lstrip().lstrip('[').replace(':','').replace('=>',':')
		data_dict = eval_dict(data)

	user_id = frags[2].rstrip().lstrip().lstrip('[')
	email_id = frags[3].rstrip().lstrip().lstrip('[')

	msg = frags[4].lstrip().lstrip('[').replace('=>',':')
	msg_dict = eval_dict(msg)
	number_of_lists= len(frags)
	return date, timestamp, data_dict, user_id, email_id, msg_dict, msg, number_of_lists

l=1
while(l<=17):
    try:
        load = json.load(open("logdumps_all/logdump_"+str(l)+"00000.json"))
        l=l+1
        data={}
        for i in load:
            try:
                date, timestamp, data_dict, user_id, email_id, msg_dict, msg, number_of_lists = parse_eachline(i["message"])
                action = str(data_dict['action'])
                controller = str(data_dict['controller'])
                if(action == "log"):
                    msg_dict_log = eval_dict_logger(msg)
                    course_id = msg_dict_log["course_id"]
                    video_id = msg_dict_log["video_id"]
                    if int(user_id) and len(video_id) == 11:
                        if user_id not in data:
                            data[user_id]={}
                        data[user_id][video_id]=date+ ',' +timestamp
            except:
                continue

        for i in data.keys():
            for j in data[i].keys():
                print i, j, data[i][j]
                logs.write(i+','+j+','+ data[i][j]+'\n')

        conn = psycopg2.connect("host='localhost' port='5432' dbname='logs' user='postgres' password='qwerty123'")
        cur = conn.cursor()

        copy_to_db("logdumps_all" + "/" + "logs.csv", cur, 'user_video')

        conn.commit()
        conn.close()
    except:
        continue

    #print asd
