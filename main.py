from ui.main_ui import MainUI
import tkinter as tk


def main():
    """Ponto de entrada principal do aplicativo."""
    root = tk.Tk()
    app = MainUI(root)  # noqa: F841
    root.mainloop()


if __name__ == "__main__":
    main()
