import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# -----------------------------
# Ortam değişkeninden TOKEN al
# -----------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN ortam değişkeni bulunamadı!")

bot = Bot(TOKEN)

# -----------------------------
# Flask app
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Basit start handler
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Ооба", callback_data="yes"),
         InlineKeyboardButton("❌ Жок", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Салам! Мен сага намазды жеңил жана түшүнүктүү жол менен үйрөтө турган ботмун.\nҮйрөнүүгө даярсыңбы?",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "yes":
        keyboard = [[InlineKeyboardButton("✅ Башта", callback_data="start_lesson")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "🌟 Бул жерде сен намазды толук үйрөнөсүң. Сабакты баштоо үчүн төмөнкү “Башта” баскычын бас:", 
            reply_markup=reply_markup
        )
    else:
        await query.edit_message_text("Макул, даяр болгондо кайрыл 🌿")

async def lesson_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📘 Алгачкы сабагыбыз – Гусул. Бул сабакта гусул тууралуу үйрөнөсүз.")
    keyboard = [[InlineKeyboardButton("➡️ Кийинки", callback_data="daarat_lesson")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Гусул сабагынын видеосу (тест): https://youtube.com", reply_markup=reply_markup)

async def daarat_lesson_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📘 Кийинки сабак – Даарат. Бул сабакта даарат алуу жолун үйрөнөсүз.")
    keyboard = [[InlineKeyboardButton("➡️ Кийинки", callback_data="next_lesson")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Даарат сабагынын видеосу (тест): https://youtube.com", reply_markup=reply_markup)

async def next_lesson_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📘 Кийинки сабак – Намаз. Бул сабакта намаз тууралуу үйрөнөсүз.")
    keyboard = [[InlineKeyboardButton("➡️ Кийинки", callback_data="short_suras")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Намаз сабагынын видеосу (тест): https://youtube.com", reply_markup=reply_markup)

async def short_suras_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("📖 Сүрөлөргө өтүү", url="https://youtube.com")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("📖 Сизге жөнөтүлгөн шилтемеден намазда окулуучу кыска Куран сүрөлөрүн үйрөнө аласыз.", reply_markup=reply_markup)
    next_keyboard = [[InlineKeyboardButton("➡️ Кийинки", callback_data="end_lesson")]]
    next_reply_markup = InlineKeyboardMarkup(next_keyboard)
    await query.message.reply_text("Сүрөлөр менен таанышкандан кийин кийинки бөлүмгө өтүңүз.", reply_markup=next_reply_markup)

async def end_lesson_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("📖 Улантуу", callback_data="namaz_info")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("➡️ Кийинки сабак – Намаз. Беш убак намазды үйрөнөсүз.", reply_markup=reply_markup)

async def namaz_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "*БЕШ УБАК НАМАЗ*\n\n"
        "• *Багымдат намазы:* эки рекет сүннөт, эки рекет парз.\n"
        "• *Бешим намазы:* төрт рекет сүннөт, төрт рекет парз жана эки рекет сүннөт.\n"
        "• *Аср (Дигер) намазы:* төрт рекет парз.\n"
        "• *Шам намазы:* үч рекет парз, эки рекет сүннөт.\n"
        "• *Куптан намазы:* төрт рекет парз, эки рекет сүннөт. Кийин үч рекет витир.\n\n"
        "*НАМАЗДЫН УБАКЫТТАРЫ*\n"
        "• *Багымдат намазынын убагы:* таң агаргандан баштап күн чыкканга чейинки аралык.\n"
        "• *Бешим намазынын убагы:* күн чак түштөн бир аз оогондон баштап ар бир нерсенин көлөкөсү өзү менен барабар болгонго чейинки аралык.\n"
        "• *Аср намазынын убагы:* бешимдин убагы бүткөндөн баштап күн батканга чейинки аралык.\n"
        "• *Шам намазынын убагы:* күн толугу менен баткандан тартып күндүн шапагы (кызылы) кеткенге чейинки аралык.\n"
        "• *Куптан намазынын убагы:* шам намазынын убагы толук бүткөндөн тартып багымдат намазынын убагы киргенге чейинки аралык.\n\n"
        "*ЭСКЕРТҮҮ*\n"
        "Бир күндө үч убакыт бар, ошол убактарда намаз окулбайт:\n"
        "– Эрте менен күн чыгып жатканда.\n"
        "– Күн чак түшкө келгенде.\n"
        "– Күн батып жатканда (эгер аср намазын окубаган болсо күн батып жатканда окуса болот)"
    )
    await query.message.reply_text(text, parse_mode="Markdown")
    keyboard = [[InlineKeyboardButton("➡️ Бүттүрүү", callback_data="final_message")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "Сабак бүткөндөн кийин ‘Бүттүрүү’ баскычын басып, кийинки бөлүмгө өтүңүз:", 
        reply_markup=reply_markup
    )


async def final_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    final_text = (
        "🎉 Куттуктайбыз! Сиз намаз үйрөнүү сабагын ийгиликтүү аяктадыңыз.\n"
        "Бул чоң жетишкендик, эми күнүмдүк ибадатыңызда бул билимди колдонсоңуз болот.\n\n"
        "📌 Бул бот aitat.mektebi Instagram баракчасы тарабынан даярдалды."
    )
    keyboard = [[InlineKeyboardButton("💡 Колдоо көрсөтүү", callback_data="donation_message")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(final_text, reply_markup=reply_markup)

async def donation_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    donation_text = "💡 Бул кызмат толугу менен акысыз. Салым кошуу үчүн төмөнкү баскычты колдонуңуз."
    keyboard = [[InlineKeyboardButton("✅ Салым кошуу", callback_data="start_donation")],
                [InlineKeyboardButton("❌ Жок", callback_data="exit_session")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(donation_text, reply_markup=reply_markup)

async def start_donation_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("💳 Салым кошуу үчүн бул шилтемеге кириңиз:\nM Bank БЕГИМЖАН А. +996 (508) 050 268")

async def exit_session_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("🚪 Сиз отурумдан чыктыңыз. Рахмат!")

# -----------------------------
# Application ve Handler Ekleme
# -----------------------------
application = Application.builder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_handler, pattern="^(yes|no)$"))
application.add_handler(CallbackQueryHandler(lesson_start_handler, pattern="^start_lesson$"))
application.add_handler(CallbackQueryHandler(daarat_lesson_handler, pattern="^daarat_lesson$"))
application.add_handler(CallbackQueryHandler(next_lesson_handler, pattern="^next_lesson$"))
application.add_handler(CallbackQueryHandler(short_suras_handler, pattern="^short_suras$"))
application.add_handler(CallbackQueryHandler(end_lesson_handler, pattern="^end_lesson$"))
application.add_handler(CallbackQueryHandler(namaz_info_handler, pattern="^namaz_info$"))
application.add_handler(CallbackQueryHandler(final_message_handler, pattern="^final_message$"))
application.add_handler(CallbackQueryHandler(donation_message_handler, pattern="^donation_message$"))
application.add_handler(CallbackQueryHandler(start_donation_handler, pattern="^start_donation$"))
application.add_handler(CallbackQueryHandler(exit_session_handler, pattern="^exit_session$"))

# -----------------------------
# Webhook endpoint
# -----------------------------
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(application.process_update(update))
    return "ok"

@app.route("/")
def index():
    return "Bot çalışıyor!"

# -----------------------------
# Flask çalıştırma
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
   
