from typing import Final

from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, filters, CallbackContext

from scraper import Scrapper

TOKEN: Final = '6490849011:AAFmcjual25C8xGMZ0aXBVRnkahVPCi2Lko'
BOT_USERNAME: Final = '@SureBetsTheBot'


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me!')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Help command')


async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scrapper = Scrapper(website_url='https://oddspedia.com/br/apostas-certas')
    betting_info = scrapper.check_website_status()

    message = "Here are the latest betting details:\n\n"

    for info in betting_info:
        message += f"*Location:* {info['location']}\n"
        message += f"*League:* {info['league']}\n"
        message += f"*Date:* {info['date']}\n\n"
        message += f"*{info['team1']['name']} ({info['team1']['house']}):* {info['team1']['odd']}\n"
        message += f"*{info['team2']['name']} ({info['team2']['house']}):* {info['team2']['odd']}\n\n"
        message += f"*Type of Bet:* {info['type_of_bet']}\n"
        message += f"*Potential Profit:* {info['profit']}\n\n"

        # Reply with the Markdown message
        await update.message.reply_markdown(message)
        message = ""


# Handle Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'

    return 'I do not understand what you wrote.'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User {update.message.chat.id} in {message_type}: '{text}'")

    if message_type == 'GROUP':
        print("here")
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print(f"Bot: {response}")
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


async def schedule_job(update: Update, context: CallbackContext) -> None:
    # Get the chat ID
    chat_id = update.message.chat_id

    # Set up the job queue
    job_queue = context.job_queue

    # Schedule the job to run every 3 minutes
    job_queue.run_repeating(job_callback, interval=180, first=0, chat_id=chat_id)

    scrapper = Scrapper(website_url='https://oddspedia.com/br/apostas-certas')
    betting_info = scrapper.check_website_status()

    message = "Here are the latest betting details:\n\n"

    for info in betting_info:
        message += f"*Location:* {info['location']}\n"
        message += f"*League:* {info['league']}\n"
        message += f"*Date:* {info['date']}\n\n"
        message += f"*{info['team1']['name']} ({info['team1']['house']}):* {info['team1']['odd']}\n"
        message += f"*{info['team2']['name']} ({info['team2']['house']}):* {info['team2']['odd']}\n\n"
        message += f"*Type of Bet:* {info['type_of_bet']}\n"
        message += f"*Potential Profit:* {info['profit']}\n\n"

        # Reply with the Markdown message
        await update.message.reply_markdown(message)
        message = ""


async def job_callback(context: CallbackContext):
    chat_id = context.job.chat_id

    scrapper = Scrapper(website_url='https://oddspedia.com/br/apostas-certas')
    message_text = scrapper.check_website_status()

    # Send the message
    await context.bot.send_message(chat_id=chat_id, text=message_text)


if __name__ == '__main__':
    app = Application.builder().token(token=TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('test', test_command))
    app.add_handler(CommandHandler("schedule", schedule_job))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)
    print("Polls the bot...")
    app.run_polling(poll_interval=3)
