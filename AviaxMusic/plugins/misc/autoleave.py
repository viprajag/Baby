import asyncio
from datetime import datetime
from pyrogram.enums import ChatType
from pytgcalls.exceptions import GroupCallNotFound
import config
from AviaxMusic import app
from AviaxMusic.misc import db
from AviaxMusic.core.call import Aviax, autoend, counter
from AviaxMusic.utils.database import get_client, set_loop, is_active_chat, is_autoend, is_autoleave
import logging


                    
async def auto_end():
    global autoend, counter
    while True:
        await asyncio.sleep(60)
        try:
            ender = await is_autoend()
            if not ender:
                continue
            chatss = autoend
            keys_to_remove = []
            nocall = False
            for chat_id in chatss:
                try:
                    users = len(await Aviax.call_listeners(chat_id))
                except GroupCallNotFound:
                    users = 1
                    nocall = True
                except Exception:
                    users = 100
                timer = autoend.get(chat_id)
                if users == 1:
                    res = await set_loop(chat_id, 0)
                    keys_to_remove.append(chat_id)
                    try:
                        await db[chat_id][0]["mystic"].delete()
                    except Exception:
                        pass
                    try:
                        await Aviax.stop_stream(chat_id)
                    except Exception:
                        pass
                    try:
                        if not nocall:
                            await app.send_message(chat_id, "» ʙᴏᴛ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʟᴇғᴛ ᴠɪᴅᴇᴏᴄʜᴀᴛ ʙᴇᴄᴀᴜsᴇ ɴᴏ ᴏɴᴇ ᴡᴀs ʟɪsᴛᴇɴɪɴɢ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ.")
                    except Exception:
                        pass
            for chat_id in keys_to_remove:
                del autoend[chat_id]
        except Exception as e:
            logging.info(e)

asyncio.create_task(auto_end())
