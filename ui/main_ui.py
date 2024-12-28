import tkinter as tk
from pages.google_page import GooglePage


class MainUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot de Vendas")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg="#333333")  # Fundo escuro

        # Título
        self.title_label = tk.Label(self.root, text="Bot de Vendas",
                                    font=("Arial", 16), 
                                    fg="#f0f0f0", bg="#333333")
        self.title_label.pack(pady=20)

        # Página de pesquisa do Google
        self.google_page = GooglePage(self.root)
        self.google_page.create_search_button()


# Main execução do app
if __name__ == "__main__":
    root = tk.Tk()
    app = MainUI(root)
    root.mainloop()
