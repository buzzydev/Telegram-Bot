import sqlite3

# ====================================================================
# 1. 🛠️ JADVALLARNI YARATISH (DATABASE INITIALIZATION)
# ====================================================================

def create_tables():
    """
    🗄️ Baza va unga tegishli barcha jadvallarni
    (users, categories, products, cart) yaratadi.
    """
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    # 👤 Foydalanuvchilar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        username TEXT,
        telegram_id INTEGER,
        is_admin BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subs_channels(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_name TEXT,
        channel_id TEXT,
        channel_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 📂 Kategoriyalar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 📦 Mahsulotlar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        category_id INTEGER,
        price INTEGER,
        quantity INTEGER,
        image TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 🛒 Savatcha (Cart) jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        price INTEGER,
        quantity INTEGER,
        status BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    connect.commit()
    connect.close()


# ====================================================================
# 2. 🛒 SAVATCHA (CART) BILAN ISHLASH FUNKSIYALARI
# ====================================================================
# -------------------------------------------------------------------
# 🔍 SAVATCHANI TEKSHIRISH VA MA'LUMOT OLISH
# -------------------------------------------------------------------

def check_cart(product_id):
    """🔍 Mahsulot savatda bor-yo'qligini tekshiradi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT * FROM cart
        WHERE product_id = ?
    """, (product_id,))

    data = cursor.fetchone()
    connect.close()
    return data


def get_cart_item_quantity_by_product_id(product_id):
    """🔢 Savatdagi mahsulot miqdorini oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT quantity FROM cart
        WHERE product_id = ?
    """, (product_id,))

    data = cursor.fetchone()
    connect.close()
    return data


def get_cart_item_price_by_product_id(product_id):
    """💰 Savatdagi mahsulot narxini oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT price FROM cart
        WHERE product_id = ?
    """, (product_id,))

    data = cursor.fetchone()
    connect.close()
    return data


def get_one_cart_item_by_id(cart_id):
    """🆔 ID bo'yicha savatdagi bitta elementni oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT * FROM cart
        WHERE id = ?
    """, (cart_id,))

    data = cursor.fetchone()
    connect.close()
    return data


def get_all_cart_items_by_id(user_id):
    """📋 Foydalanuvchining aktiv savat elementlarini oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT * FROM cart
        WHERE user_id = ?
        AND status = 1
    """, (user_id,))

    data = cursor.fetchall()
    connect.close()
    return data

def add_channel(channel_name, channel_id, channel_url):
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()
    
    cursor.execute("""
        INSERT INTO subs_channels (
            channel_name,
            channel_id,
            channel_url
        )
        VALUES (?, ?, ?)
    """, (channel_name, channel_id, channel_url))

    connect.commit()

# -------------------------------------------------------------------
# ➕ SAVATGA QO'SHISH VA O'CHIRISH
# -------------------------------------------------------------------

def add_cart_item(user_id, product_id, price, quantity):
    """➕ Savatga yangi mahsulot qo'shadi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        INSERT INTO cart (user_id, product_id, price, quantity)
        VALUES (?, ?, ?, ?)
    """, (user_id, product_id, price, quantity))

    connect.commit()
    connect.close()


def clear_user_cart(user_id):
    """🗑️ Foydalanuvchining butun savatini tozalaydi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        DELETE FROM cart
        WHERE user_id = ?
    """, (user_id,))

    connect.commit()
    connect.close()


def delete_cart_item_by(cart_id):
    """❌ Savatdan ID bo'yicha elementni o'chiradi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        DELETE FROM cart
        WHERE id = ?
    """, (cart_id,))

    connect.commit()
    connect.close()

def delete_cart_item_by_id(cart_id):
    """❌ Savatdan ID bo'yicha elementni o'chiradi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        DELETE FROM cart
        WHERE product_id = ?
    """, (cart_id,))

    connect.commit()
    connect.close()


