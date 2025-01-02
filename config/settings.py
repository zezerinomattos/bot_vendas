# import os
from dotenv import load_dotenv
import chromedriver_autoinstaller

# Carregar variáveis do arquivo .env
load_dotenv()

# Instalar automaticamente a versão correta do ChromeDriver
chromedriver_autoinstaller.install()

# Configurações globais
GOOGLE_URL = "https://www.google.com"
WHATSAPP_URL = "https://web.whatsapp.com/"