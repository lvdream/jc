from sqlitedict import SqliteDict
from .. import jdbot, chat_id, logger

sqlite = SqliteDict(f"data_data.sqlite", autocommit=True)
commandDB = 'jdCommand'
commandMt = 'monitor'


async def getSqlite(value):
    return sqlite.get(f"{commandDB}.{value}")


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
        logger.info(_s)
        if None == _s:
            _rs = "暂时没有找到需要监控的频道"
    logger.info(len(msg_text))
    logger.info(_rs)
    return _rs
async def resetMonitor(msg_text):
    """
    设置监控
    :return:
    """
    sqlite[f"{commandDB}.{commandMt}"] = None
    _rs = "监控重置完成"
    return _rs
