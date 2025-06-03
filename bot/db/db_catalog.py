from .con_db import get_connection


async def get_categories():
    conn = await get_connection()
    categories = await conn.fetch("SELECT id, name FROM admin_panel_category")
    await conn.close()
    return categories

async def get_subcategories(category_id: int):
    conn = await get_connection()
    subcategories = await conn.fetch(
        "SELECT id, name FROM admin_panel_subcategory WHERE category_id = $1", category_id
    )
    await conn.close()
    return subcategories

async def get_products(subcategory_id: int):
    conn = await get_connection()
    products = await conn.fetch(
        "SELECT * FROM admin_panel_product WHERE subcategory_id = $1", subcategory_id
    )
    await conn.close()
    return products
