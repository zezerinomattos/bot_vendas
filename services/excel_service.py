import csv
import os


class ExcelService:
    @staticmethod
    def save_phone_numbers_to_csv(phone_numbers, 
                                  file_name="phone_numbers.csv"):
        """Salva os números de telefone extraídos em um arquivo CSV."""
        
        # Obtém o caminho da pasta de Downloads no sistema operacional
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # Define o caminho completo para salvar o arquivo CSV
        file_path = os.path.join(downloads_folder, file_name)

        # Cria ou abre o arquivo CSV para escrever os números de telefone
        with open(file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            
            # Se o arquivo estiver vazio, escreve o cabeçalho
            if file.tell() == 0:
                writer.writerow(["Phone Number"])

            # Escreve cada número de telefone no arquivo CSV
            for number in phone_numbers:
                writer.writerow([number])
        
        print(f"Números de telefone salvos em: {file_path}")
