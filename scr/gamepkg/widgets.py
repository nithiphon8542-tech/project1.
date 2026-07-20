# -*- coding: utf-8 -*-
"""
widgets.py
วิดเจ็ตปุ่มโค้งมนสวย ๆ วาดด้วย Canvas (tkinter ปกติปุ่มจะเหลี่ยม ๆ ไม่สวย)
"""
import tkinter as tk
from . import theme


class RoundButton(tk.Canvas):
    """ปุ่มมุมโค้งมน มี hover effect วาดด้วย Canvas ล้วน ๆ (ไม่ต้องใช้ไลบรารีเสริม)"""

    def __init__(self, parent, text, command=None,
                 width=260, height=56, radius=18,
                 fill=None, hover_fill=None, text_color=None,
                 font=None, **kwargs):
        super().__init__(parent, width=width, height=height,
                          bg=parent["bg"] if isinstance(parent, (tk.Frame, tk.Tk)) else theme.BG_DARK,
                          highlightthickness=0, **kwargs)
        self.command = command
        self.width = width
        self.height = height
        self.radius = radius
        self.fill = fill or theme.ACCENT
        self.hover_fill = hover_fill or theme.ACCENT_DARK
        self.text_color = text_color or "#0f172a"
        self.font = font or theme.FONT_BTN
        self.text = text

        self._draw(self.fill)
        self.bind("<Enter>", lambda e: self._draw(self.hover_fill))
        self.bind("<Leave>", lambda e: self._draw(self.fill))
        self.bind("<Button-1>", self._on_click)

    def _round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _draw(self, color):
        self.delete("all")
        self._round_rect(2, 2, self.width - 2, self.height - 2, self.radius,
                          fill=color, outline="")
        self.create_text(self.width / 2, self.height / 2, text=self.text,
                          fill=self.text_color, font=self.font)

    def _on_click(self, event):
        if self.command:
            self.command()
