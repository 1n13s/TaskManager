import sqlite3
from typing import Dict, List
class Database():
    """Manages the Database
    """
    def __init__(self, database: str) -> None:
        """Initializes db"""
        self.__database=database