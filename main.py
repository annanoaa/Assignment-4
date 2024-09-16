import aiohttp
import asyncio
import json
import time

first_post =True
# Async function to fetch data from a URL
async def fetch_data(session, url, lock):
    global first_post
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                async with lock:  # Acquiring lock for thread-safe file writing
                    with open('post_data.json', 'a') as json_file:
                        if not first_post:
                            json_file.write(',\n')
                        else:
                            first_post = False
                        json.dump(data, json_file, indent=4)
    except Exception as e:
        print(f"Error fetching {url}: {e}")

# Main function to handle all async tasks
async def main():
    start_time = time.time()

    # Initialize the lock
    lock = asyncio.Lock()

    # Create a new JSON file and add opening bracket
    with open('post_data.json', 'w') as json_file:
        json_file.write('[\n')

    # List of URLs
    urls = [f'https://jsonplaceholder.typicode.com/posts/{i}' for i in range(1, 78)]

    # Using aiohttp to create an asynchronous session
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url, lock) for url in urls]
        await asyncio.gather(*tasks)

    # Add closing bracket to the JSON file
    with open('post_data.json', 'a') as json_file:
        json_file.write('\n]')

    end_time = time.time()
    print("All posts have been fetched and saved to posts_data.json")
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
