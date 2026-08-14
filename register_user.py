from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# -------------------------------------------------------------------
# ⚙️ TUGMALAR VA BAZA FUNKSIYALARI IMPORTI
# -------------------------------------------------------------------
from buttons import phone_request_keyboard, user_start_keyboard
from database import add_users, check_user


# ====================================================================
# 1. 📝 FSM HOLATLARINI ANIQLASH (REGISTER STATES)
# ====================================================================

class RegisterState(StatesGroup):
    """
    📝 Ro'yxatdan o'tish jarayoni uchun ketma-ket holatlar (FSM):
    - ism: Foydalanuvchi ismini qabul qilish
    - manzil: Foydalanuvchi manzilini qabul qilish
    - telefon: Foydalanuvchi telefon raqamini qabul qilish
    """
    ism = State()
    manzil = State()
    telefon = State()


# 🔀 Ro'yxatdan o'tish uchun alohida router
r_router = Router()


# # ====================================================================
# # 2. 🟢 RO'YXATDAN O'TISHNI BOSHLASH (CALLBACK)
# # ====================================================================

# @r_router.callback_query(F.data == "register_user")
# async def register_cmd(callback: CallbackQuery, state: FSMContext):
#     """
#     🟢 'register_user' tugmasi bosilganda ishga tushadi:
#     1. Foydalanuvchi oldin ro'yxatdan o'tganligini tekshiradi.
#     2. Agar o'tmagan bo'lsa, ism so'rash holatiga o'tkazadi.
#     """
#     user_id = callback.from_user.id
#     user = check_user(user_id)

#     # Foydalanuvchi allaqachon mavjud bo'lsa
#     if user is not None:
#         await callback.answer("Siz allaqachon ro'yxatdan o'tgansiz!", show_alert=True)
#         return

#     # Eski FSM ma'lumotlarini tozalash
#     await state.clear()

#     # Ism so'rash va holatni o'zgartirish
#     await callback.message.answer("Ismingizni kiriting:")
#     await state.set_state(RegisterState.ism)
#     await callback.answer()


# # ====================================================================
# # 3. 👤 ISMNI QABUL QILISH VA TEKSHIRISH
# # ====================================================================

# @r_router.message(RegisterState.ism)
# async def get_ism(message: Message, state: FSMContext):
#     """
#     👤 Foydalanuvchi kiritgan ismni qabul qiladi va validatsiya qiladi:
#     - Belgilar soni kamida 3 ta bo'lishi kerak.
#     - Faqat harflardan iborat bo'lishi kerak.
#     """
#     text = message.text

#     # Uzunlikni tekshirish
#     if not text or len(text) < 3:
#         return await message.answer("Ismni to'liqroq kiriting.")

#     # Bo'shliqlarni olib tashlab harflardan iboratligini tekshirish
#     if not text.replace(" ", "").isalpha():
#         return await message.answer("Ismda faqat harflar qatnashishi kerak.")

#     # Ma'lumotni FSM ga saqlash
#     await state.update_data(ism=text)

#     # Keyingi holatga o'tish (manzil so'rash)
#     await message.answer("Manzilni kiriting:")
#     await state.set_state(RegisterState.manzil)


# # ====================================================================
# # 4. 📍 MANZILNI QABUL QILISH
# # ====================================================================

# @r_router.message(RegisterState.manzil)
# async def get_manzil(message: Message, state: FSMContext):
#     """
#     📍 Foydalanuvchi kiritgan manzilni qabul qiladi:
#     - Uzunlik kamida 3 ta belgi bo'lishini tekshiradi.
#     - Telefon raqam so'rash bosqichiga o'tkazadi.
#     """
#     text = message.text

#     if not text or len(text) < 3:
#         return await message.answer("Manzilni to'liqroq kiriting.")

#     # Manzilni FSM xotirasiga saqlash
#     await state.update_data(manzil=text)

#     # Telefon raqam yuborish tugmasi bilan birga xabar yuborish
#     await message.answer(
#         "Telefon raqamingizni kiriting (yoki tugmani bosing):",
#         reply_markup=phone_request_keyboard
#     )

#     await state.set_state(RegisterState.telefon)


# # ====================================================================
# # 5. 📞 TELEFON RAQAMNI QABUL QILISH VA BAZAGA SAQLASH
# # ====================================================================

# @r_router.message(RegisterState.telefon)
# async def get_telefon(message: Message, state: FSMContext):
#     """
#     📞 Telefon raqamini (kontakt yoki matn ko'rinishida) qabul qiladi:
#     - Kontakt yuborilgan bo'lsa: prefiksni tekshiradi va formatlaydi.
#     - Matn yuborilgan bo'lsa: '+998' bilan boshlanishini tekshiradi.
#     - Barcha ma'lumotlarni yig'ib bazaga (add_users) saqlaydi va ro'yxatdan o'tishni yakunlaydi.
#     """
#     # 1. Kontakt orqali yuborilgan bo'lsa
#     if message.contact:
#         telefon = message.contact.phone_number
#         if not telefon.startswith("+"):
#             telefon = "+" + telefon

#     # 2. Matn ko'rinishida yozilgan bo'lsa
#     elif message.text:
#         telefon = message.text

#         if not telefon.startswith("+998"):
#             return await message.answer(
#                 "Telefon raqam +998 bilan boshlanishi kerak.",
#                 reply_markup=phone_request_keyboard
#             )
#     else:
#         return await message.answer(
#             "Telefon raqam kiriting.", 
#             reply_markup=phone_request_keyboard
#         )

#     await state.update_data(telefon=telefon)

#     # 💾 Yig'ilgan barcha ma me'lumotlarni olish
#     data = await state.get_data()

#     ism = data.get("ism")
#     address = data.get("manzil")
#     telefon = data.get("telefon")
#     user_id = message.from_user.id
#     username = message.from_user.username or "mavjud_emas"

#     # Foydalanuvchini bazaga qo'shish
#     add_users(
#         ism,
#         address,
#         telefon,
#         username,
#         user_id
#     )

#     # FSM holatini tozalash
#     await state.clear()

#     # 🏁 Ro'yxatdan o'tish yakunlangani haqida xabar va asosiy menyuni chiqarish
#     await message.answer(
#         "✅ Ro'yxatdan muvaffaqiyatli o'tdingiz!",
#         reply_markup=ReplyKeyboardRemove()
#     )
#     await message.answer(
#         "📂 Asosiy menyu:",
#         reply_markup=user_start_keyboard
#     )