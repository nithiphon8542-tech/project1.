# -*- coding: utf-8 -*-
"""
game1.py - เกมงู (Snake)
บังคับด้วยลูกศร/WASD กินอาหารเพื่อโตและเพิ่มคะแนน ห้ามชนกำแพงหรือชนตัวเอง
"""
import tkinter as tk
import random
from . import theme
from .widgets import RoundButton

CELL = 24
COLS = 30
ROWS = 20
BOARD_W = CELL * COLS
BOARD_H = CELL * ROWS


class SnakeGame(tk.Frame):
    def __init__(self, parent, go_home):
        super().__init__(parent, bg=theme.BG_DARK)
        self.go_home = go_home
        self.after_id = None
        self.speed_ms = 130

        self._build_header()

        board_wrap = tk.Frame(self, bg=theme.BG_DARK)
        board_wrap.pack(pady=10)
        self.canvas = tk.Canvas(board_wrap, width=BOARD_W, height=BOARD_H,
                                 bg="#111827", highlightthickness=3,
                                 highlightbackground=theme.ACCENT_GREEN)
        self.canvas.pack()

        self.bind_all("<Key>", self._on_key)
        self._new_game()

    # ---------- UI header ----------
    def _build_header(self):
        top = tk.Frame(self, bg=theme.BG_DARK)
        top.pack(fill="x", pady=(18, 4), padx=24)

        tk.Label(top, text="🐍  Snake", font=theme.FONT_TITLE,
                 fg=theme.ACCENT_GREEN, bg=theme.BG_DARK).pack(side="left")

        self.score_var = tk.StringVar(value="คะแนน: 0")
        tk.Label(top, textvariable=self.score_var, font=theme.FONT_SCORE,
                 fg=theme.TEXT_LIGHT, bg=theme.BG_DARK).pack(side="left", padx=24)

        RoundButton(top, "⟵ กลับเมนู", command=self._back_home,
                    width=140, height=42, fill=theme.ACCENT_RED,
                    hover_fill="#dc2626", text_color="#0f172a").pack(side="right")

        tk.Label(self, text="ใช้ปุ่มลูกศร หรือ W A S D เพื่อบังคับทิศทาง",
                 font=theme.FONT_SUB, fg=theme.TEXT_MUTED, bg=theme.BG_DARK).pack()

    # ---------- game lifecycle ----------
    def _new_game(self):
        self.snake = [(COLS // 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2),
                      (COLS // 2 - 2, ROWS // 2)]
        self.direction = "Right"
        self.next_direction = "Right"
        self.score = 0
        self.running = True
        self.food = self._place_food()
        self.score_var.set("คะแนน: 0")
        self._draw()
        self._tick()

    def _place_food(self):
        empty = [(x, y) for x in range(COLS) for y in range(ROWS)
                 if (x, y) not in self.snake]
        return random.choice(empty)

    def _on_key(self, event):
        key = event.keysym
        mapping = {"w": "Up", "s": "Down", "a": "Left", "d": "Right"}
        key = mapping.get(key.lower(), key)
        opposite = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if key in ("Up", "Down", "Left", "Right") and key != opposite.get(self.direction):
            self.next_direction = key
        if key == "r" and not self.running:
            self._new_game()

    def _tick(self):
        if not self.running:
            return
        self.direction = self.next_direction
        hx, hy = self.snake[0]
        dx, dy = {"Up": (0, -1), "Down": (0, 1),
                  "Left": (-1, 0), "Right": (1, 0)}[self.direction]
        new_head = (hx + dx, hy + dy)

        if (new_head in self.snake or not (0 <= new_head[0] < COLS)
                or not (0 <= new_head[1] < ROWS)):
            self._game_over()
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 10
            self.score_var.set(f"คะแนน: {self.score}")
            self.food = self._place_food()
            self.speed_ms = max(70, self.speed_ms - 2)
        else:
            self.snake.pop()

        self._draw()
        self.after_id = self.after(self.speed_ms, self._tick)

    def _game_over(self):
        self.running = False
        self.canvas.create_rectangle(0, 0, BOARD_W, BOARD_H, fill="#000000", stipple="gray50")
        self.canvas.create_text(BOARD_W / 2, BOARD_H / 2 - 30, text="เกมจบแล้ว!",
                                 font=("Segoe UI", 26, "bold"), fill=theme.ACCENT_RED)
        self.canvas.create_text(BOARD_W / 2, BOARD_H / 2 + 10,
                                 text=f"คะแนนสุดท้าย: {self.score}",
                                 font=theme.FONT_SCORE, fill=theme.TEXT_LIGHT)
        self.canvas.create_text(BOARD_W / 2, BOARD_H / 2 + 45,
                                 text="กด R เพื่อเล่นใหม่",
                                 font=theme.FONT_SUB, fill=theme.TEXT_MUTED)

    def _draw(self):
        self.canvas.delete("all")
        # grid ตารางบาง ๆ ให้ดูมีมิติ
        for x in range(0, BOARD_W, CELL):
            self.canvas.create_line(x, 0, x, BOARD_H, fill="#1f2937")
        for y in range(0, BOARD_H, CELL):
            self.canvas.create_line(0, y, BOARD_W, y, fill="#1f2937")

        fx, fy = self.food
        self.canvas.create_oval(fx * CELL + 3, fy * CELL + 3,
                                 fx * CELL + CELL - 3, fy * CELL + CELL - 3,
                                 fill=theme.ACCENT_YELLOW, outline="")

        for i, (x, y) in enumerate(self.snake):
            color = theme.ACCENT_GREEN if i == 0 else "#22c55e"
            self.canvas.create_rectangle(
                x * CELL + 1, y * CELL + 1, x * CELL + CELL - 1, y * CELL + CELL - 1,
                fill=color, outline="#064e3b")

    def _back_home(self):
        self.running = False
        if self.after_id:
            self.after_cancel(self.after_id)
        self.go_home()

    def on_leave(self):
        """เรียกตอนออกจากหน้านี้ เพื่อหยุด loop และยกเลิก key binding"""
        self.running = False
        if self.after_id:
            self.after_cancel(self.after_id)
