import logging
import traceback

log = logging.getLogger(__name__)

class CoroutineUtil:

    @staticmethod
    async def run(coroutine):
        try:
            return await coroutine
        except BaseException:
            log.error(f"Unexpected error.\n{CoroutineUtil.get_stack_str()}", exc_info=True)

    @staticmethod
    def get_stack_str():
        stack_str = ""
        stack = traceback.format_stack()
        for e in stack:
            stack_str += e
        return stack_str
