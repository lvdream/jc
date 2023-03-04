from pagermaid import bot, log, scheduler
from pagermaid.single_utils import sqlite
from pagermaid.enums import Message
from pagermaid.utils import lang, edit_delete
from pagermaid.listener import listener
import json
from datetime import datetime, timedelta, timezone
from asyncio import sleep
import re

# ⚠ 容器Bot ID 或 用户名（推荐用户名）
# USER_BOT = 1234567890 或 USER_BOT = "xxxxxx_bot"，注意如果是id不要带引号
USER_BOT = "5659441760"
# 调试模式
DEBUG_MODE = True
commandDB = 'jdCommand'


def getTimes(format):
    TZ = timezone(timedelta(hours=8), name='Asia/Shanghai')
    times_now = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(TZ)
    return times_now.strftime(format)


async def debugMode(msg):
    DEBUG_MODE = await getSqlite('debug')
    if DEBUG_MODE == 'on':
        await bot.send_message(USER_BOT, getTimes('%Y-%m-%d %H:%M:%S') + f"\n🔧 debug: {msg}")
    else:
        return


async def infoLog(msg, _bot):
    await bot.send_message(_bot, getTimes('%Y-%m-%d %H:%M:%S') + f"\n info: \n{msg}")


async def getSqlite(value):
    return sqlite.get(f"{commandDB}.{value}")


@listener(is_plugin=False, outgoing=True, command="jdCommand",
          description='\njd 指令设置',
          parameters="`"
                     "\n\n**查询监控频道**:\n `,jdCommand monitor-search <频道/组,ID，留空查询全部>`"
                     "\n\n**设置/更新监控频道**:\n `,jdCommand monitor-set <频道/组,ID>`"
                     "\n\n**移除监控频道**:\n `,jdCommand monitor-del <频道/组,ID>`"
                     "\n\n**打开监控调试**:\n `,jdCommand debug on/off`"
                     "\n\n**设置接收命令bot**:\n `,jdCommand bot`"
                     "\n\n**查看当前队列**:\n `,jdCommand queue`"
                     "\n\n**查询监控命令**:\n `,jdCommand code-search <字符串>`"
                     "\n\n**设置监控命令**:\n `,jdCommand code-set {k:监控关键字，v:执行的命令}`"
                     "\n\n**删除监控命令**:\n `,jdCommand code-del <k:关键字>`\n")
