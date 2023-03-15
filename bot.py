import os
import telegram
import instaloader

# Initialize Telegram Bot API
bot = telegram.Bot(token='5576076382:AAE4zSa_WnN4NX7NiBerdRaOTHuBuXaAEQQ')

# Initialize Instaloader
L = instaloader.Instaloader()

# Define function to handle incoming messages
def download_post(update, context):
    # Get the message sent by user
    message = update.message.text

    # Extract Instagram post URL from message
    url = message.split()[-1]

    try:
        # Download the Instagram post
        L.download_post(url, target=os.getcwd())

        # Send the downloaded post as a file to user
        chat_id = update.message.chat_id
        file_name = url.split('/')[-2] + '.jpg'
        with open(file_name, 'rb') as f:
            bot.send_photo(chat_id=chat_id, photo=f)

        # Delete the downloaded file
        os.remove(file_name)
    except Exception as e:
        # If error occurs, send the error message to user
        bot.send_message(chat_id=chat_id, text=str(e))

# Add handler for incoming messages
updater = telegram.ext.Updater(token='5576076382:AAE4zSa_WnN4NX7NiBerdRaOTHuBuXaAEQQ', use_context=True)
updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text & telegram.ext.Filters.entity(telegram.ext.MessageEntity.URL), download_post))

# Start the bot
updater.start_polling()
updater.idle()
