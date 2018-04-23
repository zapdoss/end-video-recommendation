import requests
import json

def tags(id):
    try:
        tags=json.loads((requests.get("https://www.googleapis.com/youtube/v3/videos?key=AIzaSyCjXSaAJchstnrxGPXd9yR73kp4dIjjNU8&fields=items(snippet(title,description,tags))&part=snippet&id="+id)).content)["items"][0]["snippet"]["tags"]

        vids=[]
        temp = ""
        for i in range(min(len(tags), 5)):
            temp += tags[i] + "+"

        string = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q="+temp+"&key=AIzaSyCsrw2p5BxOKuKjjCn9NNMhYRra8amsboQ&type=video&pageToken="
        searchRes=json.loads((requests.get(string)).content)["items"]

        for i in range(min(25,len(searchRes))):
            if searchRes[i]["id"]["videoId"] != id:
                vids.append(searchRes[i]["id"]["videoId"])

        return vids
    except:
        return []