async def config(message: Message):
    cMD = message.parameter[0]
    cId = ''
    try:
        cId = message.parameter[1]
    except:
        cId = None
    if len(message.parameter) > 2:
        cId = message.parameter[1]
        for i in range(len(message.parameter)):
            if i > 1:
                cId += ' ' + message.parameter[i]
    # 查询监控频道
    if cMD == "monitor-search":
        fId = await getSqlite(f'monitor')
        if None is cId:
            await edit_delete(message, f'10秒后删除，现有监控频道[{str(fId)}].', 10)
            return
        else:
            if None is fId:
                await edit_delete(message, f'该{cId}没有找到')
                return
            else:
                if cId not in fId:
                    await edit_delete(message, f'该{cId}没有找到')
                else:
                    await edit_delete(message, f'该{cId}已设置')
    elif cMD == "monitor-set":
        try:
            fId = await getSqlite(f'monitor')
            if None is fId:
                fId = []
                fId.append(cId)
                sqlite[f"{commandDB}.monitor"] = fId
                await edit_delete(message, f"✅ {cId}.监控已设置")
            else:
                if cId not in fId:
                    fId.append(cId)
                    sqlite[f"{commandDB}.monitor"] = fId
                    await edit_delete(message, f"✅ {cId}.监控已设置")
                else:
                    await edit_delete(message, f"❌ {cId}.该监控已经设置过了")
        except:
            await edit_delete(message, "❌ 目标对话没有启用监控")
            return
    elif cMD == "monitor-del":
        try:
            fId = await getSqlite(f'monitor')
            if None is fId:
                await edit_delete(message, f"❌ {cId}.没有匹配要删除的对象")
            else:
                if cId not in fId:
                    await edit_delete(message, f"❌ {cId}.没有匹配要删除的对象")
                else:
                    fId.remove(cId)
                    sqlite[f"{commandDB}.monitor"] = fId
                    await edit_delete(message, f"✅ {cId}.该监控已经移除")
        except:
            await edit_delete(message, "❌ 目标对话没有启用监控")
            return
    elif cMD == "debug":
        if cId is not None:
            sqlite[f"{commandDB}.debug"] = cId
            await edit_delete(message, f"✅ debug {cId}.已设置")
    elif cMD == "bot":
        if cId is not None:
            sqlite[f"{commandDB}.bot"] = cId
            await edit_delete(message, f"✅ bot {cId}.已设置")
        else:
            dId = await getSqlite(f'bot')
            if None is dId:
                await edit_delete(message, f"✅ bot 还未设置")
                return
            else:
                await edit_delete(message, f"✅ bot {dId}已设置")
    elif cMD == "code-search":
        dId = await getSqlite(f'code')
        if None is cId:
            await edit_delete(message, f'10秒后删除，现有监控指令[{str(dId)}].', 10)
            return
    elif cMD == "code-set":
        dId = await getSqlite(f'code')
        if None is cId:
            await edit_delete(message, "❌ 不支持空白指令")
            return
        _cid = json.loads(str(cId))
        if None is _cid['k'] or None is _cid['v']:
            await edit_delete(message, "❌ 设置格式不正确，{k:监控关键字，v:执行的命令}")
            return
        if None is dId:
            dId = '{}'
        await log(f",jdCommand dId ：{dId}")  # 打印日志
        kId = eval(str(dId))
        kId[_cid['k']] = _cid['v']
        sqlite[f"{commandDB}.code"] = kId
        await edit_delete(message, f"✅ code {_cid['k']}.已设置")
    elif cMD == "code-del":
        dId = await getSqlite(f'code')
        if None is cId:
            await edit_delete(message, "❌ 不支持空白指令")
            return
        _cid = json.loads(str(cId))
        if None is _cid['k']:
            await edit_delete(message, "❌ 设置格式不正确，{k:监控关键字}")
            return
        if None is dId:
            dId = '{}'
        await log(f",jdCommand dId ：{dId}")  # 打印日志
        kId = eval(str(dId))
        kId.pop(_cid['k'])
        sqlite[f"{commandDB}.code"] = kId
        await edit_delete(message, f"✅ code {_cid['k']}.已清除")
    elif cMD == "queue":
        try:
            _timer = await getSqlite(f'timer')
            _msg = '队列信息如下[100秒以后删除]:\n'
            if None is not _timer:
                _codes = list(_timer.keys())
                for i in range(len(_codes)):
                    _codeQueue = await getSqlite(f'{_codes[i]}')
                    _msg += f'队列[{_codes[i]},长度[{len(list(_codeQueue))}]]\n'
            await edit_delete(message, f"{_msg}", 100)
        except Exception as e:
            await log(f"❌ 第{e.__traceback__.tb_lineno}行：{e}")  # 打印日志


@listener(is_plugin=True, incoming=True, ignore_edited=True)
async def forward_message(message: Message):
    try:
        if message.chat:
            await debugMode(f'message.chat.name={message.chat.title},message.chat.id={message.chat.id}')
            fId = await getSqlite(f'monitor')
            if str(message.chat.id) in fId:
                text = message.text
                await filters(text)
            else:
                await debugMode(f'message.chat.id={message.chat.id},fId={fId}')
    except Exception as e:
        errorMsg = f"❌ 第{e.__traceback__.tb_lineno}行：{e}"
        await debugMode(errorMsg)


