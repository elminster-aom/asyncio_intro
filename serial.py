import time

_WAIT_TIMES = {
    "compile_kernel": 3,
    "laundry": 2,
    "bake": 2,
    "cut_grass": 1,
}


def work_in(duty: str) -> None:
    if duty not in _WAIT_TIMES:
        known_duties = ', '.join(_WAIT_TIMES.keys())
        raise ValueError(f"Unknown duty {duty}, valid ones: {known_duties}.")
    print("> Started duty", duty)
    time.sleep(_WAIT_TIMES[duty])
    print("<<  Ended duty", duty)


def main() -> None:
    todays_duties = ("compile_kernel", "bake", "laundry")
    for duty in todays_duties:
        work_in(duty)


if __name__ == '__main__':
    start_day = time.perf_counter()
    main()
    end_day = time.perf_counter()
    print(f"My work day took: {end_day - start_day:.2f} seconds")
