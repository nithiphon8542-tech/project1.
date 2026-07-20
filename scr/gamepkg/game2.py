# -*- coding: utf-8 -*-
"""
game2.py - เกมตีอิฐ (Breakout)
บังคับแท่นด้วยลูกศรซ้าย/ขวา หรือเมาส์ ตีลูกบอลให้ทำลายอิฐทั้งหมดให้ได้
"""
import tkinter as tk
from . import theme
from .widgets import RoundButton

BOARD_W = 760
BOARD_H = 520
PADDLE_W = 110
PADDLE_H = 16
BALL_R = 9

BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_PAD = 4
BRICK_TOP = 60
BRICK_H = 22

ROW_COLORS = ["#f87171", "#fb923c", "#fbbf24", "#4ade80", "#38bdf8", "#a78bfa"]


class BreakoutGame(tk.Frame):
    def __init__(self, parent, go_home):
        super().__init__(parent, bg=theme.BG_DARK)
        self.go_home = go_home
        self.after_id = None

        self._build_header()

        board_wrap = tk.Frame(self, bg=theme.BG_DARK)
        board_wrap.pack(pady=6)
        self.canvas = tk.Canvas(board_wrap, width=BOARD_W, height=BOARD_H,
                                 bg="#111827", highlightthickness=3,
                                 highlightbackground=theme.ACCENT_PINK)
        self.canvas.pack()

        self.canvas.bind("<Motion>", self._on_mouse)
        self.bind_all("<Left>", lambda e: self._move_paddle(-40))
        self.bind_all("<Right>", lambda e: self._move_paddle(40))
        self.bind_all("<space>", self._on_space)

        self._new_game()

    def _build_header(self):
        top = tk.Frame(self, bg=theme.BG_DARK)
        top.pack(fill="x", pady=(18, 4), padx=24)

        tk.Label(top, text="🧱  Breakout", font=theme.FONT_TITLE,
                 fg=theme.ACCENT_PINK, bg=theme.BG_DARK).pack(side="left")

        self.info_var = tk.StringVar(value="คะแนน: 0   |   ชีวิต: 3")
        tk.Label(top, textvariable=self.info_var, font=theme.FONT_SCORE,
                 fg=theme.TEXT_LIGHT, bg=theme.BG_DARK).pack(side="left", padx=24)

        RoundButton(top, "⟵ กลับเมนู", command=self._back_home,
                    width=140, height=42, fill=theme.ACCENT_RED,
                    hover_fill="#dc2626", text_color="#0f172a").pack(side="right")

        tk.Label(self, text="เลื่อนเมาส์ หรือใช้ลูกศรซ้าย/ขวา • กด Space เพื่อปล่อยลูกบอล",
                 font=theme.FONT_SUB, fg=theme.TEXT_MUTED, bg=theme.BG_DARK).pack()

    # ---------- game lifecycle ----------
    def _new_game(self):
        self.score = 0
        self.lives = 3
        self.running = True
        self.ball_launched = False
        self.paddle_x = BOARD_W / 2 - PADDLE_W / 2
        self._reset_ball()
        self._build_bricks()
        self._update_info()
        self._draw()
        self._loop()

    def _build_bricks(self):
        self.bricks = []  # (x1, y1, x2, y2, color)
        total_gap = BRICK_PAD * (BRICK_COLS + 1)
        brick_w = (BOARD_W - total_gap) / BRICK_COLS
        for r in range(BRICK_ROWS):
            for c in range(BRICK_COLS):
                x1 = BRICK_PAD + c * (brick_w + BRICK_PAD)
                y1 = BRICK_TOP + r * (BRICK_H + BRICK_PAD)
                x2 = x1 + brick_w
                y2 = y1 + BRICK_H
                self.bricks.append([x1, y1, x2, y2, ROW_COLORS[r % len(ROW_COLORS)]])

    def _reset_ball(self):
        self.ball_launched = False
        self.ball_x = self.paddle_x + PADDLE_W / 2
        self.ball_y = BOARD_H - 60
        self.ball_dx = 4
        self.ball_dy = -4

    def _update_info(self):
        self.info_var.set(f"คะแนน: {self.score}   |   ชีวิต: {self.lives}")

    # ---------- controls ----------
    def _on_mouse(self, event):
        self.paddle_x = min(max(0, event.x - PADDLE_W / 2), BOARD_W - PADDLE_W)
        if not self.ball_launched:
            self.ball_x = self.paddle_x + PADDLE_W / 2

    def _move_paddle(self, dx):
        self.paddle_x = min(max(0, self.paddle_x + dx), BOARD_W - PADDLE_W)
        if not self.ball_launched:
            self.ball_x = self.paddle_x + PADDLE_W / 2

    def _on_space(self, event):
        if not self.running:
            self._new_game()
        else:
            self.ball_launched = True

    # ---------- main loop ----------
    def _loop(self):
        if not self.running:
            return
        if self.ball_launched:
            self._update_ball()
        self._draw()
        self.after_id = self.after(16, self._loop)

    def _update_ball(self):
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_x <= BALL_R or self.ball_x >= BOARD_W - BALL_R:
            self.ball_dx *= -1
        if self.ball_y <= BALL_R:
            self.ball_dy *= -1

        paddle_y = BOARD_H - 34
        if (paddle_y <= self.ball_y + BALL_R <= paddle_y + PADDLE_H
                and self.paddle_x <= self.ball_x <= self.paddle_x + PADDLE_W
                and self.ball_dy > 0):
            hit_pos = (self.ball_x - (self.paddle_x + PADDLE_W / 2)) / (PADDLE_W / 2)
            self.ball_dx = hit_pos * 5.5
            self.ball_dy = -abs(self.ball_dy)

        for brick in list(self.bricks):
            x1, y1, x2, y2, _ = brick
            if x1 <= self.ball_x <= x2 and y1 <= self.ball_y <= y2:
                self.bricks.remove(brick)
                self.ball_dy *= -1
                self.score += 5
                self._update_info()
                break

        if self.ball_y > BOARD_H:
            self.lives -= 1
            self._update_info()
            if self.lives <= 0:
                self._game_over(False)
            else:
                self._reset_ball()

        if not self.bricks:
            self._game_over(True)

    def _game_over(self, won):
        self.running = False
        self.canvas.create_rectangle(0, 0, BOARD_W, BOARD_H, fill="#000000", stipple="gray50")
        msg = "🎉 คุณชนะแล้ว!" if won else "เกมจบแล้ว!"
        color = theme.ACCENT_GREEN if won else theme.ACCENT_RED
        self.canvas.create_text(BOARD_W / 2, BOARD_H / 2 - 30, text=msg,
                                 font=("Segoe UI", 26, "bold"), fill=color)
        self.canvas.create_text(BOARD_W / 2, BOARD_H / 2 + 10,
                                 text=f"คะแนนสุดท้าย: {self.score}",
                                 font=theme.FONT_SCORE, fill=theme.TEXT_LIGHT)
        self.canvas.create_text(BOARD_W / 2, BOARD_H / 2 + 45,
                                 text="กด Space เพื่อเล่นใหม่",
                                 font=theme.FONT_SUB, fill=theme.TEXT_MUTED)

    # ---------- drawing ----------
    def _draw(self):
        self.canvas.delete("all")
        for x1, y1, x2, y2, color in self.bricks:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#111827")

        paddle_y = BOARD_H - 34
        self.canvas.create_rectangle(self.paddle_x, paddle_y,
                                      self.paddle_x + PADDLE_W, paddle_y + PADDLE_H,
                                      fill=theme.ACCENT_PINK, outline="")

        self.canvas.create_oval(self.ball_x - BALL_R, self.ball_y - BALL_R,
                                 self.ball_x + BALL_R, self.ball_y + BALL_R,
                                 fill=theme.ACCENT_YELLOW, outline="")

        if not self.ball_launched and self.running:
            self.canvas.create_text(BOARD_W / 2, BOARD_H / 2,
                                     text="กด Space เพื่อเริ่มปล่อยลูกบอล",
                                     font=theme.FONT_SUB, fill=theme.TEXT_MUTED)

    def _back_home(self):
        self.running = False
        if self.after_id:
            self.after_cancel(self.after_id)
        self.go_home()

    def on_leave(self):
        self.running = False
        if self.after_id:
            self.after_cancel(self.after_id)
