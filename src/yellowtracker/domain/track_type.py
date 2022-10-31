from enum import Enum

class TrackType(Enum):

    MVP = (1, 'MVP', 'mvp')
    MINING = (2, 'MINING LOCATION', 'mining')

    def __init__(self, id: int, desc: str, sql_desc: str):
        self.id = id
        self.desc = desc
        self.sql_desc = sql_desc
