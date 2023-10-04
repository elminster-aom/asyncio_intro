import asyncio
import time

_WAIT_TIMES = {
    "compile_kernel": 3,
    "laundry": 2,
    "bake": 2,
    "cut_grass": 1,
}
_LIMIT_WORK_IN = 1

async def work_in(duty: str, limit: asyncio.Semaphore) -> None:
    if duty not in _WAIT_TIMES:
        known_duties = ', '.join(_WAIT_TIMES.keys())
        raise ValueError(f"Unknown duty {duty}, valid ones: {known_duties}.")
    async with limit:
        print("> Started duty", duty)
        await asyncio.sleep(_WAIT_TIMES[duty])
        print("<<  Ended duty", duty)


async def main() -> None:
    todays_duties = ("compile_kernel", "bake", "laundry")
    semaphore = asyncio.Semaphore(_LIMIT_WORK_IN)   # Limit concurrent duties
    await asyncio.wait(
        [ asyncio.create_task(work_in(duty, semaphore)) for duty in todays_duties ]
    )  # For the example simplicity, ignored return


if __name__ == '__main__':
    start_day = time.perf_counter()
    asyncio.run(main())
    end_day = time.perf_counter()
    print(f"My work day took: {end_day - start_day:.2f} seconds")
