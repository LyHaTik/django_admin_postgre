from aiogram import Dispatcher
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from rapidfuzz import process

import uuid

from config import FAQ_DATA, THRESHOLD


## Хэндлеры FAQ
async def inline_faq(query: InlineQuery):
    user_query = query.query.strip()
    results = []

    if user_query:
        matches = process.extract(
            user_query,
            [faq["question"] for faq in FAQ_DATA],
            limit=10,
            score_cutoff=THRESHOLD,
        )

        for match in matches:
            question_text = match[0]
            faq_item = next(f for f in FAQ_DATA if f["question"] == question_text)
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=faq_item["question"],
                    input_message_content=InputTextMessageContent(
                        message_text=f"❓ {faq_item['question']}\n\n💬 {faq_item['answer']}"
                    ),
                    description=faq_item["answer"],
                )
            )
    else:
        for faq in FAQ_DATA:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=faq["question"],
                    input_message_content=InputTextMessageContent(
                        message_text=f"❓ {faq['question']}\n\n💬 {faq['answer']}"
                    ),
                    description=faq["answer"],
                )
            )

    await query.answer(results[:10], cache_time=1)


def register_faq(dp: Dispatcher):
    dp.inline_query.register(inline_faq)

