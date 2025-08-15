import os
import asyncio
import logging
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# -----------------------------
# LOG AYARLARI
# -----------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# -----------------------------
# TOKEN KONTROLÜ
# -----------------------------
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment değişkeni tanımlı değil!")

bot = Bot(TOKEN)
app = Flask(__name__)

# -----------------------------
# Videolar ve linkler
# -----------------------------
GUSUL_VIDEO_ID = "BAACAgQAAxkBAANKaJ3cEF99UmwNx0q0AhXGSS40YhgAAqIXAAJDHPFQ_yxAWpLMewQ2BA"
DAARAT_VIDEO_ID = "BAACAgQAAxkBAANdaJ3rrfsXVOKmlMF7X0eGu_ymaBIAAq4XAAJDHPFQaSNM38vA9ZQ2BA"
NAMAZ_VIDEO_ID = "BAACAgQAAxkBAANnaJ3whloNqbji9bSw-_0Lz9RpP8YAAr0XAAJDHPFQgKVWC5hJFhU2BA"
NAMAZ_VIDEO_LINK = "https://www.youtube.com/playlist?list=PLgfsDRXXIm97Y3IW4JWGTI-GcvZ8Dt6gE"
SURELER_LINK = "https://www.youtube.com/playlist?list=PLEzrCOBjn_28LQWQ3W_J8CNBMy1xYJhjP"

# -----------------------------
# Ders Handler’ları
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Ооба", callback_data="yes"),
         InlineKeyboardButton("❌ Жок", callback_data="no")]
    ]
    await update.message.reply_text(
        "Салам! Мен сага намазды жеңил жана түшүнүктүү жол менен үйрөтө турган ботмун.\nҮйрөнүүгө даярсыңбы?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "yes":
        keyboard = [[InlineKeyboardButton("✅ Башта", callback_data="start_lesson")]]
        text = (
            "🌟 Бул жерде сен намазды толук үйрөнөсүң:\n"
            "🛁 Гусул жана даарат – туура жасоо ыкмалары\n"
            "🕋 Намаздын ар бир шарты – кадам кадам түшүндүрмө\n"
            "🎥 Беш убак намаз – видео көрсөтмөлөр менен\n"
            "📖 Жаттоо үчүн керектүү дуба жана сүрөлөр\n\n"
            "➡️ Сабакка баштоо үчүн төмөнкү “Башта” баскычына бас:"
        )
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await query.edit_message_text("Макул, даяр болгондо кайрыл 🌿")

async def lesson_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📘 Алгачкы сабагыбыз – Гусул. Бул сабакта гусул тууралуу үйрөнөсүз.")
    keyboard = [[InlineKeyboardButton("➡️ Кийинки", callback_data="daarat_lesson")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_video(
        chat_id=query.message.chat_id,
        video=GUSUL_VIDEO_ID,
        caption="Гусул сабагынын видеосу",
        reply_markup=reply_markup,
        protect_content=True
    )

async def daarat_lesson_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📘 Кийинки сабак – Даарат. Бул сабакта даарат алуу жолун үйрөнөсүз.")
    keyboard = [[InlineKeyboardButton("➡️ Кийинки", callback_data="next_lesson")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_video(
        chat_id=query.message.chat_id,
        video=DAARAT_VIDEO_ID,
        caption="Даарат сабагынын видеосу",
        reply_markup=reply_markup,
        protect_content=True
    )

async def next_lesson_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📘 Кийинки сабак – Намаз. Бул сабакта намаз тууралуу үйрөнөсүз.")
    keyboard = [[InlineKeyboardButton("➡️ Кийинки", callback_data="short_suras")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_video(
        chat_id=query.message.chat_id,
        video=NAMAZ_VIDEO_ID,
        caption="Намаз сабагынын видеосу",
        reply_markup=reply_markup,
        protect_content=True
    )

async def short_suras_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("📖 Сүрөлөргө өтүү", url=SURELER_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "📖 Сизге жөнөтүлгөн шилтемеден намазда окулуучу кыска Куран сүрөлөрүн үйрөнө аласыз.",
        reply_markup=reply_markup
    )
    next_keyboard = [[InlineKeyboardButton("➡️ Кийинки", callback_data="end_lesson")]]
    next_reply_markup = InlineKeyboardMarkup(next_keyboard)
    await query.message.reply_text(
        "Сүрөлөр менен таанышкандан кийин кийинки бөлүмгө өтүңүз.",
        reply_markup=next_reply_markup
    )

async def end_lesson_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("📖 Улантуу", callback_data="namaz_info")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        f"➡️ Кийинки сабак – Намаз.\nБул сабакта беш убак намазды үйрөнөсүз.\n\n📺 Видео менен үйрөнүү: {NAMAZ_VIDEO_LINK}",
        reply_markup=reply_markup
    )

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
        "Сабак бүткөндөн кийин ‘Бүттүрүү’ баскычын басып, кийинки бөлүмгө өтүңүз:", reply_markup=reply_markup
    )

# -----------------------------
# Final ve Donation Handler
# -----------------------------
async def final_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    final_text = (
        "🎉 Куттуктайбыз! Сиз намаз үйрөнүү сабагын ийгиликтүү аяктадыңыз.\n"
        "Бул чоң жетишкендик, эми күнүмдүк ибадатыңызда бул билимди колдонсоңуз болот.\n\n"
        "📌 Бул бот aitat.mektebi Instagram баракчасы тарабынан даярдалды:\n"
        "https://www.instagram.com/aiat.mektebi\n"
        "Биздин баракча аркылуу дагы көп руханий билимдерди жана практикалык сабактарды таба аласыз."
    )
    keyboard = [[InlineKeyboardButton("💡 Колдоо көрсөтүү", callback_data="donation_message")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(final_text, reply_markup=reply_markup)

async def donation_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    donation_text = (
        "💡 Бул кызмат толугу менен акысыз.\n"
        "Бирок биздин долбоорлордун өнүгүшүнө салым кошууну кааласаңыз, каражат жөнөтө аласыз.\n\n"
        "Эгер салым кошууну кааласаңыз, төмөнкү '✅ Салым кошуу' баскычын басып улантыңыз.\n"
        "Эгер чыккыңыз келсе, '❌ Жок' баскычын басып, отурумуңузду токтотсоңуз болот."
    )
    keyboard = [
        [InlineKeyboardButton("✅ Салым кошуу", callback_data="start_donation")],
        [InlineKeyboardButton("❌ Жок", callback_data="exit_session")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(donation_text, reply_markup=reply_markup)

async def start_donation_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    donation_info = "💳 Салым кошуу үчүн бул шилтемеге кириңиз:\nM Bank БЕГИМЖАН А. +996 (508) 050 268"
    await query.message.reply_text(donation_info)

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
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        logger.info(f"Update alındı: {update}")
        asyncio.create_task(application.process_update(update))
    except Exception as e:
        logger.error(f"Webhook işlem hatası: {e}")
    return "ok", 200

@app.route("/")
def index():
    return "Bot çalışıyor!", 200

# -----------------------------
# Flask çalıştırma
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Flask {port} portunda başlatılıyor...")
    app.run(host="0.0.0.0", port=port)
