import os
import json
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from dotenv import load_dotenv
import logging

import asyncio
from openai import AsyncOpenAI
import openai

from pathlib import Path


import models


# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Slack app
app = AsyncApp(token=os.getenv("SLACK_BOT_TOKEN"))



# Set up logging
logging.basicConfig(level=logging.DEBUG)



'''
# Event listener for messages
@app.event("message")
async def handle_message(event, say):
    logging.debug(f"Received event: {event}")
    await say("Hi")

# Event listener for app mentions
@app.event("app_mention")
async def handle_app_mention(event, say):
    logging.debug(f"Received app_mention event: {event}")
    await say("Hi")
'''

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Function to call OpenAI API
async def call_openai_api(convo:models.Conversation) -> str:
    chat_completion = await client.chat.completions.create(
        messages=convo.messages,# noqa 
        model="gpt-4o"
    )
    return chat_completion.choices[0].message.content.strip()



# Event listener for app mentions
@app.event("app_mention")
async def handle_app_mention(event, say):
    logging.debug(f"Received app_mention event: {event}")
    user_message = event['text']
    # print()
    # print(f"EVENT: {event}")
    # print()
    user_id = event["user"]
    channel_id = event["channel"]
    con_key = user_id +"-"+ channel_id
    settings = models.get_conversations()
    if con_key in settings.conversations:
        convo = settings.conversations[con_key]
    else:
        convo = models.Conversation()
    convo.add_message(user_message,"user")
    response = await call_openai_api(convo)
    convo.add_message(response,"assistant")
    settings.conversations[con_key] = convo
    models.save_conversations(settings)
    await say(response)



# Event listener for messages
@app.event("message")
async def handle_message(event, say):
    logging.debug(f"Received event: {event}")
    user_message = event['text']
    user_id = event['user']
    channel_id = event['channel']
    con_key = user_id + "-" + channel_id
    # make userid and channelid as a combined name and put it into the record
    settings = models.get_conversations()  
    # To record it, they can read all conversations in the settings, if they exist in the json file.
    if con_key in settings.conversations:
        convo = settings.conversations[con_key]
    else:
        convo = models.Conversation()
    convo.add_message(user_message, "user")
    response = await call_openai_api(convo)
    convo.add_message(response, "assistant")
    settings.conversations[con_key] = convo
    models.save_conversations(settings)
    await say(response)

# Event listener for messages
# @app.event("message")
# async def handle_message(event, say):
#     logging.debug(f"Received event: {event}")
#     user_message = event['text']
#     user_id = event['user']  # Adjust this according to your event object structure
#     response = await call_openai_api(user_message)
#     # Log conversation in the background
#     asyncio.create_task(asyncio.to_thread(log_conversation, user_id, user_message, response))
#     await say(response)

# # Event listener for app mentions
# @app.event("app_mention")
# async def handle_app_mention(event, say):
#     logging.debug(f"Received app_mention event: {event}")
#     # Extracting the text from the event that mentions the bot
#     try:
#         user_message = event['text']
#         user_id = event['user']  # Ensure this is the correct key to access user ID
#         response = await call_openai_api(user_message)
#         # Optionally log the conversation, utilizing a background thread to avoid blocking
#         asyncio.create_task(asyncio.to_thread(log_conversation, user_id, user_message, response))
#         await say(response)
#     except Exception as e:
#         logging.error(f"Error handling app_mention: {str(e)}")
#         await say("Sorry, I encountered an error processing your mention.")

# Initialize Socket Mode handler
async def main():
    handler = AsyncSocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))
    await handler.start_async()

# @app.event("message")
# async def try_except(input,output):
#     out = await client.chat.completions.create(
#         messages=convo.messages,# noqa 
#         model="gpt-4"
#     )
#     d  = output.np()-out.np()
#     cosine_similarity = d/(output.np() ** 2 +out.np() ** 2)
#     if cosine_similarity > 1:
#         return 1
#     elif cosine_similarity < -1:
#         return -1
#     else:
#         return cosine_similarity


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    