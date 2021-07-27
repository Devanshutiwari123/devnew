# pylint: disable=missing-module-docstring
#
# Copyright (C) 2020-2021 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

from glob import glob
from signal import SIGTERM
from os import environ, getpid, kill
from os.path import isfile, relpath
from typing import Dict, List, Union

_SECURE = [
    # critical
    'API_ID', 'API_HASH', 'BOT_TOKEN', 'HU_STRING_SESSION', 'DATABASE_URL', 'HEROKU_API_KEY',
    # others
    'INSTA_ID', 'INSTA_PASS', 'SPAM_WATCH_API', 'CURRENCY_API', 'OCR_SPACE_API_KEY',
    'REMOVE_BG_API_KEY', 'G_DRIVE_CLIENT_ID', 'G_DRIVE_CLIENT_SECRET',
    # unofficial
    'ARL_TOKEN', 'GCS_API_KEY', 'GCS_IMAGE_E_ID', 'G_PHOTOS_CLIENT_ID',
    'G_PHOTOS_CLIENT_SECRET', 'CH_LYDIA_API']


class SafeDict(Dict[str, str]):
    """ modded dict """
    def __missing__(self, key: str) -> str:
        return '{' + key + '}'


def get_import_path(root: str, path: str) -> Union[str, List[str]]:
    """ return import path """
    seperator = '\\' if '\\' in root else '/'
    if isfile(path):
        return '.'.join(relpath(path, root).split(seperator))[:-3]
    all_paths = glob(root + path.rstrip(seperator) + f"{seperator}*.py", recursive=True)
    return sorted(
        [
            '.'.join(relpath(f, root).split(seperator))[:-3] for f in all_paths
            if not f.endswith("__init__.py")
        ]
    )


def terminate() -> None:
    """ terminate programme """
    kill(getpid(), SIGTERM)

def check_owner(func):
    async def wrapper(_, c_q: CallbackQuery):
        if c_q.from_user and (
            c_q.from_user.id in Config.OWNER_ID or c_q.from_user.id in Config.SUDO_USERS
        ):
            try:
                await func(c_q)
            except FloodWait as e:
                await asyncio.sleep(e.x + 5)
            except MessageNotModified:
                pass
        else:
            await c_q.answer(
                "Only My Master can Access This !!\n\n     𝘿𝙚𝙥𝙡𝙤𝙮 𝙮𝙤𝙪𝙧 𝙤𝙬𝙣 𝙐𝙎𝙀𝙍𝙂𝙀-𝙓",
                show_alert=True,
            )

    return wrapper

def secure_text(text: str) -> str:
    """ secure given text """
    if not text:
        return ''
    for var in _SECURE:
        tvar = environ.get(var)
        if tvar and tvar in text:
            text = text.replace(tvar, "[SECURED!]")
    return text
