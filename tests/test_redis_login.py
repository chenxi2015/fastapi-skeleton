import asyncio
import httpx
from redis.asyncio import Redis
from app.core.config import settings

BASE_URL = f"http://localhost:8000{settings.API_V1_STR}"
# Use the computed REDIS_URI from settings which includes password if set
REDIS_URL = (
    settings.REDIS_URI
    or f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}"
    if settings.REDIS_PASSWORD
    else f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
)


async def test_redis_login():
    async with httpx.AsyncClient() as client:
        # 1. Create a user
        email = "test_redis_user@example.com"
        password = "password123"
        user_data = {
            "email": email,
            "password": password,
            "is_active": True,
            "is_superuser": False,
            "username": "test_redis_user",
        }

        # Check if user exists or create
        # Note: The create endpoint in users.py might fail if user exists, so we might need to handle 400
        print(f"Creating user {email}...")
        response = await client.post(f"{BASE_URL}/users/", json=user_data)
        if response.status_code == 200:
            print("User created successfully.")
        elif response.status_code == 400 and "already exists" in response.text:
            print("User already exists, proceeding to login.")
        else:
            print(f"Failed to create user: {response.text}")
            return

        # 2. Login
        print("Logging in...")
        login_data = {"username": "test_redis_user", "password": password}
        response = await client.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code != 200:
            print(f"Login failed: {response.text}")
            return

        token_data = response.json()
        access_token = token_data.get("access_token")
        print(f"Login successful. Access token: {access_token}")

        # 3. Check Redis
        print("Checking Redis...")
        redis = Redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

        # Check token:{access_token}
        user_id = await redis.get(f"token:{access_token}")
        print(f"Redis key 'token:{access_token}': {user_id}")

        if user_id:
            print("SUCCESS: Token found in Redis!")

            # Check user:{user_id}:token
            stored_token = await redis.get(f"user:{user_id}:token")
            print(f"Redis key 'user:{user_id}:token': {stored_token}")

            if stored_token == access_token:
                print("SUCCESS: User token mapping is correct!")
            else:
                print(
                    f"WARNING: User token mapping mismatch or missing. Expected {access_token}, got {stored_token}"
                )

        else:
            print("FAILURE: Token NOT found in Redis.")

        await redis.close()


if __name__ == "__main__":
    asyncio.run(test_redis_login())
