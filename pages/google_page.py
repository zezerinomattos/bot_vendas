import tkinter as tk
from services.google_search_service import GoogleSearchService


class GooglePage:
    def __init__(self, root):
        self.root = root
        self.google_icon = None
        self.search_button = None

    def create_search_button(self):
        """Cria o botão de busca"""
        self.search_button = tk.Button(self.root, text="Buscar no Google",
                                       font=("Arial", 12), fg="#333333",
                                       bg="#f0f0f0", pady=10,
                                       command=self.show_search_popup,
                                       relief="raised", width=200,
                                       height=200, compound="top")
        self.search_button.pack(pady=50)

        # Hover no botão de busca
        self.search_button.bind("<Enter>",
                                lambda event:
                                self.on_hover(self.search_button))
        self.search_button.bind("<Leave>",
                                lambda event:
                                self.on_leave(self.search_button))

        # Ícone do Google
        self.load_google_icon()

    def load_google_icon(self):
        """Carrega o ícone do Google"""
        try:
            from PIL import Image, ImageTk
            self.google_icon = Image.open("assets/google_icon.png")
            self.google_icon = self.google_icon.resize(
                (100, 100), Image.Resampling.LANCZOS)  # Redimensiona a imagem
            self.google_icon = ImageTk.PhotoImage(self.google_icon)

            # Coloca o ícone dentro do botão
            self.search_button.config(image=self.google_icon)
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

    def on_hover(self, button):
        """Alterar estilo no hover"""
        button.config(bg="#C4D977", fg="#0D0D0D")

    def on_leave(self, button):
        """Restaurar estilo original"""
        button.config(bg="#f0f0f0", fg="#333333")

    def show_search_popup(self):
        """Exibe o popup para inserir o nicho e cidade"""
        def on_input_change(*args):
            # Habilita o botão "OK" se o campo não estiver vazio
            if user_input.get().strip() != "":
                search_button.config(state=tk.NORMAL, 
                                     bg="#C4D977", fg="#0D0D0D")
            else:
                search_button.config(state=tk.DISABLED, bg="#f0f0f0")

        user_input = tk.StringVar()

        # Popup customizado
        popup = tk.Toplevel(self.root)
        popup.title("Buscar no Google")
        
        # Obter as dimensões da tela principal
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Definir as dimensões do popup
        popup_width = 550
        popup_height = 200
        
        # Calcular a posição do popup para centralizar na tela
        position_top = int(screen_height / 2 - popup_height / 2)
        position_right = int(screen_width / 2 - popup_width / 2)
        
        popup.geometry(
            f'{popup_width}x{popup_height}+{position_right}+{position_top}')
        popup.configure(bg="#333333")

        # Label e campo de entrada
        label = tk.Label(popup,
                         text="Insira o nicho e cidade para pesquisa"
                         "(ex: Cabeleireiro em Sapiranga, RS):",
                         font=("Arial", 12), fg="#f0f0f0", bg="#333333")
        label.pack(pady=10)

        input_entry = tk.Entry(popup, textvariable=user_input,
                               font=("Arial", 12), width=30)
        input_entry.pack(pady=10)
        
        # Botão "OK"
        search_button = tk.Button(popup,
                                  text="PESQUISAR",
                                  font=("Arial", 12),
                                  fg="#333333",
                                  bg="#f0f0f0",
                                  command=lambda:
                                  self.activate_search_button(user_input.get())
                                  or popup.destroy(), state=tk.DISABLED)
        search_button.pack(pady=10)

        # Atualiza o estado do botão "OK" conforme o campo de entrada
        user_input.trace("w", on_input_change)

        # Fecha o popup
        def on_close():
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)

    def activate_search_button(self, search_query):
        """Chama a automação para realizar a busca no Google"""
        search_service = GoogleSearchService(search_query)
        search_service.search_on_google()
