import asyncio
import time
from typing import Any, Awaitable, Self

_WAIT_TIMES = {
    "compile_kernel": 3,
    "laundry": 2,
    "bake": 2,
    "cut_grass": 1,
}
_LIMIT_pool = 2

class TaskPool(object):
    def __init__(self, pool_size: int=1) -> None:
        self._semaphore = asyncio.Semaphore(pool_size)
        self._pool: set[Awaitable[Any]] = set()

    async def add(self, coro: Awaitable[Any]) -> None:
        await self._semaphore.acquire()
        task = asyncio.ensure_future(coro)
        task.add_done_callback(self._on_task_done)
        self._pool.add(task)

    def _on_task_done(self, task: Awaitable[Any]) -> None:
        self._pool.remove(task)
        self._semaphore.release()

    async def join(self) -> None:
        await asyncio.gather(*self._pool)

    async def __aenter__(self) -> Self:
        return self

    def __aexit__(self, *_: tuple[Any]) -> Awaitable[None]:
        return self.join()


async def work_in(duty: str) -> None:
    if duty not in _WAIT_TIMES:
        known_duties = ', '.join(_WAIT_TIMES.keys())
        raise ValueError(f"Unknown duty {duty}, valid ones: {known_duties}.")
    print("> Started duty", duty)
    await asyncio.sleep(_WAIT_TIMES[duty])
    print("<<  Ended duty", duty)


async def main() -> None:
    todays_duties = ("compile_kernel", "bake", "laundry")
    async with TaskPool(_LIMIT_pool) as tasks:
        for duty in todays_duties:
            await tasks.add(work_in(duty))


if __name__ == '__main__':
    start_day = time.perf_counter()
    asyncio.run(main())
    end_day = time.perf_counter()
    print(f"My work day took: {end_day - start_day:.2f} seconds")
