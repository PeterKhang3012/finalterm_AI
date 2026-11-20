"""Tkinter board and step-by-step playback of the Kakuro solver."""

from collections import Counter
import tkinter as tk
from tkinter import ttk

from model import Domains, Puzzle
from puzzles import PUZZLES
from solver import KakuroSolver, Step

CELL_SIZE = 56
HIGHLIGHT = {
    "propagate": "#bde4ff",
    "guess": "#ffe5a1",
    "conflict": "#ffb6b6",
    "backtrack": "#e6cffb",
}


class KakuroUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Kakuro CSP")
        root.configure(padx=14, pady=14)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        controls = ttk.Frame(root)
        controls.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.selector = ttk.Combobox(
            controls, state="readonly", width=25, values=[p.name for p in PUZZLES]
        )
        self.selector.current(0)
        self.selector.pack(side="left", padx=(0, 8))
        self.selector.bind("<<ComboboxSelected>>", self.reset)
        self.next_button = ttk.Button(controls, text="Bước tiếp", command=self.advance)
        self.next_button.pack(side="left")
        self.play_button = ttk.Button(controls, text="Tự chạy", command=self.toggle_play)
        self.play_button.pack(side="left", padx=6)
        ttk.Button(controls, text="Làm lại", command=self.reset).pack(side="left")

        body = ttk.Frame(root)
        body.grid(row=1, column=0, sticky="nsew")
        body.rowconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        self.board = tk.Canvas(body, highlightthickness=0)
        self.board.grid(row=0, column=0, sticky="nw", padx=(0, 12))

        history_frame = ttk.Frame(body)
        history_frame.grid(row=0, column=1, sticky="nsew")
        history_frame.rowconfigure(1, weight=1)
        history_frame.columnconfigure(0, weight=1)
        ttk.Label(history_frame, text="Nhật ký giải").grid(row=0, column=0, sticky="w")
        self.history = tk.Text(history_frame, width=28, height=12, wrap="word", state="disabled")
        scroll = ttk.Scrollbar(history_frame, command=self.history.yview)
        self.history.configure(yscrollcommand=scroll.set)
        self.history.grid(row=1, column=0, sticky="nsew")
        scroll.grid(row=1, column=1, sticky="ns")
        self.status = ttk.Label(root)
        self.status.grid(row=2, column=0, sticky="w", pady=(10, 0))

        self.timer: str | None = None
        self.reset()

    @property
    def puzzle(self) -> Puzzle:
        return PUZZLES[self.selector.current()]

    def reset(self, _event: tk.Event | None = None) -> None:
        self.pause()
        self.steps = KakuroSolver(self.puzzle).solve_steps()
        self.counts: Counter[str] = Counter()
        self.next_button.state(["!disabled"])
        self.play_button.state(["!disabled"])
        self.history.configure(state="normal")
        self.history.delete("1.0", "end")
        self.history.configure(state="disabled")
        self.update_status()
        self.draw(self.puzzle.initial_domains())

    def update_status(self) -> None:
        self.status.configure(text=(
            f"Lan truyền {self.counts['propagate']}   |   "
            f"Thử {self.counts['guess']}   |   Quay lui {self.counts['backtrack']}"
        ))

    def draw(self, domains: Domains, step: Step | None = None) -> None:
        self.board.delete("all")
        self.board.configure(
            width=self.puzzle.width * CELL_SIZE + 1,
            height=self.puzzle.height * CELL_SIZE + 1,
        )
        marked = set(step.cells) if step else set()
        for row, tokens in enumerate(self.puzzle.grid, 1):
            for column, token in enumerate(tokens, 1):
                x, y = (column - 1) * CELL_SIZE + 1, (row - 1) * CELL_SIZE + 1