# 查看是否需要发送指令，过滤无效信息
async def filters(text):
    try:
        if "task env edit " in text or "export" in text:
            await log(f",text ：{text}")  # 打印日志
            dId = await getSqlite(f'code')
            _bot = await getSqlite(f'bot')
            all = str(text).replace('export ', '')
            all = str(all).replace('="', '----')
            # 以防最后一个双引号后面还有内容
            all = all.split('"')[0] + '"'
            all = str(all).replace('"', '')
            _code = all.split('----')[0]
            _url = all.split('----')[1]
            if None is _bot:
                await edit_delete(text, f"❌ bot机器人未设置！")
                return
            if str(_code) in dId.keys():
                cmd = str(dId[_code]).replace('$url$', _url)
                await infoLog(f",找到对应指令：{cmd},发送到机器人", _bot)  # 打印日志
                # await bot.send_message(_bot, cmd)
                await addQueue(_code, cmd)
            else:
                await infoLog(f",未找到对应指令：[{_code}]", _bot)  # 打印日志
        elif 'https' in text:
            all = text.split('https')
            _bot = await getSqlite(f'bot')
            await infoLog(f",找到需要解析的url：[{all[0]}],[{all[1]}]", _bot)  # 打印日志
    except Exception as e:
        errorMsg = f"❌ 第{e.__traceback__.tb_lineno}行：{e}"
        await debugMode(errorMsg)


# 队列判断和操作
# @code 执行的代码
# @cmd 执行的命令
async def addQueue(code, cmd):
    # 获取当前队列的长度
    _codeQueue = await getSqlite(f'{code}')
    _timer = await getSqlite(f'timer')
    if None is _timer:
        _timer = {f"{code}": f"{getTimes('%Y-%m-%d %H:%M:%S')}"}
    else:
        if code not in _timer.keys():
            _timer[f"{code}"] = getTimes('%Y-%m-%d %H:%M:%S')
    sqlite[f"{commandDB}.timer"] = _timer
    if None is _codeQueue:
        _codeQueue = []
        sqlite[f"{commandDB}.{code}_timer"] = getTimes('%Y-%m-%d %H:%M:%S')
    _codeQueue.append(cmd)  # 追加命令
    sqlite[f"{commandDB}.{code}"] = _codeQueue
    await log(f",jdCommand _timer ：添加成功")  # 打印日志


@scheduler.scheduled_job("interval", seconds=5)
async def checkScheduled_job():
    try:
        _timer = await getSqlite(f'timer')
        if None is _timer:
            await log(f",jdCommand _timer ：None")  # 打印日志
        else:
            _codes = list(_timer.keys())
            for i in range(len(_codes)):
                _codeQueue = await getSqlite(f'{_codes[i]}')
                if None is _codeQueue:
                    _timer.remove(_codes[i])
                else:
                    _pvalue = _timer.get(_codes[i])
                    _pvalue = str(_pvalue).replace("{'", '')
                    _pvalue = str(_pvalue).replace("'}", '')
                    # 找到队列任务
                    _codeQueue = await getSqlite(f'{_codes[i]}')
                    # await log(f",jdCommand _timer _codeQueue ：{_codeQueue}")  # 打印日志
                    if None is not _codeQueue and len(_codeQueue) > 0:
                        # 对应值的更新时间
                        _time_01 = datetime.strptime(str(_pvalue), "%Y-%m-%d %H:%M:%S")
                        # 追加10分钟
                        minutes_after_10 = _time_01 + timedelta(minutes=10)
                        _time_02 = datetime.strptime(getTimes("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                        # 当前时间大于，设计时间加10分钟，则队列可以放行一个
                        if minutes_after_10 < _time_02:
                            # await log(f",jdCommand _timer compare ：{_time_02},{minutes_after_10}")  # 打印日志
                            # await log(f",jdCommand _timer compare ：{minutes_after_10 < _time_02}")  # 打印日志
                            cTask = _codeQueue[0]
                            _bot = await getSqlite(f'bot')
                            await bot.send_message(_bot, cTask)
                            del _codeQueue[0]
                            _timer[_codes[i]] = getTimes("%Y-%m-%d %H:%M:%S")
                            sqlite[f"{commandDB}.timer"] = _timer
                        # await bot.send_message(_bot, cTask)
                        # del _codeQueue[0]
                    elif None is not _codeQueue and len(_codeQueue) == 0:
                        _timer.remove(_codes[i])
                        sqlite[f"{commandDB}.timer"] = _timer
            # await log(f",jdCommand _timer ：{_timer}")  # 打印日志
    except Exception as e:
        await log(f"❌ 第{e.__traceback__.tb_lineno}行：{e}")  # 打印日志
