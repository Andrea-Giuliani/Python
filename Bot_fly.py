#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: giuliani
"""

import requests
NEW_LINE = '\n'

print('Von:')
von = input() # ber
print('Nach:')
nach = input() # vie

print('Month start:')
month_start = input() # 01, 02, 03

print('Month finish:')
month_finish = input() # 01, 02, 03


url = f'https://www.skyscanner.de/transport/fluge/{von}/{nach}/%3Foym=21{month_start}%26selectedoday=24%26iym=21{month_finish}%26selectediday=24'
print(url)


def telegram_bot_sendtext(bot_message):
    
    bot_token = ''
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
    

Flight = telegram_bot_sendtext("These are the cheapest flights given your selected criteria" + NEW_LINE + url)
print(Flight)