def clear_cart_by_user_id(user_id):
    """🗑️ Foydalanuvchi ID si bo'yicha savatni tozalaydi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        DELETE FROM cart
        WHERE user_id = ?
    """, (user_id,))

    connect.commit()
    connect.close()


# -------------------------------------------------------------------
# ✏️ SAVATDAKI MA'LUMOTLARNI YANGILASH (UPDATE)
# -------------------------------------------------------------------

def update_cart_price_by_id(cart_id, new_price):
    """💰 Savat elementining narxini ID bo'yicha yangilaydi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        UPDATE cart
        SET price = ?
        WHERE id = ?
    """, (new_price, cart_id))

    connect.commit()
    connect.close()


def update_cart_price_by_product_id(product_id, new_price):
    """💰 Savat elementining narxini Product ID bo'yicha yangilaydi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        UPDATE cart
        SET price = ?
        WHERE product_id = ?
    """, (new_price, product_id))

    connect.commit()
    connect.close()


def update_cart_quantity_by_id(cart_id, new_quantity):
    """🔢 Savat elementining miqdorini ID bo'yicha yangilaydi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        UPDATE cart
        SET quantity = ?
        WHERE id = ?
    """, (new_quantity, cart_id))

    connect.commit()
    connect.close()


def update_cart_quantity_by_product_id(product_id, new_quantity):
    """🔢 Savat elementining miqdorini Product ID bo'yicha yangilaydi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        UPDATE cart
        SET quantity = ?
        WHERE product_id = ?
    """, (new_quantity, product_id))

    connect.commit()
    connect.close()


def update_cart_status_by_id(cart_id, new_status):
    """🔄 Savat buyurtma holatini (status) yangilaydi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        UPDATE cart
        SET status = ?
        WHERE id = ?
    """, (new_status, cart_id))

    connect.commit()
    connect.close()


def update_product_quantity_by_id(new_quantity, product_id):
    """📦 Mahsulot qoldig'ini yangilaydi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        UPDATE products
        SET quantity = ?
        WHERE id = ?
    """, (new_quantity, product_id))

    connect.commit()
    connect.close()


# ====================================================================
# 3. 👤 FOYDALANUVCHILAR VA ADMINLAR BILAN ISHLASH
# ====================================================================

def add_users(name, username, telegram_id):
    """👤 Yangi foydalanuvchini bazaga qo'shadi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        INSERT INTO users (name, username, telegram_id)
        VALUES (?, ?, ?)
    """, (name, username, telegram_id))

    connect.commit()
    connect.close()

