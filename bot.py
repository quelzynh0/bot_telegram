import os
import telegram
import pandas as pd
import configparser

clear = lambda: os.system('cls')
config = configparser.ConfigParser()
config.sections()
config.read('config.ini')
chat_id = config['bot_cfg']['chatId']
token_bot = config['bot_cfg']['tokenBot']
data = pd.read_excel('servidores.xlsx', index_col=0, na_values=['string1', 'string2']) 
ip_list = [(ix, k, v) for ix, row in data.iterrows() for k, v in row.items()]

def send(msg, chat_id=chat_id, token=token_bot):
	bot = telegram.Bot(token=token)
	bot.sendMessage(chat_id=chat_id, text=msg)

clear()

for local, net, ip in ip_list:
    response = os.popen(f"ping -n 4 {ip}").read()
    if "TTL=" in response:
        if ip != 0:
            print(f"{net} - {ip} ({local}) - Está online")
    else:
        if ip != 0:
            print(f"{net} - {ip} ({local}) - Está offline")
            send(f"{net} - {ip} ({local}) - Está offline")