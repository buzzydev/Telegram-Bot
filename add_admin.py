from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import add_admin, check_user, check_admin


# -------------------------------------------------------------------
# 📌 FSM STATES (Xabar almashish holatlari)
# -------------------------------------------------------------------
class AdminManagementStates(StatesGroup):
    """Yangi admin qo'shish jarayonidagi holatlar."""
    waiting_for_admin_id = State()  # Telegram ID kiritilishini kutish holati


# -------------------------------------------------------------------
# 🔀 ROUTER SETUP (Ruter sozlamasi)
# -------------------------------------------------------------------
admin_management_router = Router()


# -------------------------------------------------------------------
# 🛠️ HANDLERS (Ishlovchilar)
# -------------------------------------------------------------------

@admin_management_router.callback_query(F.data == "admin_action_add")
async def start_add_admin_process(callback: CallbackQuery, state: FSMContext) -> None:
    """
    ➕ 'Yangi admin qo'shish' tugmasi bosilganda ishlaydi.
    FSM holatini tozalaydi va foydalanuvchidan Telegram ID so'raydi.
    """
    await callback.answer("✨ Admin qo'shish jarayoni boshlandi.")
    await state.clear()

    await callback.message.answer(
        "📝 <b>Yangi admin tayinlash</b>\n\n"
        "Iltimos, yangi admin qilmoqchi bo'lgan foydalanuvchining <b>Telegram ID</b> sini kiriting:",
        parse_mode="HTML"
    )
    await state.set_state(AdminManagementStates.waiting_for_admin_id)


@admin_management_router.message(AdminManagementStates.waiting_for_admin_id)
async def process_admin_id_input(message: Message, state: FSMContext) -> None:
    """
    📥 Kiritilgan Telegram ID ni qabul qiladi va ma'lumotlar bazasi bilan tekshiradi.
    """
    input_text = message.text.strip()

    # 1️⃣ ID raqamlardan iboratligini tekshirish
    if not input_text.isdigit():
        return await message.answer(
            "⚠️ <b>Xatolik!</b> ID faqat raqamlardan iborat bo'lishi kerak.\n"
            "🔄 Qaytadan kiriting:", parse_mode="HTML"
        )

    target_admin_id = int(input_text)

    # 2️⃣ Foydalanuvchi bazada mavjudligini tekshirish
    user_record = check_user(target_admin_id)
    if user_record is None:
        return await message.answer(
            "🔍 <b>Foydalanuvchi topilmadi!</b>\n\n"
            "Ushbu foydalanuvchi hali botdan <code>/start</code> buyrug'i orqali ro'yxatdan o'tmagan.", parse_mode="HTML"
        )

    # 3️⃣ Foydalanuvchi allaqachon admin ekanligini tekshirish
    if check_admin(target_admin_id):
        await state.clear()
        return await message.answer(
            "👑 <b>Ma'lumot:</b> Ushbu foydalanuvchi allaqachon admin huquqlariga ega."
        )

    # 4️⃣ Bazaga yangi adminni qo'shish
    add_admin(target_admin_id)
    await message.answer(
        f"🎉 <b>Muvaffaqiyatli!</b>\n\n"
        f"🆔 <b>ID:</b> <code>{target_admin_id}</code>\n\n"
        f"🚀 Foydalanuvchiga admin huquqlari berildi!",
        parse_mode="HTML"
    )
    
    await state.clear() 