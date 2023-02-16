# -V2RAY-USER-LIMIT
اسکریپت محدود کردن تعداد کاربران متصل به v2ray


# Limit v2Ray Users Guidance

1 - apt update

2 - apt-add-repository -r ppa:certbot/certbot

3 - apt install python3-pip

4 - pip3 install requests

5 - pip3 install schedule

6 - apt install net-tools

7 - cd  (root access in root folder) 

8 - 
8.1 Edit main.py for yourself Configurate in your system (Allow Device: LINE 10 , T-BOT ID : LINE 12 @botfather, Your T-ID : LINE 13 @cid_bot, Lock TIME : LINE 89 -Default : time.sleep(1000)  -->ONLY EDIT NUMBERS [sec] - for minutes : num/60)

8.2 - Copy main.py File in /root/

9 - copy all text in xray configuration.txt File & Paste in XUI PANEL -> Panel Setting -> xray related settings -> xray configuration template -> intoTEXTBOX
(Replace Old)

10 - copy all text in cron.txt

11 - crontab -e

12 - Paste all text in Command 10 & save

13 - reboot

14 - TEST :D


FORCE:
nohup python3 main.py
python3 main.py
