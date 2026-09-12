import asyncio

async def add(a,b):
    await asyncio.sleep(1)
    return a+b

async def main():
    result = await asyncio.gather(add(1,2),add(4,2),add(3,2),add(7,2),add(1,2),add(2,2))

    # res = add(1,2)
    # res1 = add(2,3)

    for res in result:
        print(res)

asyncio.run(main())