from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Your API Key
API_KEY = '7789870114:AAGvLAKdKYlIFxs2dqGTe3i49JRaP8IFFCU'

# Start command handler with inline buttons
async def start(update: Update, context) -> None:
    keyboard = [
        [InlineKeyboardButton("Our Services", callback_data='services')],
        [InlineKeyboardButton("Contact Us", callback_data='contact')],
        [InlineKeyboardButton("About Us", callback_data='about')],
        [InlineKeyboardButton("Give Feedback", callback_data='feedback')],
        [InlineKeyboardButton("Schedule Appointment", callback_data='appointment')],
        [InlineKeyboardButton("Refer a Friend", callback_data='referral')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to DevStudioAL! Choose an option below:", reply_markup=reply_markup)

# Back to main menu function with message auto-deletion
async def back_to_main(query: Update, context) -> None:
    await start(query.message, context)

# Function to auto-delete messages
async def delete_message(context) -> None:
    job = context.job
    await context.bot.delete_message(job.context['chat_id'], job.context['message_id'])

# Set a timer to delete bot messages after 30 seconds
async def set_delete_timer(context, message) -> None:
    context.job_queue.run_once(delete_message, 30, context={'chat_id': message.chat_id, 'message_id': message.message_id})

# Appointment handler
async def appointment(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    msg = await query.edit_message_text("Please provide your preferred date and time for the appointment (e.g., 2023-09-30 14:00):")
    context.user_data['awaiting_appointment'] = True
    await set_delete_timer(context, msg)  # Set deletion timer for this message

# Services handler
async def services(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    msg = await query.edit_message_text("Here are our services:\n1. Web Design\n2. SEO\n3. Responsive Design", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back to Main Menu", callback_data='back')]]))
    await set_delete_timer(context, msg)  # Set deletion timer for this message

# Contact handler
async def contact(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    msg = await query.edit_message_text("Contact us at: info@devstudioal.com", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back to Main Menu", callback_data='back')]]))
    await set_delete_timer(context, msg)  # Set deletion timer for this message

# Callback query handler (for all button clicks)
async def button_handler(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'services':
        await services(update, context)
    elif query.data == 'contact':
        await contact(update, context)
    elif query.data == 'appointment':
        await appointment(update, context)
    elif query.data == 'back':
        await back_to_main(query, context)

def main():
    application = Application.builder().token(API_KEY).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
