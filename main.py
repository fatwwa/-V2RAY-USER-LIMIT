from glob import glob
import os;
import sqlite3;
import time;
import requests;
import subprocess;
import threading;
import schedule;
_db_address = '/etc/x-ui/x-ui.db'
_max_allowed_connections = 1
_user_last_id = 0
_telegrambot_token = '5920755012:AAGz7DzgM8PmXcFqNcMbCnBbcI4bTL_zjtI' #bot ID
_telegram_chat_id = '117575426' # you can get this in @cid_bot bot.
def getUsers():
    global _user_last_id
    conn = sqlite3.connect(_db_address)
    cursor = conn.execute(f"select id,remark,port from inbounds where id > {_user_last_id}");
    users_list = [];
    for c in cursor:
        users_list.append({'name':c[1],'port':c[2]})
        _user_last_id = c[0];
    conn.close();
    return users_list

	#disable Account
def disableAccount(user_port):
    conn = sqlite3.connect(_db_address) 
    conn.execute(f"update inbounds set enable = 0 where port={user_port}");
    conn.commit()
    conn.close();
    time.sleep(20)
    os.popen("x-ui restart")
    time.sleep(30)

    #enable Account
def enableAccount(user_port):
    conn = sqlite3.connect(_db_address) 
    conn.execute(f"update inbounds set enable = 1 where port={user_port}");
    conn.commit()
    conn.close();
    time.sleep(20)
    os.popen("x-ui restart")
    time.sleep(30)
	
    #Check New Users 
def checkNewUsers():
    conn = sqlite3.connect(_db_address)
    cursor = conn.execute(f"select count(*) from inbounds WHERE id > {_user_last_id}");
    new_counts = cursor.fetchone()[0];
    conn.close();
    if new_counts > 0:
        init()
		
	#Add New User
def init():
    users_list = getUsers();
    for user in users_list:
        thread = AccessChecker(user)
        thread.start()
        print("starting checker for : " + user['name'])
class AccessChecker(threading.Thread):
    def __init__(self, user):
        threading.Thread.__init__(self)
        self.user = user;
    def run(self):
        #global _max_allowed_connections; <<if you get variable error uncomment this.
        user_remark = self.user['name'];
        user_port = self.user['port'];

        while True:
            netstate_data =  os.popen("netstat -np 2>/dev/null | grep :"+str(user_port)+" | awk '{if($3!=0) print $5;}' | cut -d: -f1 | sort | uniq -c | sort -nr | head").read();
            netstate_data = str(netstate_data)
            connection_count =  len(netstate_data.split("\n")) - 1;
            x=0
            time.sleep(10)
            while connection_count > _max_allowed_connections:
                x=x+1
                if x==1:
                    user_remark = user_remark.replace(" ","%20")
                    requests.get(f'https://api.telegram.org/bot{_telegrambot_token}/sendMessage?chat_id={_telegram_chat_id}&text={user_remark}%20:%20{user_port}%20locked%20By%20{connection_count}%20Connection')
                    print(f"{user_remark} with {connection_count}%20Connection and port {user_port} blocked")
                    disableAccount(user_port=user_port)   #درصورت غیر فعال کردن حکلت غیرفعالیه خودگار این خط را کامنت کنید
                    (user_port_blocked)=user_port 
                    time.sleep(1000)
                netstate_data =  os.popen("netstat -np 2>/dev/null | grep :"+str(user_port_blocked)+" | awk '{if($3!=0) print $5;}' | cut -d: -f1 | sort | uniq -c | sort -nr | head").read();
                netstate_data = str(netstate_data)
                connection_count =  len(netstate_data.split("\n")) - 1;
                if connection_count > _max_allowed_connections:
                    time.sleep(1000)
                else: 
                    requests.get(f'https://api.telegram.org/bot{_telegrambot_token}/sendMessage?chat_id={_telegram_chat_id}&text={user_remark}%20:%20{user_port}%20Unlocked%20By%20{connection_count}%20Connection')
                    enableAccount(user_port=user_port)     #درصورت غیر فعال کردن فعال شدن خودگار این خط را کامنت کنید
                    print(f"{user_remark} with {connection_count}%20Connection and port {user_port} Unlocked")
                    time.sleep(100)
 

init();
schedule.every(1).minutes.do(checkNewUsers)
while True:
    schedule.run_pending()
    time.sleep(1)