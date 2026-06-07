from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, CallbackQueryHandler, ContextTypes

# ضع التوكن الخاص بك هنا بدلاً من النص الموجود بين علامتي التنصيص
TOKEN = '8760224750:AAHAHbI_FhwMSao4I_nDAtzcor4hI-NACvA'

WELCOME_MESSAGE = (
    "**היי 👋🏻 {name}**\n\n"
    "**בכדי להיכנס ל- ישראליות בלעדיות 2026 עליך לשתף את הקישור ל-10 קבוצות מינימום‼️**\n\n"
    "**במידה ושיתפת את/ה תאושר/י באופן אוטומטי, האישור יכול לקחת עד 24 שעות מרגע השיתוף, התאזר/י בסבלנות.**\n\n"
    "✖️✖️✖️✖️✖️✖️✖️✖️✖️✖️\n\n"
    "**לחץ /start לרענון הבוט**"
)

async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    
    keyboard = [
        [InlineKeyboardButton("שתף את הקישור לערוץ 🔗", url="https://t.me/share/url?url=https://t.me/+iW43dzHvntM4NTI1")],
        [InlineKeyboardButton("❌ חובה הצטרפות לאישור ❌", url="https://t.me/Sjdndndbbot")],
        [InlineKeyboardButton("בדיקת מצב הצטרפות 🔍", callback_data="check_status")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await context.bot.send_message(
            chat_id=user.id, 
            text=WELCOME_MESSAGE.format(name=user.first_name),
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        print(f"Error: {e}")
    
    await update.chat_join_request.approve()

async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    # الرسالة المنبثقة الثابتة
    alert_text = "❌ אין לך גישה \nחמשפר הכניסות לקישור שלך: 0 מתוך 10 כניסות"
    await query.answer(text=alert_text, show_alert=True)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(ChatJoinRequestHandler(approve_request))
    app.add_handler(CallbackQueryHandler(check_button))
    
    print("البوت يعمل الآن...")
    app.run_polling()

