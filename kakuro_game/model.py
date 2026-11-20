"""Kakuro CSP: coordinates, initial domains, and ordered sum constraints."""

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, permutations

Cell = tuple[int, int]
Domains = dict[Cell, frozenset[int]]
DIGITS = frozenset(range(1, 10))


@lru_cache(maxsize=None)
def _run_candidates(length: int, total: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        ordered
        for digits in combinations(sorted(DIGITS), length)
        if sum(digits) == total
        for ordered in permutations(digits)
    )


@dataclass(frozen=True)
class Run:
    clue: Cell
    direction: str
    total: int
    cells: tuple[Cell, ...]

    @property
    def candidates(self) -> tuple[tuple[int, ...], ...]:
        return _run_candidates(len(self.cells), self.total)

    def supported_domains(self, domains: Domains) -> tuple[frozenset[int], ...]:
        current = [domains[cell] for cell in self.cells]
        supported = [set() for _ in self.cells]
        for candidate in self.candidates:
            if all(value in domain for value, domain in zip(candidate, current)):
                for support, value in zip(supported, candidate):
                    support.add(value)
        return tuple(frozenset(support) for support in supported)

    def accepts(self, values: dict[Cell, int]) -> bool:
        digits = [values[cell] for cell in self.cells]
        return sum(digits) == self.total and len(set(digits)) == len(digits)

    @property
    def label(self) -> str:
        row, column = self.clue
        return f"{self.direction} ({row}, {column}), tổng {self.total}"


class Puzzle:
    def __init__(self, name: str, layout: str):
        # Rows and columns are one-based to match the report.
        self.name = name
        self.grid = tuple(tuple(row.split()) for row in layout.strip().splitlines())
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        if not all(len(row) == self.width for row in self.grid):
            raise ValueError("The grid must be rectangular")

        tiles = {
            (r, c): token
            for r, row in enumerate(self.grid, 1)
            for c, token in enumerate(row, 1)
        }
        self.cells = tuple(cell for cell, token in tiles.items() if token == ".")
        runs_by_cell: dict[Cell, list[Run]] = {cell: [] for cell in self.cells}
        runs = []
        for (r, c), token in tiles.items():
            if token in {"#", "."}:
                continue
            down, across = (int(value) for value in token.split("/"))
            for direction, total, dr, dc in (
                ("Dọc", down, 1, 0),
                ("Ngang", across, 0, 1),
            ):
                if total == 0:
                    continue
                cells = []
                current = r + dr, c + dc
                while tiles.get(current) == ".":
                    cells.append(current)
                    current = current[0] + dr, current[1] + dc
                if not cells or len(cells) > len(DIGITS) or total < 1:
                    raise ValueError(f"Invalid run at {(r, c)}: {direction}")
                run = Run((r, c), direction, total, tuple(cells))
                runs.append(run)
                for cell in cells:
                    runs_by_cell[cell].append(run)
        self.runs = tuple(runs)

        for cell, containing in runs_by_cell.items():
            if {run.direction for run in containing} != {"Dọc", "Ngang"}:
                raise ValueError(f"Cell {cell} must belong to an across and a down run")

        self._runs_by_cell = {cell: tuple(runs) for cell, runs in runs_by_cell.items()}

    def runs_for(self, cell: Cell) -> tuple[Run, ...]:
        return self._runs_by_cell[cell]

    def initial_domains(self) -> Domains:
        return dict.fromkeys(self.cells, DIGITS)

    def is_solution(self, values: dict[Cell, int]) -> bool:
        if values.keys() != self._runs_by_cell.keys() or any(
            value not in DIGITS for value in values.values()
        ):
            return False
        return all(run.accepts(values) for run in self.runs)
