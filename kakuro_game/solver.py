"""Generalized arc consistency on each run, then DFS with MRV."""

from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass

from model import Cell, Domains, Puzzle, Run


@dataclass(frozen=True)
class Step:
    kind: str
    domains: Domains
    message: str
    cells: tuple[Cell, ...] = ()


class KakuroSolver:
    def __init__(self, puzzle: Puzzle):
        self._puzzle = puzzle

    def solve_steps(self) -> Iterator[Step]:
        domains = self._puzzle.initial_domains()
        for step in self._search(domains, self._puzzle.runs):
            yield step
            if step.kind == "solved":
                return
        yield Step("unsolved", self._puzzle.initial_domains(), "Bảng không có lời giải.")

    def _propagate(
        self, domains: Domains, pending: tuple[Run, ...]
    ) -> Iterator[Step]:
        queue = deque(pending)
        queued = set(pending)
        while queue:
            run = queue.popleft()
            queued.remove(run)
            supported = run.supported_domains(domains)
            if not supported[0]:
                yield Step("conflict", domains.copy(), f"Mâu thuẫn tại dãy {run.label}.", run.cells)
                return

            changed = []
            for cell, support in zip(run.cells, supported):
                if support == domains[cell]:
                    continue
                domains[cell] = support
                changed.append(cell)
                for neighbor in self._puzzle.runs_for(cell):
                    if neighbor != run and neighbor not in queued:
                        queue.append(neighbor)
                        queued.add(neighbor)
            if changed:
                yield Step(
                    "propagate", domains.copy(), f"Thu hẹp miền theo dãy {run.label}.",
                    tuple(changed),
                )


    def _search(
        self, domains: Domains, pending: tuple[Run, ...]
    ) -> Iterator[Step]:
        for step in self._propagate(domains, pending):
            yield step
            if step.kind == "conflict":
                return

        cell = min(
            (cell for cell in self._puzzle.cells if len(domains[cell]) > 1),
            key=lambda cell: len(domains[cell]),
            default=None,
        )
        if cell is None:
            yield Step("solved", domains.copy(), "Đã tìm được lời giải.")
            return

        for value in sorted(domains[cell]):
            branch = domains.copy()
            branch[cell] = frozenset({value})
            yield Step("guess", branch.copy(), f"MRV chọn ô {cell}. Thử {value}.", (cell,))
            for step in self._search(branch, self._puzzle.runs_for(cell)):
                yield step
                if step.kind == "solved":
                    return
            yield Step("backtrack", domains.copy(), f"Quay lui tại ô {cell}, bỏ nhánh thử {value}.", (cell,))
