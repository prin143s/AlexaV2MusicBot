import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types.input_stream import InputAudioStream
from yt_dlp import YoutubeDL
from PIL import Image, ImageDraw, ImageFont
import asyncio
import requests

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = Client("bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
user = Client(session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)
vc = PyTgCalls(user)

ydl_opts = {"format": "bestaudio", "quiet": True}

@bot.on_message(filters.command("start"))
async def start(client, message):
    banner = "startup_banner.jpg"
    await message.reply_photo(photo=banner, caption="🎶 Welcome to VC Music Bot!\nCreated by Prince 💻")

@bot.on_message(filters.command("play") & filters.group)
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ Provide a song name or YouTube URL.")
    query = " ".join(message.command[1:])
    await message.reply("🔍 Searching & downloading...")
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            url = info['url']
            thumb_url = info['thumbnail']
            title = info['title']
            thumb_file = "thumb.jpg"
            with open(thumb_file, "wb") as f:
                f.write(requests.get(thumb_url).content)
            overlay = Image.open(thumb_file)
            draw = ImageDraw.Draw(overlay)
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
            draw.text((10, overlay.size[1] - 30), "Created by Prince", font=font, fill="white")
            overlay.save(thumb_file)

        await vc.join_group_call(
            message.chat.id,
            InputAudioStream(url),
            stream_type="local_stream"
        )
        await message.reply_photo(photo=thumb_file, caption=f"▶️ Now Playing: {title}\n🎧 Created by Prince")
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

@bot.on_message(filters.command("pause") & filters.group)
async def pause(_, message):
    await vc.pause_stream(message.chat.id)
    await message.reply("⏸️ Paused by Admin")

@bot.on_message(filters.command("resume") & filters.group)
async def resume(_, message):
    await vc.resume_stream(message.chat.id)
    await message.reply("▶️ Resumed by Admin")

@bot.on_message(filters.command("stop") & filters.group)
async def stop(_, message):
    await vc.leave_group_call(message.chat.id)
    await message.reply("🛑 Music Stopped & Left VC")

@bot.on_message(filters.command("logo"))
async def logo(_, message):
    if len(message.command) < 2:
        return await message.reply("Type something: /logo <text>")
    text = " ".join(message.command[1:])
    img = Image.new("RGB", (500, 150), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
    draw.text((20, 40), text, font=font, fill="cyan")
    draw.text((20, 100), "by Prince", font=ImageFont.truetype("DejaVuSans-Bold.ttf", 20), fill="gray")
    img.save("logo.jpg")
    await message.reply_photo("logo.jpg")

@bot.on_message(filters.command("help"))
async def help(_, message):
    txt = (
        "**🎧 VC Music Bot Help**\n"
        "Created by 👑 Prince\n\n"
        "`/play song` - Play music\n"
        "`/pause` - Pause music\n"
        "`/resume` - Resume music\n"
        "`/stop` - Leave voice chat\n"
        "`/logo text` - Make logo\n"
        "`/help` - Show this help\n\n"
        "[📢 Join Updates Channel](https://t.me/yourchannel)"
    )
    await message.reply(txt, disable_web_page_preview=True)

async def main():
    await bot.start()
    await user.start()
    await vc.start()
    print("✅ Bot is running!")
    await idle()

asyncio.run(main())
                
