import requests as req
import re, time

def get_csrf(string):
    return re.findall("name=\"csrf-token\" content=\"(.+)\" \/>", string)[0]

def go_in_meet(url, name):
    def main_task():
        firstGet = session.get(url)
        csrf_1 = get_csrf(firstGet.text)

        data = {
            "utf8": "✓", 
            "authenticity_token": csrf_1, 
            "/b/x2g-dqc-6fg[search]": "", 
            "/b/x2g-dqc-6fg[column]": "", 
            "/b/x2g-dqc-6fg[direction]": "", 
            "/b/x2g-dqc-6fg[join_name]": name
        }

        confer = session.post(url, data=data, allow_redirects=True)
        #csrf_2 = get_csrf(confer.text)
        #print(confer.history[-1].headers['Location'], confer.url)
        #print(confer.text)
        
        #isstart = re.findall("<div class=\"row\">\s+<div class=\"col-9\">\s+<h3>(.+)<\/h3>",
        #                     confer.text)[0] not in ["Встреча еще не началась",
        #                                            "Зустріч ще не почалася"]

        #print(isstart, confer.text)
        params = {
            "fullName": name, 
            #"join_via_html5": "true",
            "meetingID": "cdca89b8c354ed039027fe05f834ed4f4a2a888d", 
            "password": "qnHdvSOFyshj", 
            #"userID": "gl-guest-9a6e3294dde3f928d2d29139",
            "checksum": "ecf7149f0eb452c8180555c5f23699df5d822c36"
        }
        join = session.get("https://bbb.comsys.kpi.ua/bigbluebutton/api/join", params=params)
        print(join.url, join.history[-1].url)
        return True#isstart
    
    session = req.Session()
    is_start = main_task()
    
    #while not is_start:
    #    time.sleep(10)
    #    is_start = main_task()
    


#go_in_meet("https://bbb.comsys.kpi.ua/b/x2g-dqc-6fg", "Undef")
go_in_meet("https://bbb.comsys.kpi.ua/b/val-3gt-q6j", "Undef")