def update_cart_quantity_by_user_id(user_id):
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        UPDATE cart
        SET status = 0 WHERE user_id = ?
    """, (user_id,))

    connect.commit()
    connect.close()
    

def check_user(telegram_id):
    """🔍 Foydalanuvchini Telegram ID bo'yicha tekshiradi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE telegram_id = ?
    """, (telegram_id,))

    user = cursor.fetchone()
    connect.close()
    return user


def add_admin(telegram_id):
    """🔑 Foydalanuvchiga admin huquqini beradi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        UPDATE users
        SET is_admin = 1
        WHERE telegram_id = ?
    """, (telegram_id,))

    connect.commit()
    connect.close()


# Asosiy adminni birinchi marta tayinlash
# add_admin(8968685902)


def check_admin(telegram_id):
    """⚙️ Foydalanuvchi admin yoki yo'qligini tekshiradi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE is_admin = 1
        AND telegram_id = ?
    """, (telegram_id,))

    admin = cursor.fetchone()
    connect.close()
    return admin

def delete_admin(telegram_id):
    """❌ Foydalanuvchining adminlik huquqini olib tashlaydi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        UPDATE users
        SET is_admin = 0
        WHERE telegram_id = ?
    """, (telegram_id,))

    connect.commit()
    connect.close()


def get_users_count():
    """📊 Jami foydalanuvchilar sonini oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM users
    """)

    count = cursor.fetchone()
    connect.close()
    return count


def get_all_users_id():
    """🆔 Barcha foydalanuvchilarning Telegram ID larini oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT telegram_id FROM users
    """)

    data = cursor.fetchall()
    connect.close()
    return data


def get_all_admins():
    """👑 Barcha adminlar ro'yxatini oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE is_admin = 1
    """)

    data = cursor.fetchall()
    connect.close()
    return data


def get_one_admin(admin_id):
    """👤 Bitta admin ma'lumotlarini ID bo'yicha oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE id = ?
    """, (admin_id,))

    data = cursor.fetchone()
    connect.close()
    return data


# ====================================================================
# 4. 📂 KATEGORIYALAR BILAN ISHLASH
# ====================================================================

def add_categorys(title):
    """➕ Yangi kategoriya qo'shadi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        INSERT INTO categories(title)
        VALUES (?)
    """, (title,))

    connect.commit()
    connect.close()


def deletes_category(category_id):
    """🗑️ Kategoriyani ID bo'yicha o'chiradi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        DELETE FROM categories
        WHERE id = ?
    """, (category_id,))

    connect.commit()
    connect.close()


def get_all_categories():
    """📋 Barcha kategoriyalar ro'yxatini oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT * FROM categories
    """)

    data = cursor.fetchall()
    connect.close()
    return data


def get_one_category(ctg_id):
    """📂 Bitta kategoriya ma'lumotlarini ID bo'yicha oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT * FROM categories
        WHERE id = ?
    """, (ctg_id,))

    data = cursor.fetchone()
    connect.close()
    return data


# ====================================================================
# 5. 📦 MAHSULOTLAR (PRODUCTS) BILAN ISHLASH
# ====================================================================

def add_products(name, description, category_id, price, quantity, image):
    """📦 Yangi mahsulot qo'shadi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        INSERT INTO products(
            name,
            description,
            category_id,
            price,
            quantity,
            image
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        description,
        category_id,
        price,
        quantity,
        image,
    ))

    connect.commit()
    connect.close()


def delete_products(product_id):
    """🗑️ Mahsulotni ID bo'yicha o'chiradi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        DELETE FROM products
        WHERE id = ?
    """, (product_id,))

    connect.commit()
    connect.close()


def get_product_by_category(category_id):
    """📂 Kategoriya ID si bo'yicha tegishli mahsulotlarni oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT * FROM products
        WHERE category_id = ?
    """, (category_id,))

    data = cursor.fetchall()
    connect.close()
    return data


def get_products_by_ctg_id(category_id):
    """📂 Kategoriya ID si bo'yicha mahsulotlarni oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT * FROM products
        WHERE category_id = ?
    """, (category_id,))

    data = cursor.fetchall()
    connect.close()
    return data


def get_all_products():
    """🗂️ Barcha mahsulotlar ro'yxatini oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT * FROM products
    """)

    data = cursor.fetchall()
    connect.close()
    return data

def get_one_channel(channel_id):
    """🥤 Bitta mahsulot ma'lumotlarini ID bo'yicha oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT * FROM subs_channels
        WHERE id = ?
    """, (channel_id,))

    data = cursor.fetchone()
    connect.close()
    return data

def get_one_channel_by_telegram_id(channel_id):
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()
    cursor.execute("""
        SELECT id, channel_name, channel_id, channel_url, created_at
        FROM subs_channels
        WHERE channel_id = ?
    """, (channel_id,))

    return cursor.fetchone()

def delete_channel(channel_id):
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()
    cursor.execute("""
        DELETE FROM subs_channels
        WHERE id = ?
    """, (channel_id,))

    connect.commit()
def get_all_channels():
    """🗂️ Barcha mahsulotlar ro'yxatini oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT * FROM subs_channels
    """)

    data = cursor.fetchall()
    connect.close()
    return data

def get_one_product(product_id):
    """🥤 Bitta mahsulot ma'lumotlarini ID bo'yicha oladi."""
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    cursor.execute("""
        SELECT * FROM products
        WHERE id = ?
    """, (product_id,))

    data = cursor.fetchone()
    connect.close()
    return data