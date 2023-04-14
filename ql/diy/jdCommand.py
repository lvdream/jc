# 引入库文件，基于telethon
import time
import json
from telethon import events
# 从上级目录引入 jdbot,chat_id变量
from .. import jdbot, chat_id
from ..bot.utils import cmd,env_manage_QL, TASK_CMD, AUTH_FILE

# 格式基本固定，本例子表示从chat_id处接收到包含hello消息后，要做的事情
@jdbot.on(events.NewMessage(chats=chat_id, pattern=r'^/jdCommand'))
# 定义自己的函数名称
async def hi(event):
    with open(AUTH_FILE, 'r', encoding='utf-8') as f:
        auth = json.load(f)
    # do something
    msg_text = event.raw_text.split(' ')
    msg = await jdbot.send_message(chat_id, '命令已经收到，准备执行')
    res = env_manage_QL('search', 'test11', auth['token'])
    res['data'][0]['value']='abcd'
    res['data'][0]['remarks']='mnbv'
    env_manage_QL(
        'edit', res['data'][0], auth['token'])
    await cmd('task raw_main_xingkong.js -a')
    time.sleep(3)
    msg = await jdbot.edit_message(msg, '开始执行')

