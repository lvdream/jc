# 引入库文件，基于telethon
import time

from telethon import events
# 从上级目录引入 jdbot,chat_id变量
from .. import jdbot, chat_id
from ..bot.utils import cmd, TASK_CMD

# 格式基本固定，本例子表示从chat_id处接收到包含hello消息后，要做的事情
@jdbot.on(events.NewMessage(chats=chat_id, pattern=r'^/jdCommand'))
# 定义自己的函数名称
async def hi(event):
    # do something
    msg_text = event.raw_text.split(' ')
    msg = await jdbot.send_message(chat_id, '命令已经收到，准备执行')
    await cmd('/cmd ql')
    time.sleep(5)
    msg = await jdbot.edit_message(msg, '开始执行')

