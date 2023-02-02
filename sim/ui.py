"""
Contains methods and classes to run the simulation using a tkinter ui.
"""
import tkinter as tk


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()


def main() -> None:
    app: tk.Tk = App()
    app.mainloop()


if __name__ == "main":
    main()
