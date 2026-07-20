# -*- coding: utf-8 -*-
"""
menu.py - หน้าเมนูหลัก ให้ผู้เล่นเลือกว่าจะเล่นเกมไหน
"""
import tkinter as tk
from . import theme
from .widgets import RoundButton


class MainMenu(tk.Frame):
    def __init__(self, parent, on_select_game1, on_select_game2):
        super().__init__(parent, bg=theme.BG_DARK)

        center = tk.Frame(self, bg=theme.BG_DARK)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="🎮 GAME CENTER", font=("Segoe UI", 34, "bold"),
                 fg=theme.ACCENT, bg=theme.BG_DARK).pack(pady=(0, 4))
        tk.Label(center, text="เลือกเกมที่ต้องการเล่น", font=theme.FONT_SUB,
                 fg=theme.TEXT_MUTED, bg=theme.BG_DARK).pack(pady=(0, 30))

        card_row = tk.Frame(center, bg=theme.BG_DARK)
        card_row.pack()

        self._build_card(card_row, "🐍", "Snake", "งูกินอาหารสุดคลาสสิก",
                          theme.ACCENT_GREEN, on_select_game1).pack(side="left", padx=18)
        self._build_card(card_row, "🧱", "Breakout", "ตีอิฐให้แตกกระจาย",
                          theme.ACCENT_PINK, on_select_game2).pack(side="left", padx=18)

        tk.Label(center, text="พัฒนาโดยใช้ Python + Tkinter", font=theme.FONT_SMALL,
                 fg=theme.TEXT_MUTED, bg=theme.BG_DARK).pack(pady=(34, 0))

    def _build_card(self, parent, emoji, title, subtitle, color, command):
        card = tk.Frame(parent, bg=theme.BG_PANEL, width=260, height=280,
                         highlightthickness=2, highlightbackground=color)
        card.pack_propagate(False)

        tk.Label(card, text=emoji, font=("Segoe UI", 54), bg=theme.BG_PANEL).pack(pady=(28, 6))
        tk.Label(card, text=title, font=("Segoe UI", 20, "bold"),
                 fg=theme.TEXT_LIGHT, bg=theme.BG_PANEL).pack()
        tk.Label(card, text=subtitle, font=theme.FONT_SUB,
                 fg=theme.TEXT_MUTED, bg=theme.BG_PANEL).pack(pady=(4, 20))

        RoundButton(card, "เล่นเลย ▶", command=command, width=180, height=48,
                    fill=color, hover_fill=theme.ACCENT_DARK,
                    text_color="#0f172a").pack()
        return card
