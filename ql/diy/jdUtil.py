from sqlitedict import SqliteDict

sqlite = SqliteDict(f"data_data.sqlite", autocommit=True)
commandDB = 'jdCommand'

async def getSqlite(value):
    return sqlite.get(f"{commandDB}.{value}")
