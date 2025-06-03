from .con_db import get_connection


async def check_create_user(user_id: int) -> bool:
    conn = await get_connection()
    result = await conn.execute(
        "INSERT INTO admin_panel_usertg (id) VALUES ($1) ON CONFLICT DO NOTHING",
        user_id
    )
    await conn.close()
    return result == "INSERT 0 1"

async def get_user(user_id: int):
    conn = await get_connection()
    user = await conn.fetchrow("""
        SELECT * FROM admin_panel_usertg WHERE id = $1
    """, user_id)
    await conn.close()
    return user

async def update_user_address(user_id: int, address: str):
    conn = await get_connection()
    await conn.execute("""
        UPDATE admin_panel_usertg SET address = $2 WHERE id = $1
    """, user_id, address)
    await conn.close()

async def update_user_phone(user_id: int, phone: str):
    conn = await get_connection()
    await conn.execute("""
        UPDATE admin_panel_usertg SET phone = $2 WHERE id = $1
    """, user_id, phone)
    await conn.close()