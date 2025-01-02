import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from dotenv import load_dotenv
from config.settings import WHATSAPP_URL
import time
import random

# Carregar variáveis do arquivo .env
load_dotenv()


class WhatsAppMessageService:
    def __init__(self, message_data):
        self.message_data = message_data

    def open_whatsapp_web(self):
        """Abre o WhatsApp Web no navegador"""
        chromedriver_autoinstaller.install()

        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)

        try:
            driver.get(WHATSAPP_URL)
            print("Acessando o WhatsApp Web...")
            return driver
        except Exception as e:
            print(f"Erro ao abrir o WhatsApp Web: {e}")
            return None

    def wait_for_qr_code(self, driver):
        """Espera o QR Code carregar na tela"""
        try:
            print("Aguardando o QR Code aparecer...")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="app"]/div/div[2]/div[2]/div[1]/div/div/'
                     'div[2]/div[2]/div[1]/canvas')
                )
            )
            print("QR Code detectado!")
        except Exception as e:
            print(f"Erro ao esperar o QR Code: {e}")

    def wait_for_chat_list(self, driver):
        """Espera a barra de conversas carregar na tela"""
        try:
            print("Aguardando a barra de conversas aparecer...")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="app"]/div/div[3]/div/div[3]/header/header')
                )
            )
            print("Barra de conversas detectada!")
        except Exception as e:
            print(f"Erro ao esperar a barra de conversas: {e}")

    def click_new_chat_button(self, driver):
        """Clica no botão para iniciar um novo chat"""
        try:
            time.sleep(1)
            print("Procurando o botão de novo chat...")
            new_chat_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '[data-icon="new-chat-outline"]'))
            )
            new_chat_button.click()
            print("Botão de novo chat clicado!")
        except Exception as e:
            print(f"Erro ao clicar no botão de novo chat: {e}")

    def enter_phone_number(self, driver, phone_number):
        """Insere o número de telefone no campo de input"""
        try:
            print(f"Digitando o número de telefone: {phone_number}")
            phone_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="x1n2onr6 xh8yej3 lexical-rich-text-input"]'
                     '//div[@role="textbox"]')
                )
            )
            phone_input.click()
            phone_input.send_keys(phone_number)
            print("Número de telefone digitado!")
            time.sleep(1)  # Aguardar 1 segundo

            print("Aqui dentro vai ser a sequência do código.")

            # Esperar o contato aparecer após digitar o número
            time.sleep(2)  # Aguardar que o contato apareça

            # Localizar a div do contato e comparar os últimos 4 dígitos
            contact_div = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "_ak8q")
                )
            )

            # Obter o título (número de telefone) da div
            contact_number = contact_div.find_element(
                By.TAG_NAME, "span").get_attribute("title")
            print(f"Contato encontrado: {contact_number}")

            # Comparar os últimos 4 dígitos
            if phone_number[-4:] in contact_number:
                contact_div.click()  # Clica no contato
            else:
                print(f"Número {phone_number[-4:]} não encontrado.")

        except Exception as e:
            print(f"Erro ao digitar ou limpar o número de telefone: {e}")

    def write_message(self,
                      driver,
                      message,
                      conversion=None,
                      audio=None,
                      img_media=None):
        """Escreve a mensagem no campo de mensagem e envia"""
        try:
            print(f"Escrevendo a mensagem: {message}")
            time.sleep(3)
            
            # Re-localizar o campo de mensagem
            message_field = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="main"]/footer/div[1]/div/span/'
                     'div/div[2]/div[1]/div[2]/div[1]/p')
                )
            )

            message_field.click()  # Clicar no campo de mensagem

            # Digitar a mensagem lentamente (greeting)
            for char in message:
                message_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.2))  # Intervalo aleatório
            print("Mensagem de saudação escrita com sucesso!")

            # Re-localizar o botão de enviar e clicar
            send_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//button[@aria-label='Enviar' and @data-tab='11']")
                )
            )
            send_button.click()  # Clica no botão de envio
            print("Mensagem de saudação enviada com sucesso!")

            # Verificar se existe mensagem em conversion
            if conversion:
                time.sleep(6)

                # Re-localizar o campo de mensagem
                message_field = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         '//*[@id="main"]/footer/div[1]/div/span/'
                         'div/div[2]/div[1]/div[2]/div[1]/p')
                    )
                )

                message_field.click()

                # Digitar a mensagem de conversão lentamente
                for char in conversion:
                    message_field.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.2))

                print("Mensagem de conversão escrita com sucesso!")

                # Re-localizar o botão de enviar e clicar novamente
                send_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                         "//button[@aria-label='Enviar' and @data-tab='11']")
                    )
                )
                send_button.click()

            else:
                print("Nenhuma mensagem de conversão encontrada.")

            # Verificar se existe áudio em audio
            if audio:
                try:
                    time.sleep(6)
                    # clicar no primeiro botão (SVG com data-icon="plus")
                    first_button = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//span[@data-icon="plus"]'))
                    )
                    first_button.click()
                    print("Primeiro botão clicado com sucesso!")
                    time.sleep(1)

                    # Localizar o input do tipo file
                    print("Tentando localizar o input do tipo 'file'...")
                    file_input = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                             '//*[@id="app"]/div/span[5]/div/ul/'
                             'div/div/div[2]/li/div/input'))
                    )
                    print("Input localizado com sucesso!")

                    # Enviar o caminho do arquivo para o input
                    print("Enviando o arquivo para upload...")
                    file_input.send_keys(audio)
                    print("Arquivo enviado com sucesso!")
                    time.sleep(2)

                    file_input = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                             '//*[@id="app"]/div/div[3]/div/div[2]/div[2]/'
                             'span/div/div/div/div[2]/div/div[2]/div[2]/'
                             'div/div'))
                    )
                    file_input.click()  # Clica no botão de envio

                except Exception as e:
                    print(f"Erro ao clicar nos botões: {e}")
            else:
                print("Nenhum arquivo de áudio foi fornecido.")

            # Verificar se existe imagem em img_media
            if img_media:
                try:
                    # Localizar o input do tipo file para imagens
                    time.sleep(6)
                    # clicar no primeiro botão (SVG com data-icon="plus")
                    first_button = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//span[@data-icon="plus"]'))
                    )
                    first_button.click()
                    print("Primeiro botão clicado com sucesso!")
                    time.sleep(1)

                    # Localizar o input do tipo file
                    print("Tentando localizar o input do tipo 'file'...")
                    file_input = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="app"]/div/span[5]/div/ul/'
                             'div/div/div[2]/li/div/input'))
                    )
                    print("Input localizado com sucesso!")

                    # Enviar o caminho do arquivo para o input
                    print("Enviando o arquivo para upload...")
                    file_input.send_keys(img_media)
                    print("Arquivo enviado com sucesso!")
                    time.sleep(2)

                    file_input = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                             '//*[@id="app"]/div/div[3]/div/div[2]/div[2]/'
                             'span/div/div/div/div[2]/div/div[2]/div[2]/'
                             'div/div'))
                    )
                    file_input.click()  # Clica no botão de envio

                except Exception as e:
                    print(f"Erro ao carregar a imagem: {e}")
                    driver.quit()  # Fecha o navegador

        except Exception as e:
            print(f"Erro ao escrever ou enviar a mensagem: {e}")

    def send_message(self):
        """Envio de mensagem para o WhatsApp"""
        driver = self.open_whatsapp_web()
        if not driver:
            return

        self.wait_for_qr_code(driver)
        self.wait_for_chat_list(driver)
        self.click_new_chat_button(driver)

        csv_path = self.message_data['csv_path']
        
        if not os.path.exists(csv_path):
            print(f"Erro: O arquivo CSV não foi encontrado {csv_path}")
            return

        with open(csv_path, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Ignorar cabeçalho

            for row in csvreader:
                phone_number = row[0]
                self.click_new_chat_button(driver)
                self.enter_phone_number(driver, phone_number)

                # Escrever a mensagem usando o dado de saudação
                greeting_message = self.message_data['greeting']
                conversion_message = self.message_data['conversion']
                audio_message = self.message_data['audio']
                img_media = self.message_data['media']
                self.write_message(driver,
                                   greeting_message,
                                   conversion_message,
                                   audio_message,
                                   img_media)

                print(f"Mensagem enviada para o número: {phone_number}")
                time.sleep(60)

        driver.quit()
