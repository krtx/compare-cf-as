from minio import Minio
import os
import io
import time
import random
import cProfile
import multiprocessing
import asyncio
from concurrent.futures import ThreadPoolExecutor

OBJECT_COUNT = 1000


def sequential():
    client = Minio('minio:9000',
        access_key=os.environ["MINIO_ACCESS_KEY"],
        secret_key=os.environ["MINIO_SECRET_KEY"],
        secure=False)

    bucket_name = "test"

    try:
        client.make_bucket(bucket_name, location="ap-northeast-1")
    except Exception:
        pass

    for index in range(0, OBJECT_COUNT):
        length = random.randint(10, 1000000)
        data = os.urandom(length)
        client.put_object(bucket_name, f"object{index}", io.BytesIO(data), length)


# def send_object(index):
#     client = Minio("minio:9000",
#         access_key=os.environ["MINIO_ACCESS_KEY"],
#         secret_key=os.environ["MINIO_SECRET_KEY"],
#         secure=False)
        
#     length = random.randint(10, 1000000)
#     data = os.urandom(length)
#     client.put_object("mp", f"object{index}", io.BytesIO(data), length)

# don't work
# def mp():
#     client = Minio("minio:9000",
#             access_key=os.environ["MINIO_ACCESS_KEY"],
#             secret_key=os.environ["MINIO_SECRET_KEY"],
#             secure=False)

#     try:
#         client.make_bucket("mp")
#     except Exception:
#         pass

#     with multiprocessing.Pool(processes=os.cpu_count()) as pool:
#         pool.map(send_object, range(0, OBJECT_COUNT))


def thread():
    client = Minio("minio:9000",
            access_key=os.environ["MINIO_ACCESS_KEY"],
            secret_key=os.environ["MINIO_SECRET_KEY"],
            secure=False)

    try:
        client.make_bucket("thread")
    except Exception:
        pass

    def send_object(index):
        length = random.randint(10, 1000000)
        data = os.urandom(length)
        client.put_object("thread", f"object{index}", io.BytesIO(data), length)

    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()*10) as executor:
        executor.map(send_object, range(0, OBJECT_COUNT))


async def asyn(loop):
    client = Minio("minio:9000",
            access_key=os.environ["MINIO_ACCESS_KEY"],
            secret_key=os.environ["MINIO_SECRET_KEY"],
            secure=False)

    try:
        client.make_bucket("asyn")
    except Exception:
        pass
    
    async def send_object(index):
        length = random.randint(10, 1000000)
        data = os.urandom(length)
        await loop.run_in_executor(None, lambda index: client.put_object("asyn", f"object{index}", io.BytesIO(data), length), index)

    tasks = [send_object(index) for index in range(0, OBJECT_COUNT)]
    
    await asyncio.gather(*tasks)


def main():
    # print("sequential")
    # start = time.time()
    # sequential()
    # print(f"{time.time() - start}")

    print("concurrent.futures")
    start = time.time()
    thread()
    print(f"{time.time() - start}")

    print("asyn")
    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyn(loop))
    print(f"{time.time() - start}")


if __name__ == "__main__":
    input("input>")
    main()