import logging
from aiohttp import web
from config import bot

logger = logging.getLogger(__name__)

app = web.Application()

routes = web.RouteTableDef()

@routes.post('/send_message/')
async def send_message(request):
    try:
        data = await request.json()
        user_id = data.get("user_id")
        text = data.get("text")

        if not user_id or not text:
            logger.warning(f"Bad request: {data}")
            return web.json_response({"error": "Missing user_id or text"}, status=400)

        await bot.send_message(chat_id=user_id, text=text)
        logger.info(f"Message sent to user_id={user_id}")
        return web.json_response({"status": "ok"})
    except Exception as e:
        logger.error(f"Failed to send message: {e}", exc_info=True)
        return web.json_response({"error": str(e)}, status=500)

app.add_routes(routes)
