from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# -------------------------------------------------------------------
# ⚙️ TUGMALAR VA BAZA FUNKSIYALARI IMPORTI
# -------------------------------------------------------------------
from buttons import admin_menu_keyboard
from database import get_all_users_id


# ====================================================================
# 1. 📝 FSM HOLATINI ANIQLASH (SEND MESSAGE STATE)
# ====================================================================

class SendMessageState(StatesGroup):
    """
    📢 Ommaviy xabar yuborish (Rassilka) jarayoni uchun FSM holati:
    - message: Admin yubormoqchi bo'lgan xabarni qabul qilish holati.
    """
    message = State()


# 🔀 Ommaviy xabarlar uchun alohida router
send_message_router = Router()


# ====================================================================
# 2. 🟢 OMMAVIY XABAR YUBORISHNI BOSHLASH (CALLBACK)
# ====================================================================

@send_message_router.callback_query(F.data == "admin:send_message")
async def register_cmd(callback: CallbackQuery, state: FSMContext):
    """
    🟢 Admin 'admin:send_message' tugmasini bosganda ishga tushadi:
    1. Avvalgi FSM xotirasini tozalaydi.
    2. Admindan tarqatiladigan xabarni (matn, rasm, video va h.k.) so'raydi.
    3. FSM holatini SendMessageState.message ga o'tkazadi.
    """
    await state.clear()

    await callback.message.answer("📢 Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni kiriting:")
    await state.set_state(SendMessageState.message)
    await callback.answer()


# ====================================================================
# 3. 📤 XABARNI QABUL QILISH VA BARCHAGA TARQATISH (RASSILKA)
# ====================================================================

@send_message_router.message(SendMessageState.message)
async def get_message(message: Message, state: FSMContext):
    """
    📤 Admin yuborgan xabarni qabul qiladi va barcha foydalanuvchilarga tarqatadi:
    - Bazadan barcha user Telegram ID larini oladi.
    - Sikl orqali `message.copy_to` yordamida xabarni aslicha (mediasi bilan) nusxalaydi.
    - Botni bloklagan yoki nofaol foydalanuvchilarni xatolik (Exception) orqali o'tkazib yuboradi.
    - Muvaffaqiyatli yetib borgan xabarlar sonini hisoblab, adminga hisobot beradi.
    """
    users_id = get_all_users_id()
    sent_count = 0

    # Barcha foydalanuvchilarga xabarni (matn, rasm, video va h.k.) nusxalab yuborish
    for user in users_id:
        try:
            await message.copy_to(chat_id=user[0])
            sent_count += 1
        except Exception:
            # Botni bloklagan yoki nofaol foydalanuvchilarni o'tkazib yuborish
            pass

    # FSM holatini tozalash
    await state.clear()

    # Admin menyusiga qaytarish va natijani ko'rsatish
    await message.answer(
        f"✅ Xabar {sent_count} ta foydalanuvchiga muvaffaqiyatli yuborildi!",
        reply_markup=admin_menu_keyboard
    )