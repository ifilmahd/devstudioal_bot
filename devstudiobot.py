from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Your API Key
API_KEY = '7789870114:AAGvLAKdKYlIFxs2dqGTe3i49JRaP8IFFCU'

# Start command handler with inline buttons
async def start(update: Update, context) -> None:
    # Handle both messages and callback queries
    message = update.message if update.message else update.callback_query.message
    keyboard = [
        [InlineKeyboardButton("Our Services", callback_data='services')],
        [InlineKeyboardButton("Contact Us", callback_data='contact')],
        [InlineKeyboardButton("About Us", callback_data='about')],
        [InlineKeyboardButton("Give Feedback", callback_data='feedback')],
        [InlineKeyboardButton("Schedule Appointment", callback_data='appointment')],
        [InlineKeyboardButton("Refer a Friend", callback_data='referral')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # If there's an old message, edit it instead of sending a new one
    if context.user_data.get('last_message_id'):
        await context.bot.edit_message_text(
            chat_id=message.chat_id,
            message_id=context.user_data['last_message_id'],
            text="Welcome to DevStudioAL! Choose an option below:",
            reply_markup=reply_markup
        )
    else:
        sent_message = await message.reply_text(
            "Welcome to DevStudioAL! Choose an option below:",
            reply_markup=reply_markup
        )
        context.user_data['last_message_id'] = sent_message.message_id

# Services handler
async def services(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    services_message = (
        "Here are our services:\n"
        "1. Web Design & Development\n"
        "2. E-commerce Solutions\n"
        "3. Responsive Design\n"
        "4. SEO Optimization\n"
        "5. Custom Web Applications\n\n"
        "Visit: https://devstudioal.com for more details!"
    )
    keyboard = [[InlineKeyboardButton("Back to Main Menu", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Edit the previous message with the services information
    await context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=context.user_data['last_message_id'],
        text=services_message,
        reply_markup=reply_markup
    )

# Contact handler
async def contact(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    contact_message = (
        "You can reach us at:\n"
        "📧 Email: info@devstudioal.com\n"
        f"📞 <a href='https://wa.me/447537168000'>WhatsApp</a>\n"
        "🌐 Website: https://devstudioal.com"
    )
    keyboard = [[InlineKeyboardButton("Back to Main Menu", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Edit the previous message with the contact information
    await context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=context.user_data['last_message_id'],
        text=contact_message,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

# About handler
async def about(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    about_message = (
        "DevStudioAL is a professional web design and development studio.\n"
        "We specialize in modern, responsive websites tailored to your business needs.\n"
        "Let us help you build a strong online presence!"
    )
    keyboard = [[InlineKeyboardButton("Back to Main Menu", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Edit the previous message with the about information
    await context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=context.user_data['last_message_id'],
        text=about_message,
        reply_markup=reply_markup
    )

# Feedback handler
async def feedback(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Please type your feedback:")
    context.user_data['awaiting_feedback'] = True

# Back to main menu
async def back_to_main(update: Update, context) -> None:
    await start(update, context)

# Button handler
async def button_handler(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'services':
        await services(update, context)
    elif query.data == 'contact':
        await contact(update, context)
    elif query.data == 'about':
        await about(update, context)
    elif query.data == 'feedback':
        await feedback(update, context)
    elif query.data == 'appointment':
        # You can add appointment handling here later
        pass
    elif query.data == 'referral':
        # You can add referral handling here later
        pass
    elif query.data == 'back':
        await back_to_main(update, context)

def main():
    application = Application.builder().token(API_KEY).build()

    # Command to start the bot
    application.add_handler(CommandHandler("start", start))
    # Button handler
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
