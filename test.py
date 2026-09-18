import redis.asyncio as redis
import asyncio
from redis.exceptions import WatchError


# async def inc(name):
#     async with redis.Redis(host="localhost", port=6379, decode_responses=True) as r:

#         async with r.pipeline(transaction=True) as pipe:
#             while True:
#                 try:
#                     print(name, "watching")
#                     await pipe.watch("counter")
#                     curr = int(await r.get("counter"))
#                     await asyncio.sleep(1)
#                     pipe.multi()
#                     pipe.set("counter", str(curr+1))
#                     await pipe.execute()
#                     print("success")
#                     break
#                 except WatchError:
#                     continue


# async def test():
#     async with redis.Redis(host="localhost", port=6379, decode_responses=True) as r:

#         await r.set("counter", "0")    

#     await asyncio.gather(inc("t1"), inc("t2"), inc("t3"), inc("t4"))

#     async with redis.Redis(host="localhost", port=6379, decode_responses=True) as r:

#         print(await r.get("counter"))

# asyncio.run(test())

async def pubsub_example():
    async with redis.Redis(
        host='localhost', port=6379, decode_responses=True
    ) as r:
        async with r.pubsub() as pubsub:
            await pubsub.subscribe('channel-1')

            async def reader():
                async for message in pubsub.listen():
                    if message['type'] == 'message':
                        print(message['data'])
                        # hello
                        break

            reader_task = asyncio.create_task(reader())
            await asyncio.sleep(0.1)
            await r.publish('channel-1', 'hello123')
            await reader_task

asyncio.run(pubsub_example())