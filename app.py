from quart import Quart, Response, request
from pyrogram import Client
import os

API_ID = 6
API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"

BOT_TOKEN = "9001522987:AAFpViGI2y4kvXU32CpEJEB0QlKQ1IX9C0c"
CHANNEL_ID = -1003963804386

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
        in_memory=True
    )
    await bot.start()

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
        range_header = request.headers.get('Range', None)

        if range_header:
            # استخراج بداية ونهاية البايتات المطلوبة من المتصفح
            byte_offset = int(range_header.replace('bytes=', '').split('-')[0])
            length = file_size - byte_offset

            async def generate_chunks():
                async for chunk in bot.stream_media(message, offset=byte_offset, limit=0):
                    yield chunk

            headers = {
                "Content-Type": "video/mp4",
                "Content-Range": f"bytes {byte_offset}-{file_size - 1}/{file_size}",
                "Content-Length": str(length),
                "Accept-Ranges": "bytes"
            }
            return Response(generate_chunks(), status=206, headers=headers)
        else:
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
