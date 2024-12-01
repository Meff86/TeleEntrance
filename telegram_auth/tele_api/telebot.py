import os
import dotenv
import requests
import jwt
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

dotenv.read_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    data = {
        'id': user.id,
        'username': user.username,
    }

    response = requests.post('https://3bba-95-25-251-67.ngrok-free.app/auth/complete/telegram/', data=data)
    if response.status_code == 200:
        token = jwt.encode({'telegram_id': user.id}, 'your-secret-key', algorithm='HS256')

        auth_url = f'https://3bba-95-25-251-67.ngrok-free.app/auth/complete/telegram/?token={token}'

        keyboard = [[InlineKeyboardButton("Continue to website", url=auth_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f'Привет {user.first_name}! Ты авторизован. Пожалуйста, перейди по ссылке:',
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(f'Failed to log in. Please try again.')
def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
