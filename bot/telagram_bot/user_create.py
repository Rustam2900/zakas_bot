import aiohttp
import logging
API_URL = "http://127.0.0.1:8000/api/create-user/"  # Replace with your Django API endpoint

logger = logging.getLogger(__name__)

async def save_user_data(user_data):
    # Remove None values from user_data
    user_data = {k: v for k, v in user_data.items() if v is not None}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=user_data) as response:
            if response.status not in (200, 201):
                logger.error(f"Failed to save user data: {response.status} - {await response.text()}")
            return response.status