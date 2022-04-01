from asyncio.queues import QueueEmpty
from config import que
from pyrogram import Client, filters
from pyrogram.types import Message
from cache.admins import set
from helpers.decorators import authorized_users_only, errors
from helpers.channelmusic import get_chat_id
from helpers.command import aditya
from helpers.filters import command, other_filters
from callsmusic import callsmusic, queues
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream


ACTV_CALLS = []

@Client.on_message(aditya(["pause", "/pause", "*pause"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    await callsmusic.pytgcalls.pause_stream(message.chat.id)
    await message.reply_text("▶️😔  𝙋𝙖𝙪𝙨𝙚 🥀😔")


@Client.on_message(aditya(["resume" "/resume", "*resume"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    await callsmusic.pytgcalls.resume_stream(message.chat.id)
    await message.reply_text("⏸ 𝙍𝙚𝙨𝙪𝙢𝙚🎸 ")


@Client.on_message(aditya(["end", "/end", "*end"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    try:
        callsmusic.queues.clear(message.chat.id)
    except QueueEmpty:
        pass

    await callsmusic.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_text("❗𝙎𝙩𝙤𝙥𝙚𝙙 📳 𝙨𝙩𝙧𝙚𝙖𝙢𝙞𝙣𝙜👨‍💻")

@Client.on_message(aditya(["skip", "/skip", "*skip"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = message.chat.id
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text(" 𝙣𝙤𝙩𝙝𝙞𝙣𝙜 𝙞𝙨 𝙥𝙡𝙖𝙮𝙞𝙣𝙜 😔💢 🥀")
    else:
        queues.task_done(chat_id)
        
        if queues.is_empty(chat_id):
            await callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            await callsmusic.pytgcalls.change_stream(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        callsmusic.queues.get(chat_id)["file"],
                    ),
                ),
            )
    await message.reply_text("❗𝙎𝙠𝙞𝙥 𝙩𝙝𝙚 𝙘𝙪𝙧𝙧𝙚𝙣𝙩 𝙨𝙤𝙣𝙜🎶🙈😁")
