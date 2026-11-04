from quart import Quart, Response
from pyrogram import Client
import os

# --- استخدام المفاتيح العامة لتليجرام ---
API_ID = 6
API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"

# سحب البيانات أماناً من Environment Variables في Render
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "0"))

app = Quart(__name__)

# تعريف متغير البوت
bot = None

@app.before_serving
async def start_bot():
    global bot
    bot = Client("stream_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    await bot.start()
    print("🤖 تم تشغيل سيرفر البث بنجاح")

@app.after_serving
async def stop_bot():
    global bot
    if bot:
        await bot.stop()

@app.route('/')
async def home():
    return "سيرفر البث يعمل بنجاح! 🚀"

@app.route('/stream/<int:message_id>')
async def stream_video(message_id):
    try:
        if not bot:
            return "السيرفر غير جاهز بعد", 500

        message = await bot.get_messages(CHANNEL_ID, message_id)
        if not message or not message.video:
            return "الفيديو غير موجود في القناة", 404

        file_size = message.video.file_size

        async def generate_chunks():
            async for chunk in bot.stream_media(message, limit=0):
                yield chunk

        headers = {
            "Content-Type": "video/mp4",
            "Content-Length": str(file_size),
            "Accept-Ranges": "bytes"
        }
        
        return Response(generate_chunks(), headers=headers)

    except Exception as e:
        return f"حدث خطأ أثناء نقل البث: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
