import os
import logging
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
မင်းက Gaming Store ရဲ့ AI Assistant ဖြစ်ပါတယ်။ 
PUBG, MLBB စတဲ့ ဂိမ်းတွေနဲ့ ပတ်သက်တဲ့ မေးခွန်းတွေ၊ Top-up ဈေးနှုန်းမေးတာတွေကို ဂိမ်းမာပုံစံ ရင်းနှီးစွာ မြန်မာလို ပြန်လည်ဖြေကြားပေးပါ။
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ! Gaming Store AI မှ ကြိုဆိုပါတယ်။ ဘာများ ကူညီပေးရမလဲခင်ဗျာ။")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
            config={'system_instruction': SYSTEM_PROMPT}
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("ခဏနေမှ ပြန်စမ်းကြည့်ပေးပါ။")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running...")
    app.run_polling()
  
