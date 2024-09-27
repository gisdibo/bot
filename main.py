import firebase_admin
from firebase_admin import credentials, db
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram import Bot
import os

json_path = os.path.abspath("bitcoin-millionaire-64892-firebase-adminsdk-igri1-588ed2081e.json")
cred = credentials.Certificate(json_path)
firebase_admin.initialize_app(cred, {'databaseURL': 'https://bitcoin-millionaire-64892-default-rtdb.firebaseio.com/'})

ref = db.reference('/users')

TOKEN = '7592891158:AAEE0XdZ5djmyfZVxbi2nv7FlQv1lO0RP6s'
bot = Bot(token=TOKEN)

async def refferalFunction(userId, mainUserId):
    user_ref = ref.child(userId)
    user = user_ref.get()

    if str(userId) == str(mainUserId):
        return {"message": "I'm sorry but you can't use your own referral link."}

    if user is None:
        return {"message": "I'm sorry but I can't find the user who invited you to the game."}

    main_user_ref = ref.child(mainUserId)
    main_user = main_user_ref.get()

    if main_user is not None:
        return {"message": "I'm sorry but you're already registered. You can use a referral link before registering in the game."}
    
    chat = await bot.get_chat(userId)
    referrer_username = chat.username

    referral_data = {
        userId: {
            'username': referrer_username,
            'coinsToGive': 0,
            'coins': 0,
        }
    }

    mainUserChat = await bot.get_chat(mainUserId)

    default_user_data = {
        'id': mainUserId,
        'username': mainUserChat.username if mainUserChat.username else "Unknown",
        'coins': 5000,
        'referals': referral_data,
        'tasks': {},
        'upgrades': {},
        'newRankBonus': {},
        'energy': 500,
        "rank": "Rookie",
        'lastPressed': 0,
        "gainedCoins": 0,
        'walletAddress': ''
    }

    if main_user is None:
        main_user_ref.set(default_user_data)

    return {"message": 'You have been invited to play the game by @{}, the referral code has been accepted. You received a start bonus of 5,000 coins.'.format(referrer_username)}

async def start(update: Update, context: CallbackContext) -> None:
    referral_id = context.args[0] if context.args else None
    invite_url = f"https://t.me/testboterino3bot/TheMiner"
    chat = await bot.get_chat(update.message.from_user.id)

    keyboard = [
        [InlineKeyboardButton("Launch The Miner", url=invite_url)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if referral_id:
        checkReferal = await refferalFunction(referral_id, str(chat.id))
        await update.message.reply_text(checkReferal['message'], reply_markup=reply_markup)
        return

    await update.message.reply_text(f'<b>Hey, @{chat.username}! Welcome to The Miner!</b>\nTap on the coin and see your balance rise.\n\nDo you have friends, relatives, or co-workers?\nBring them all into the game. Copy the invite link from the game\'s "Account" menu.', parse_mode="HTML", reply_markup=reply_markup)

def main() -> None:
    print("Bot is on!")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.run_polling()

if __name__ == '__main__':
    main()