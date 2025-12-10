import requests 
from dotenv import load_dotenv
import os 
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
VLLM_API_URL = "" # Placeholder for vLLM API URL if needed
HEADERS = {"Content-Type": "application/json"}

def main():
    """Start the Telegram bot."""
    # Create Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    # Run the bot
    application.run_polling()
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("thanks for contacting almost anselm! send me a message and i'll (almost) reply.")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get input from user
    user_input = update.message.text

    payload = {
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    reply_text = "okay buddy u said this: " + user_input
    # try:
    #     # Post to the backend vLLM API
    #     response = requests.post(VLLM_API_URL, json=payload, headers=HEADERS)
    #     response.raise_for_status()
    #     result = response.json()

    #     reply_text = result["choices"][0]["message"]["content"]
    # except Exception as e:
    #     reply_text = f"Error: {e}"

    await update.message.reply_text(reply_text)


if __name__ == "__main__":
    main()
