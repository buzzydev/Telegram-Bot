from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import add_categorys


# -------------------------------------------------------------------
# 📌 FSM STATES (Kategoriya yaratish holatlari)
# -------------------------------------------------------------------
class CategoryManagementStates(StatesGroup):
    """Kategoriya qo'shish jarayonidagi holatlar."""
    waiting_for_category_title = State()  # Kategoriya nomini kutish holati


# -------------------------------------------------------------------
# 🔀 ROUTER SETUP (Ruter sozlamasi)
# -------------------------------------------------------------------
category_management_router = Router()


# -------------------------------------------------------------------
# 🛠️ HANDLERS (Ishlovchilar)
# -------------------------------------------------------------------

@category_management_router.callback_query(F.data == "category_action_add")
async def start_add_category_process(callback: CallbackQuery, state: FSMContext) -> None:
    """
    📂 'Kategoriya qo'shish' tugmasi bosilganda ishlaydi.
    FSM holatini tozalaydi va yangi kategoriya nomini so'raydi.
    """
    await callback.answer("✨ Kategoriya qo'shish jarayoni boshlandi.")
    await state.clear()

    await callback.message.answer(
        "📝 <b>Yangi kategoriya yaratish</b>\n\n"
        "Iltimos, yaratmoqchi bo'lgan kategoriyangiz nomini kiriting:",
        parse_mode="HTML"
    )
    await state.set_state(CategoryManagementStates.waiting_for_category_title)


@category_management_router.message(CategoryManagementStates.waiting_for_category_title)
async def process_category_title_input(message: Message, state: FSMContext) -> None:
    """
    📥 Kiritilgan kategoriya nomini qabul qiladi, validatsiya qiladi hamda bazaga saqlaydi.
    """
    category_title = message.text.strip()

    # 1️⃣ Kategoriya nomi uzunligini tekshirish (kamida 3 ta belgi)
    if len(category_title) < 3:
        return await message.answer(
            "⚠️ <b>Xatolik!</b> Kategoriya nomi juda qisqa.\n"
            "📏 Kamida <b>3 ta belgi</b>dan iborat bo'lishi kerak. Qaytadan kiriting:",
            parse_mode="HTML"
        )

    # 2️⃣ Kategoriya juda uzun bo'lib ketmasligini tekshirish (masalan, max 50 belgi)
    if len(category_title) > 50:
        return await message.answer(
            "⚠️ <b>Xatolik!</b> Kategoriya nomi juda uzun.\n"
            "📏 Maksimum <b>50 ta belgi</b> kiritishingiz mumkin. Qaytadan kiriting:",
            parse_mode="HTML"
        )

    # 3️⃣ Bazaga saqlash
    add_categorys(category_title)

    # 4️⃣ Muvaffaqiyatli yakunlash xabari
    await message.answer(
        f"🎉 <b>Muvaffaqiyatli!</b>\n\n"
        f"📂 <b>Kategoriya nomi:</b> <code>{category_title}</code>\n\n"
        f"✅ Yangi kategoriya ma'lumotlar bazasiga saqlandi!",
        parse_mode="HTML"
    )

    await state.clear()