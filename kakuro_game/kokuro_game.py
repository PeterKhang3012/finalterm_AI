"""Run the Kakuro interface or solve the boards from a terminal."""

import argparse
from collections import Counter
from time import perf_counter

from puzzles import PUZZLES
from solver import KakuroSolver


def print_solutions() -> None:
    for puzzle in PUZZLES:
        started = perf_counter()
        counts: Counter[str] = Counter()
        for step in KakuroSolver(puzzle).solve_steps():
            counts[step.kind] += 1
        elapsed = perf_counter() - started
        print(f"\n{puzzle.name}")
        if step.kind == "solved":
            values = {cell: next(iter(domain)) for cell, domain in step.domains.items()}
            if not puzzle.is_solution(values):
                raise RuntimeError("Bộ giải trả về lời giải không hợp lệ.")
            for row in range(1, puzzle.height + 1):
                print(" ".join(str(values.get((row, col), "#"))
                               for col in range(1, puzzle.width + 1)))
        else:
            print(step.message)
        print(f"Lan truyền {counts['propagate']} | Thử {counts['guess']} | "
              f"Quay lui {counts['backtrack']} | {elapsed:.3f} giây")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solve", action="store_true", help="In lời giải và thống kê ra terminal")
    if parser.parse_args().solve:
        print_solutions()
    else:
        from ui import launch

        launch()


if __name__ == "__main__":
    main()
