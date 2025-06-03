from .con_db import get_connection


async def mailing_text():
    conn = await get_connection()
    msg = await conn.fetchrow("""
        SELECT * FROM admin_panel_broadcastmessage WHERE sent = FALSE
        ORDER BY created_at ASC LIMIT 1
    """)
    if msg:
        await conn.execute("""
            UPDATE admin_panel_broadcastmessage SET sent = TRUE WHERE id = $1
        """, msg["id"])
    await conn.close()
    return msg["text"] if msg else None
