import asyncio
import logging

from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

# -------------------------------------------------------------------
# ⚙️ SOZLAMALAR VA BAZA IMPORTLARI
# -------------------------------------------------------------------
from config import bot, ADMIN_ID
from database import create_tables, add_admin

# -------------------------------------------------------------------
# 🔀 ROUTERLAR IMPORTI (BOT BO'LIMLARI)
# -------------------------------------------------------------------
from add_product import p_router
from command import s_router
from add_category import category_management_router
from add_admin import admin_management_router
from add_channel import channel_management_router

# Dispatcher obyektini yaratish
dp = Dispatcher()


# ====================================================================
# 1. 📜 BOT BUYRUQLARI (MENU COMMANDS)
# ====================================================================

async def menu_commands():
    """
    📜 Botning pastki chap burchagida ko'rinadigan asosiy buyruqlar menyusini o'rnatadi.
    """
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish"),
        BotCommand(command="admin", description="Admin Menyu"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


# ====================================================================
# 2. 🚀 MAIN FUNKSIYASI (BOTNI ISHGA TUSHIRISH)
# ====================================================================

async def main():
    """
    🚀 Botni ishga tushiruvchi asosiy funksiya:
    1. Menyuni o'rnatadi.
    2. Baza jadvallarini yaratadi.
    3. Barcha routerlarni dispatcherga ulaydi.
    4. Polling jarayonini boshlaydi.
    """
    # Menyuni sozlash
    await menu_commands()
    
    # Bazada jadvallar mavjud bo'lmasa, ularni yaratish
    create_tables()
    add_admin(ADMIN_ID)
      # Asosiy adminni birinchi marta tayinlash

    # 🔀 Routerlarni Dispatcherga ulash
    dp.include_router(p_router)
    dp.include_router(s_router)
    dp.include_router(channel_management_router)
    dp.include_router(category_management_router)
    dp.include_router(admin_management_router)

    # Ishga tushganlik haqida konsolga xabar chiqarish
    print("Bot muvaffaqiyatli ishga tushdi...")
    
    # Pollingni boshlash (yangi xabarlarni uzluksiz eshitib turish)
    await dp.start_polling(bot)


# ====================================================================
# 3. 🏁 DASTURNI ISHGA TUSHIRISH NUKTASI
# ====================================================================

if __name__ == "__main__":
    # Loglarni konsolda ko'rsatish sozlamasi
    logging.basicConfig(level=logging.INFO)
    
    # Asinxron main funksiyasini ishga tushirish
    asyncio.run(main())