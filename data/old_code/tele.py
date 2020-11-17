import time
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space)
from datetime import date

TOKEN = "967775629:AAEaXYZsqdkh0LnIUKukmWl6ydg_W0cX94s"

class BotStarter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(BotStarter, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)


bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, BotStarter, timeout=3)
])
MessageLoop(bot).run_as_thread()
print('Listening ...')
day = f"{date.today().day:02d}"
month = f"{date.today().month:02d}"
year = f"{date.today().year:02d}"
fFoot = ".txt"
xxx = day + month + year + fFoot
file = open('order_' + xxx, 'r')
while 1:
    where = file.tell()
    line = file.readline().replace('\'', '"')
    if not line:
        file.seek(where)
    else:
        try:
            line = line.split(' ')
            status = ''
            if line[1] == '2':
                status = 'Buy'
            elif line[1] == '1':
                status = 'Sell'
            bot.sendMessage(549485276, line[2][:-1] + ' ' + line[0] + ':' + status)
        except:
            pass
    time.sleep(1)

