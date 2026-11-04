from quart import Quart, Response
from pyrogram import Client
import os

# --- استخدام المفاتيح العامة الرسمية لتليجرام ---
API_ID = 6
API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"

# البيانات الخاصة بك
BOT_TOKEN = "9001522987:AAFpViGI2y4kvXU32CpEJEB0QlKQ1IX9C0c"
CHANNEL_ID = -1003963804386  # تم إضافة إشارة القناة -100 لتليجرام

app = Quart(__name__)
bot = None

@app.before_serving
async def start_bot():
    global bot
    bot = Client(
        "stream_bot_session",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        in_memory=True  # يمنع طلب تسجيل الدخول التفاعلي في Render
    )
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
