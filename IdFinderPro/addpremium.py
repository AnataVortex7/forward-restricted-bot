from pyrogram import Client, filters
from database.db import db  # Your Database instance
from datetime import datetime, timedelta
from config import ADMINS

@Client.on_message(filters.command("addpremium") & filters.user(ADMINS))
async def add_premium(client, message):
    args = message.text.split()
    if len(args) < 3:
        await message.reply("Usage: /addpremium <user_id> <days>")
        return

    user_id = int(args[1])
    days = int(args[2])
    
    user = await db.col.find_one({"id": user_id})
    if not user:
        # Create new user
        user_data = db.new_user(user_id, "Unknown")
        user_data['is_premium'] = True
        user_data['premium_expiry'] = datetime.utcnow() + timedelta(days=days)
        await db.col.insert_one(user_data)
        await message.reply(f"New user {user_id} added with premium for {days} days.")
    else:
        # Update existing user
        new_expiry = datetime.utcnow() + timedelta(days=days)
        await db.col.update_one(
            {"id": user_id},
            {"$set": {"is_premium": True, "premium_expiry": new_expiry}}
        )
        await message.reply(f"User {user_id} updated with premium for {days} days.")
