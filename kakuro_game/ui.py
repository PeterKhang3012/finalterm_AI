"""Tkinter board and step-by-step playback of the Kakuro solver."""

from collections import Counter
import tkinter as tk
from tkinter import ttk

from model import Puzzle
from puzzles import PUZZLES
from solver import KakuroSolver, Step

BOARD_SIZE = 576
MAX_CELL_SIZE = 96
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
        body.columnconfigure(0, weight=1)
        self.board = tk.Canvas(
            body, width=BOARD_SIZE, height=BOARD_SIZE, highlightthickness=0,
            background=root.cget("background"),
        )
        self.board.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

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
        self.board.bind("<Configure>", lambda _event: self.draw())

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
        self.domains = self.puzzle.initial_domains()
        self.current_step: Step | None = None
        self.draw()

    def update_status(self) -> None:
        self.status.configure(text=(
            f"Lan truyền {self.counts['propagate']}   |   "
            f"Thử {self.counts['guess']}   |   Quay lui {self.counts['backtrack']}"
        ))

    def draw(self) -> None:
        self.board.delete("all")
        width = self.board.winfo_width()
        height = self.board.winfo_height()
        cell_size = min(MAX_CELL_SIZE, (width - 2) // self.puzzle.width,
                        (height - 2) // self.puzzle.height)
        if cell_size < 1:
            return
        x_start = (width - self.puzzle.width * cell_size) // 2
        y_start = (height - self.puzzle.height * cell_size) // 2
        small_font = ("TkDefaultFont", -max(1, round(cell_size * 0.22)))
        large_font = ("TkDefaultFont", -max(1, round(cell_size * 0.47)), "bold")
        step = self.current_step
        marked = set(step.cells) if step else set()
        for row, tokens in enumerate(self.puzzle.grid, 1):
            for column, token in enumerate(tokens, 1):
                x = x_start + (column - 1) * cell_size
                y = y_start + (row - 1) * cell_size
                cell = row, column
                if token == ".":
                    color = HIGHLIGHT[step.kind] if cell in marked and step else "white"
                    self.board.create_rectangle(x, y, x + cell_size, y + cell_size, fill=color)
                    domain = self.domains[cell]
                    if len(domain) == 1:
                        self.board.create_text(
                            x + cell_size / 2, y + cell_size / 2,
                            text=str(next(iter(domain))), font=large_font,
                        )
                    else:
                        for value in sorted(domain):
                            r, c = divmod(value - 1, 3)
                            self.board.create_text(
                                x + (c + 0.5) * cell_size / 3,
                                y + (r + 0.5) * cell_size / 3,
                                text=str(value), fill="#344e68", font=small_font,
                            )
                    continue

                self.board.create_rectangle(x, y, x + cell_size, y + cell_size, fill="#34465b")
                self.board.create_line(x, y, x + cell_size, y + cell_size, fill="#aebdcb")
                if token != "#":
                    down, across = token.split("/")
                    if across != "0":
                        self.board.create_text(x + cell_size * 0.73, y + cell_size * 0.27,
                                               text=across, fill="white", font=small_font)
                    if down != "0":
                        self.board.create_text(x + cell_size * 0.27, y + cell_size * 0.73,
                                               text=down, fill="white", font=small_font)

    def advance(self) -> bool:
        step = next(self.steps, None)
        if step is None:
            return False
        self.counts[step.kind] += 1
        self.domains = step.domains
        self.current_step = step
        self.draw()
        self.update_status()
        self.history.configure(state="normal")
        self.history.insert("end", f"{sum(self.counts.values())}. {step.message}\n")
        self.history.see("end")
        self.history.configure(state="disabled")
        if step.kind in {"solved", "unsolved"}:
            self.pause()
            self.next_button.state(["disabled"])
            self.play_button.state(["disabled"])
            return False
        return True

    def pause(self) -> None:
        if self.timer is not None:
            self.root.after_cancel(self.timer)
            self.timer = None
        self.play_button.configure(text="Tự chạy")
        self.next_button.state(["!disabled"])

    def toggle_play(self) -> None:
        if self.timer is not None:
            self.pause()
            return
        self.play_button.configure(text="Tạm dừng")
        self.next_button.state(["disabled"])
        self.tick()

    def tick(self) -> None:
        self.timer = None
        if self.advance():
            self.timer = self.root.after(200, self.tick)


def launch() -> None:
    root = tk.Tk()
    KakuroUI(root)
    root.mainloop()
