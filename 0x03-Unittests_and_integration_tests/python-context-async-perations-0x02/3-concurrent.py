import asyncio
import aiosqlite

async def async_fetch_users():
    """Fetch all users asynchronously."""
    async with aiosqlite.connect("users.db") as conn:
        cursor = await conn.execute("SELECT * FROM users")
        return await cursor.fetchall()

async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect("users.db") as conn:
        cursor = await conn.execute("SELECT * FROM users WHERE age > ?", (40,))
        return await cursor.fetchall()

async def fetch_concurrently():
    """Run queries concurrently using asyncio.gather."""
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All Users:", all_users)
    print("Users Older Than 40:", older_users)

# Run the async fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())