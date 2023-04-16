# 引入库文件，基于telethon
import time
import json
from telethon import events
# 从上级目录引入 jdbot,chat_id变量
from .. import jdbot, chat_id
from ..bot.utils import cmd, env_manage_QL, TASK_CMD, AUTH_FILE
from .jdUtil import sqlite, commandDB

_cmd = ['proxy', 'bot', 'sub']


async def getSqlite(value):
    return sqlite.get(f"{commandDB}.{value}")


# 格式基本固定，本例子表示从chat_id处接收到包含hello消息后，要做的事情
@jdbot.on(events.NewMessage(chats=chat_id, pattern=r'^/jdCommand'))
# 定义自己的函数名称
async def main(event):
    with open(AUTH_FILE, 'r', encoding='utf-8') as f:
        auth = json.load(f)
    # do something
    msg_text = event.raw_text.split(' ')
    msg = await jdbot.send_message(chat_id, '命令已经收到，准备执行')
    if len(msg_text) == 1:
        checkCmd(msg_text, msg)
    else:

        sqlite[f"{commandDB}.monitor"] = '2323'
        ll = getSqlite(f"{commandDB}.monitor")
        await jdbot.send_message(chat_id, ll)
        res = env_manage_QL('search', 'test11', auth['token'])
        res['data'][0]['value'] = 'abcd'
        res['data'][0]['remarks'] = 'mnbv'
        env_manage_QL(
            'edit', res['data'][0], auth['token'])
        await cmd('task raw_main_xingkong.js -a')
        time.sleep(3)
        msg = await jdbot.edit_message(msg, '开始执行')


def checkCmd(msg_text, msg):
    """
    检查输入命令，执行后续的逻辑
    :param msg_text 执行命令字符串
    :param msg 会话对象
    :return:
    """
    try:
        _incmd = msg_text[1]
    except:
        sendHelp(msg)


def getProxy():
    """
    获取代理配置
    :return: 1 代理打开，0 代理关闭
    """
    isProxy = getSqlite(f"{commandDB}.proxy")
    return 1 if None is isProxy else 0;


def setProxy(cmd):
    """
    设置代理, on
    :return:
    """
    if cmd == 'on':
        sqlite[f"{commandDB}.proxy"] = '0'
    if cmd == 'off':
        sqlite[f"{commandDB}.proxy"] = None


def sendHelp(msg):
    """
    发送默认帮助说明
    :param msg:
    :return:
    """
    _msg = '\n**无效指令**\njdCommand 指令设置'
    _msg += "\n**设置代理开关[默认:关]**:\n `/jdCommand proxy on/off`"
    _msg += "\n**设置接收订阅地址**:\n `/jdCommand`"
    await jdbot.edit_message(msg, _msg)
