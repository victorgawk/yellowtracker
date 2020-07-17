import asyncio

class CoroutineUtil(object):
    @staticmethod
    async def run(coroutine):
        try:
            return await coroutine
        except:
            pass

    @staticmethod
    async def run_with_retries(coroutine):
        curr = 0
        max = 3
        while curr < max:
            try:
                return await coroutine
                break
            except:
                curr += 1
                print('retrying to execute coroutine - retry number ' + str(curr))
                await asyncio.sleep(curr)
        if curr == max:
            print('retries failed')