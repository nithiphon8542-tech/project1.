# -*- coding: utf-8 -*-
"""
main.py
จุดเริ่มต้นของโปรแกรม รันไฟล์นี้เพื่อเปิดแอป (python main.py)

โครงสร้างโปรเจกต์:
main.py
scr/
  gamepkg/
    __init__.py
    theme.py     -> สี/ฟอนต์กลาง
    widgets.py   -> ปุ่มโค้งมนสวย ๆ
    menu.py      -> หน้าเมนูเลือกเกม
    game1.py     -> เกม Snake
    game2.py     -> เกม Breakout
"""
import sys
import os
import tkinter as tk


def _find_project_root(start_path):
    """
    ไต่ขึ้นไปทีละโฟลเดอร์จากตำแหน่งไฟล์นี้ จนกว่าจะเจอโฟลเดอร์ที่มี scr/gamepkg อยู่
    ทำแบบนี้เพื่อให้ main.py รันได้ถูกต้อง ไม่ว่าจะถูกวางไว้ที่ root
    หรือถูกย้ายไปไว้ในโฟลเดอร์ย่อย (เช่น test/) ก็ตาม
    """
    current = start_path
    for _ in range(6):  # กันลูปไม่รู้จบ ไต่ขึ้นไปสูงสุด 6 ระดับ
        if os.path.isdir(os.path.join(current, "scr", "gamepkg")):
            return current
        parent = os.path.dirname(current)
        if parent == current:  # ถึงรากไดรฟ์แล้ว หาไม่เจอจริง ๆ
            break
        current = parent
    return start_path  # หาไม่เจอ ก็ใช้ตำแหน่งเดิมไปก่อน (จะ error ให้เห็นชัดเจน)


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = _find_project_root(THIS_DIR)

# ให้ import แพ็กเกจ scr.gamepkg ได้ไม่ว่า main.py จะถูกรันจากที่ไหน
sys.path.insert(0, PROJECT_ROOT)

try:
    from scr.gamepkg import theme
except ModuleNotFoundError as e:
    print("=" * 60)
    print("หา package 'scr.gamepkg' ไม่เจอ")
    print(f"ไฟล์ main.py อยู่ที่: {THIS_DIR}")
    print(f"ค้นหา project root ได้ที่: {PROJECT_ROOT}")
    print("ตรวจสอบว่ามีโฟลเดอร์ scr/gamepkg วางอยู่ในระดับที่ถูกต้องหรือไม่")
    print("=" * 60)
    raise e

from scr.gamepkg.menu import MainMenu
from scr.gamepkg.game1 import SnakeGame
from scr.gamepkg.game2 import BreakoutGame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Center - Python GUI")
        self.geometry(f"{theme.WINDOW_W}x{theme.WINDOW_H}")
        self.configure(bg=theme.BG_DARK)
        self.minsize(theme.WINDOW_W, theme.WINDOW_H)

        self.current_frame = None
        self.show_menu()

    def _clear_current(self):
        if self.current_frame is not None:
            # หยุด game loop / key binding เก่าก่อนสลับหน้าจอ
            if hasattr(self.current_frame, "on_leave"):
                self.current_frame.on_leave()
            self.unbind_all("<Key>")
            self.unbind_all("<Left>")
            self.unbind_all("<Right>")
            self.unbind_all("<space>")
            self.current_frame.destroy()

    def show_menu(self):
        self._clear_current()
        self.current_frame = MainMenu(self, self.show_game1, self.show_game2)
        self.current_frame.pack(fill="both", expand=True)

    def show_game1(self):
        self._clear_current()
        self.current_frame = SnakeGame(self, self.show_menu)
        self.current_frame.pack(fill="both", expand=True)

    def show_game2(self):
        self._clear_current()
        self.current_frame = BreakoutGame(self, self.show_menu)
        self.current_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()