# 引入库文件，基于telethon
import asyncio
import time
import json
from telethon import events
# 从上级目录引入 jdbot,chat_id变量
from .. import jdbot, chat_id, logger
from ..bot.utils import cmd, env_manage_QL, TASK_CMD, AUTH_FILE
from .jdUtil import sqlite, commandDB, actionMonitor, resetMonitor,proxy, sendHelp

_cmd = ['p', 't', 's', 'm', 'mr', 'sr', 'q', 'sa']
defdict = {
    'm': actionMonitor,
    'mr': resetMonitor,
    'p': proxy
}


async def getSqlite(value):
    return sqlite.get(f"{commandDB}.{value}")


@jdbot.on(events.NewMessage(chats=chat_id, pattern=r'^/jdCommand'))
# 定义自己的函数名称
async def main(event):
    with open(AUTH_FILE, 'r', encoding='utf-8') as f:
        auth = json.load(f)
    # do something
    msg_text = event.raw_text.split(' ')
    msg = await jdbot.send_message(chat_id, '命令已经收到，准备执行')
    if len(msg_text) == 1:
        _msg = await checkCmd(msg_text, msg)
        await jdbot.edit_message(msg, _msg)
        return
    else:
        _rs = await checkCmd(msg_text, msg)
        logger.info(_rs)
        if None is not _rs:
            await jdbot.edit_message(msg, _rs)
            time.sleep(5)
            await jdbot.delete_messages(chat_id, msg)
        else:
            await jdbot.edit_message(msg, '开始执行')
        # sqlite[f"{commandDB}.monitor"] = '2323'
        # ll = getSqlite(f"{commandDB}.monitor")
        # await jdbot.send_message(chat_id, ll)
        # res = env_manage_QL('search', 'test11', auth['token'])
        # res['data'][0]['value'] = 'abcd'
        # res['data'][0]['remarks'] = 'mnbv'
        # env_manage_QL(
        #     'edit', res['data'][0], auth['token'])
        # await cmd('task raw_main_xingkong.js -a')
        # time.sleep(3)
        # msg = await jdbot.edit_message(msg, '开始执行')


async def checkCmd(msg_text, msg):
    """
    检查输入命令，执行后续的逻辑
    :param msg_text 执行命令字符串
    :param msg 会话对象
    :return:
    """
    try:
        _incmd = msg_text[1]
        logger.info(_incmd)
        if _incmd in _cmd:
            _a = _cmd.index(_incmd)
            fun = defdict.get(_incmd)
            return await fun(msg_text)
        else:
            return sendHelp()
    except Exception as e:
        logger.error(f"❌ 第{e.__traceback__.tb_lineno}行：{e}")
        return sendHelp()


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
