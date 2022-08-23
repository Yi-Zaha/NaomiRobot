from pyrogram import filters
from typing import List, Union
from config import Config

def command(commands: Union[str, List[str]]):
    return filters.command(commands, /)
