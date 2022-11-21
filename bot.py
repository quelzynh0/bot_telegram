import os
import telegram
import time, datetime
from datetime import datetime
import pandas as pd
import configparser
from pathlib import Path
from pythonping import ping

clear = lambda: os.system('cls')
CRED = '\033[91m'
CEND = '\033[0m'

#Status dos Links
status = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
conta_status = 0

config = configparser.ConfigParser()
config.sections()
config.read('Resources/config.ini')
chat_id = config['bot_cfg']['chatId']
token_bot = config['bot_cfg']['tokenBot']
data = pd.read_excel('Resources/servidores.xls', index_col=0, na_values=['string1', 'string2', 'string3']) 
ip_list = [(ix, k, v) for ix, row in data.iterrows() for k, v in row.items()]

def send(msg, chat_id=chat_id, token=token_bot):
	bot = telegram.Bot(token=token)
	bot.sendMessage(chat_id=chat_id, text=msg)

while True:
    conta_status = 0
    now = datetime.now()
    data_hoje_string = now.strftime('%d-%m-%Y')
    mes_ano = now.strftime('%m-%Y')
    hora_string = now.strftime('%H:%M:%S')
    clear()
    for local, net, ip in ip_list:
        if ip != 0:
                response = ping(ip, size=32, count=8)
                ms = response.rtt_avg_ms
        if int(ms) < 2000:
            if ip != 0:
                if status[conta_status] == 0:
                    try:
                        send(f"🟢 {net} - {ip} ({local}) - {ms} MS - Está online")
                    except:
                        print("O envio pelo telegram falhou")
                    Path(f"Resources/log/{mes_ano}/{net}").mkdir(parents=True, exist_ok=True)      
                    log = open(f"Resources/log/{mes_ano}/{net}/{data_hoje_string}.txt","a+")
                    log.write(f"{hora_string} | {net} - {ip} ({local}) - {ms} MS - Está online\n")
                    log.close()
                status[conta_status] = 1
                print(f"{hora_string} | {net} - {ip} ({local}) - {ms} MS - Está online")
                conta_status = conta_status + 1        
        else:
            if ip != 0:
                if status[conta_status] == 1:
                    try:
                        send(f"🔴 {net} - {ip} ({local}) - Está offline")
                    except:
                        print("O envio pelo telegram falhou")
                    Path(f"Resources/log/{mes_ano}/{net}").mkdir(parents=True, exist_ok=True)      
                    log = open(f"Resources/log/{mes_ano}/{net}/{data_hoje_string}.txt","a+")
                    #log = open(f"Resources/log/{data_hoje_string}.txt","a+")
                    log.write(f"{hora_string} | {net} - {ip} ({local}) - Está offline\n")
                    log.close()
                status[conta_status] = 0
                print(CRED + f"{hora_string} | {net} - {ip} ({local}) - Está offline ↓↓↓↓↓" + CEND)
                conta_status = conta_status + 1
                
    time.sleep(30)

