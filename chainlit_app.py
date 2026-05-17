# chainlit_app.py

import chainlit as cl
import httpx
import uuid

API_BASE = "http://localhost:8000/api/v1"


# -----------------------------
# On Chat Start
# -----------------------------
@cl.on_chat_start
async def start():

    async with httpx.AsyncClient() as client:
        res = await client.post(f"{API_BASE}/session/create")
        data = res.json()

    chat_id = data["chat_id"]

    # store session
    cl.user_session.set("chat_id", chat_id)

    await cl.Message(
        content=f"🚀 Chat started (ID: {chat_id})"
    ).send()


# -----------------------------
# Handle User Message
# -----------------------------
@cl.on_message
async def handle_message(message: cl.Message):

    chat_id = cl.user_session.get("chat_id")

    async with httpx.AsyncClient(timeout=None) as client:

        async with client.stream(
            "POST",
            f"{API_BASE}/chat/{chat_id}/stream",
            json={"query": message.content},
        ) as response:

            msg = cl.Message(content="")
            await msg.send()

            async for chunk in response.aiter_text():
                if chunk:
                    await msg.stream_token(chunk)