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
    await message.reply_text("Welcome to DevStudioAL! Choose an option below:", reply_markup=reply_markup)

# Welcome message handler
async def welcome(update: Update, context) -> None:
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"Welcome {member.full_name}! Feel free to explore our services. Use /start to get started!")

# Back to main menu function
async def back_to_main(query: Update, context) -> None:
    await start(query, context)

# Appointment handler
async def appointment(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Please provide your preferred date and time for the appointment (e.g., 2023-09-30 14:00):")
    context.user_data['awaiting_appointment'] = True

# Storing appointment
async def handle_appointment(update: Update, context) -> None:
    if context.user_data.get('awaiting_appointment'):
        appointment_time = update.message.text
        print(f"Appointment requested by {update.message.from_user.first_name} for {appointment_time}.")
        await update.message.reply_text("Thank you! Your appointment has been scheduled.")
        context.user_data['awaiting_appointment'] = False

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
    await query.edit_message_text(text=services_message, reply_markup=reply_markup)

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
    await query.edit_message_text(text=contact_message, reply_markup=reply_markup, parse_mode='HTML')

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
    await query.edit_message_text(text=about_message, reply_markup=reply_markup)

# Feedback handler
async def feedback(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Please type your feedback:")
    context.user_data['awaiting_feedback'] = True

# Storing feedback
async def handle_message(update: Update, context) -> None:
    if context.user_data.get('awaiting_feedback'):
        feedback_text = update.message.text
        print(f"Feedback from {update.message.from_user.first_name}: {feedback_text}")
        await update.message.reply_text("Thank you for your feedback!")
        context.user_data['awaiting_feedback'] = False

# Referral system
async def referral(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Please provide your friend's Telegram username to refer them:")

# Handle the referral input
async def handle_referral(update: Update, context) -> None:
    if 'referring' in context.user_data:
        friend_username = update.message.text
        print(f"User {update.message.from_user.first_name} referred {friend_username}.")
        await update.message.reply_text(f"Thank you for referring {friend_username}! You've earned a reward.")
        context.user_data['referring'] = False

# Trigger commands with keywords
async def keyword_handler(update: Update, context) -> None:
    user_message = update.message.text.lower()
    
    if "services" in user_message:
        await services(update, context)
    elif "contact" in user_message:
        await contact(update, context)
    elif "about" in user_message:
        await about(update, context)

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
        await appointment(update, context)
    elif query.data == 'referral':
        await referral(update, context)
    elif query.data == 'back':
        await back_to_main(query, context)

def main():
    application = Application.builder().token(API_KEY).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, keyword_handler))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_appointment))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_referral))

    application.run_polling()

if __name__ == '__main__':
    main()
