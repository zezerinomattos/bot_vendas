import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from services.whatsapp_message_service import WhatsAppMessageService


class WhatsAppPage:
    def __init__(self, root):
        self.root = root
        self.whatsapp_icon = None
        self.send_message_button = None

    def create_send_message_button(self):
        """Cria o botão de enviar mensagem"""
        self.send_message_button = tk.Button(
            self.root,
            text="Enviar mensagem",
            font=("Arial", 12),
            fg="#333333",
            bg="#f0f0f0", pady=10,
            relief="raised",
            width=200, height=200,
            compound="top",
            command=self.open_csv_popup
        )
        self.send_message_button.pack(pady=50)

        # Hover no botão de enviar mensagem
        self.send_message_button.bind("<Enter>",
                                      lambda event: self.on_hover(
                                          self.send_message_button))
        self.send_message_button.bind("<Leave>",
                                      lambda event: self.on_leave(
                                          self.send_message_button))

        # Ícone do WhatsApp
        self.load_whatsapp_icon()

    def load_whatsapp_icon(self):
        """Carrega o ícone do WhatsApp"""
        try:
            self.whatsapp_icon = Image.open("assets/whatsapp_icon.png")
            self.whatsapp_icon = self.whatsapp_icon.resize(
                (100, 100), Image.Resampling.LANCZOS)
            self.whatsapp_icon = ImageTk.PhotoImage(self.whatsapp_icon)
            self.send_message_button.config(image=self.whatsapp_icon)
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

    def on_hover(self, button):
        """Alterar estilo no hover"""
        button.config(bg="#C4D977", fg="#0D0D0D")

    def on_leave(self, button):
        """Restaurar estilo original"""
        button.config(bg="#f0f0f0", fg="#333333")

    def open_csv_popup(self):
        """Abre um popup para o formulário de envio"""
        popup = tk.Toplevel(self.root)
        popup.title("Enviar Mensagem")

        # Centralizar o popup
        popup_width = 500
        popup_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - popup_height / 2)
        position_right = int(screen_width / 2 - popup_width / 2)
        popup.geometry(
            f"{popup_width}x{popup_height}+{position_right}+{position_top}"
        )
        popup.configure(bg="#333333")

        # Campos de entrada
        csv_label = tk.Label(popup, text="Carregar contatos (Planilha):",
                             font=("Arial", 10), fg="#f0f0f0", bg="#333333")
        csv_label.pack(pady=10)

        def load_csv():
            selected_file = filedialog.askopenfilename(
                filetypes=[("CSV Files", "*.csv")])
            file_path.set(selected_file)
            print(f"Arquivo CSV selecionado: {selected_file}")
            validate_fields()

        file_path = tk.StringVar()
        csv_button = tk.Button(popup,
                               text="Selecionar Contatos", command=load_csv)
        csv_button.pack()

        greeting_label = tk.Label(popup,
                                  text="Mensagem de saudação:",
                                  font=("Arial", 10),
                                  fg="#f0f0f0",
                                  bg="#333333")
        greeting_label.pack(pady=10)
        greeting_entry = tk.Entry(popup, width=50)
        greeting_entry.pack()

        conversion_label = tk.Label(popup,
                                    text="Mensagem de conversão"
                                    "(formatação humana ou áudio):",
                                    font=("Arial", 10),
                                    fg="#f0f0f0",
                                    bg="#333333")
        conversion_label.pack(pady=10)
        conversion_text = tk.Text(popup, width=50, height=10)
        conversion_text.pack()

        # Opção para carregar áudio
        audio_label = tk.Label(popup, text="Carregar áudio (opcional):",
                               font=("Arial", 10), fg="#f0f0f0", bg="#333333")
        audio_label.pack(pady=10)

        def load_audio():
            selected_audio = filedialog.askopenfilename(
                filetypes=[("Audio Files", "*.mp3;*.wav;*.ogg")])
            audio_path.set(selected_audio)
            print(f"Arquivo de áudio selecionado: {selected_audio}")
            validate_fields()

        audio_path = tk.StringVar()
        audio_button = tk.Button(popup,
                                 text="Selecionar Áudio",
                                 command=load_audio)
        audio_button.pack()

        media_label = tk.Label(popup, text="Carregar mídia (foto/vídeo):",
                               font=("Arial", 10), fg="#f0f0f0", bg="#333333")
        media_label.pack(pady=10)

        def load_media():
            selected_media = filedialog.askopenfilename(
                filetypes=[("Media Files", "*.*")])
            media_path.set(selected_media)
            print(f"Arquivo de mídia selecionado: {selected_media}")
            validate_fields()

        media_path = tk.StringVar()
        media_button = tk.Button(popup,
                                 text="Selecionar Mídia",
                                 command=load_media)
        media_button.pack()

        # Validação dos campos
        def validate_fields():
            # Verifica se campos obrigatorios estão preenchidos
            if (file_path.get() and greeting_entry.get().strip() and
                    (conversion_text.get("1.0", tk.END).strip() or
                     audio_path.get()) and media_path.get()):
                send_button.config(state=tk.NORMAL)
            else:
                send_button.config(state=tk.DISABLED)

        # Botão de envio
        def send_data():
            # Coleta os dados dos campos
            data = {
                "csv_path": file_path.get(),
                "greeting": greeting_entry.get(),
                "conversion": conversion_text.get("1.0", tk.END).strip(),
                "media": media_path.get(),
                "audio": audio_path.get()
            }

            # Exibe os dados no terminal para depuração
            print("Dados coletados para envio:", data)

            # Envia os dados para o WhatsAppMessageService
            whatsapp_service = WhatsAppMessageService(data)
            whatsapp_service.send_message()

            # Fecha o popup após enviar os dados
            popup.destroy()

        send_button = tk.Button(popup, text="Enviar", state=tk.DISABLED,
                                command=send_data)
        send_button.pack(pady=20)

        # Botão de fechar
        close_button = tk.Button(popup, text="Fechar", command=popup.destroy)
        close_button.pack(pady=10)

        popup.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("WhatsApp Page")
    root.geometry("400x400")

    whatsapp_page = WhatsAppPage(root)
    whatsapp_page.create_send_message_button()

    root.mainloop()
