from datetime import datetime

from .con_db import get_connection


async def get_product(product_id: int):
    conn = await get_connection()
    product = await conn.fetchrow("""
        SELECT * FROM admin_panel_product WHERE id = $1
    """, product_id)
    await conn.close()
    return product

async def put_product_to_cart(user_id: int, product_id: int, quantity: int):
    conn = await get_connection()
    added_at = datetime.utcnow()

    async with conn.transaction():
        updated = await conn.execute("""
            UPDATE admin_panel_cartitem
            SET quantity = quantity + $3
            WHERE user_id = $1 AND product_id = $2 AND is_payed = FALSE
        """, user_id, product_id, quantity)

        if updated == "UPDATE 0":
            await conn.execute("""
                INSERT INTO admin_panel_cartitem (user_id, product_id, quantity, is_payed, added_at)
                VALUES ($1, $2, $3, FALSE, $4)
            """, user_id, product_id, quantity, added_at)

    await conn.close()

async def get_cart(user_id: int):
    conn = await get_connection()
    items = await conn.fetch("""
        SELECT c.*, p.name, p.price, p.description
        FROM admin_panel_cartitem c
        JOIN admin_panel_product p ON c.product_id = p.id
        WHERE c.user_id = $1 AND c.is_payed = FALSE
    """, user_id)
    await conn.close()
    return items

async def update_item_as_payed(user_id: int):
    conn = await get_connection()
    await conn.execute("""
        UPDATE admin_panel_cartitem SET is_payed = TRUE
        WHERE user_id = $1 AND is_payed = FALSE
    """, user_id)
    await conn.close()

async def put_order_id_to_cart(user_id: int, product_id: int, order_id: int):
    conn = await get_connection()
    await conn.execute("""
        UPDATE admin_panel_cartitem SET order_id = $3
        WHERE user_id = $1 AND product_id = $2 AND is_payed = False
    """, user_id, product_id, order_id)
    await conn.close()

async def delete_product_in_cart(user_id: int, product_id: int):
    conn = await get_connection()
    await conn.execute("""
        DELETE FROM admin_panel_cartitem
        WHERE user_id = $1 AND product_id = $2 AND is_payed = False
    """, user_id, product_id)
    await conn.close()