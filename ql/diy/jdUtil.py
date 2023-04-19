from sqlitedict import SqliteDict
from .. import jdbot, chat_id, logger

sqlite = SqliteDict(f"data_data.sqlite", autocommit=True)
commandDB = 'jdCommand'
commandMt = 'monitor'
commandPxy = 'pxy'


async def getSqlite(value):
    return sqlite.get(f"{commandDB}.{value}")


async def setSqlite(key, values):
    sqlite[f"{commandDB}.{key}"] = values


def sendHelp():
    """
    发送默认帮助说明
    :param msg:
    :return:
    """
    _msg = '\n**无效指令**\njdCommand 指令设置'
    _msg += "\n**监控频道[频道/组/个人,留空查询]**:\n `/jdCommand m`"
    _msg += "\n**监控频道重置**:\n `/jdCommand mr`"
    _msg += "\n**设置代理开关[默认:关]**:\n `/jdCommand p on/off`"
    _msg += "\n**查看队列信息**:\n `/jdCommand q`"
    _msg += "\n**设置队列间隔时间[单位秒,默认120秒,无参数默认查询]**:\n `/jdCommand t`"
    _msg += "\n**设置订阅地址[无参数默认查询]**:\n `/jdCommand s`"
    _msg += "\n**设置添加订阅地址[地址相同不会添加]**:\n `/jdCommand sa 地址`"
    _msg += "\n**设置重置订阅地址**:\n `/jdCommand sr`"
    return _msg


async def actionMonitor(msg_text):
    """
    设置监控
    :return:
    """
    _rs = ""
    if len(msg_text) == 2:
        """
        没有参数，默认查询
        """
        _s = await getSqlite(commandMt)
        if None == _s:
            _rs = "暂时没有找到需要监控的频道"
        else:
            _rl = str(_s).split(',')
            _rs = "当前监控的频道如下:\n"
            _rl = '**&&'.join(_rl)
            _rl = '[' + _rl.replace("**", "]\n").replace("&&", "[")
            _rs = _rs + _rl + ']'
    else:
        _c = msg_text[2]
        _s = await getSqlite(commandMt)
        if None == _s:
            await setSqlite(commandMt, _c)
            _rs = f"需要监控的对象[{_c}]已设置完成"
        else:
            _rl = str(_s).split(',')
            if _c in _rl:
                _rs = f"需要监控的对象[{_c}]已存在，跳过"
            else:
                await setSqlite(commandMt, _s + ',' + _c)
                _rs = f"需要监控的对象[{_c}]已设置完成"
    return _rs


async def resetMonitor(msg_text):
    """
    设置监控
    :return:
    """
    await setSqlite(commandMt, None)
    _rs = "监控重置完成"
    return _rs


async def proxy(msg_text):
    """
    设置代理
    :return:
    """
    _rs = "当前未设置代理"
    isProxy = await getSqlite(commandPxy)
    logger.info(isProxy)
    isProxy = 0 if None is isProxy or '0' == isProxy else 1
    if 0 == isProxy:
        await setSqlite(commandPxy, '0')
    if len(msg_text) == 3:
        _set = '1' if msg_text[2] == 'on' else '0';
        _str = '[开启]' if msg_text[2] == 'on' else '[关闭]';
        await setSqlite(commandPxy, _set)
        logger.info(_set)
        _rs = f"当前代理设置{_str}成功"
    else:
        _str = '[关闭]' if 0 == isProxy else '[开启]';
        _rs = f"当前代理状态{_str}"
        _rs += f"\n设置代理命令，/jdCommand p on/off"
    return _rs
