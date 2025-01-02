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
            return driver
        except Exception as e:
            print(f"Erro ao abrir o WhatsApp Web: {e}")
            return None

    def wait_for_qr_code(self, driver):
        """Espera o QR Code carregar na tela"""
        try:
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
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="app"]/div/div[3]/div/div[3]/header/header')
                )
            )
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
        except Exception as e:
            print(f"Erro ao clicar no botão de novo chat: {e}")

    def enter_phone_number(self, driver, phone_number):
        """Insere o número de telefone no campo de input"""
        try:
            phone_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="x1n2onr6 xh8yej3 lexical-rich-text-input"]'
                     '//div[@role="textbox"]')
                )
            )
            phone_input.click()
            phone_input.send_keys(phone_number)
            time.sleep(1)  # Aguardar 1 segundo

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

            # Comparar os últimos 4 dígitos
            if phone_number[-4:] in contact_number:
                contact_div.click()  # Clica no contato
                return True  # Número processado com sucesso
            else:
                print(f"Número {phone_number[-4:]} não encontrado.")
                clear_input = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="app"]/div/div[3]/div/div[2]/'
                            'div[1]/span/div/span/div/div[1]/div[2]/'
                            'span/button/span')
                    )
                )
                clear_input.click()

                return False  # Número não encontrado

        except Exception as e:
            print(f"Erro ao digitar ou limpar o número de telefone: {e}")
            return False  # Número não encontrado

    def write_message(self,
                      driver,
                      message,
                      conversion=None,
                      audio=None,
                      img_media=None):
        """Escreve a mensagem no campo de mensagem e envia"""
        try:
            if message:
                try:
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
                        time.sleep(random.uniform(0.05, 0.2))  # Intervalo
                    print("Mensagem de saudação escrita com sucesso!")

                    # Re-localizar o botão de enviar e clicar
                    send_button = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable(
                            (By.XPATH,
                                "//button[@aria-label='Enviar'"
                                "and @data-tab='11']")
                        )
                    )
                    send_button.click()  # Clica no botão de envio
                    print("Mensagem de saudação enviada com sucesso!")

                except Exception as e:
                    print(f"Erro ao carregar a Saudação: {e}")
                    driver.quit()  # Fecha o navegador

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

            if audio:
                time.sleep(6)
                self.upload_file(driver, audio)

            if img_media:
                try:
                    time.sleep(6)
                    self.upload_file(driver, img_media)

                except Exception as e:
                    print(f"Erro ao carregar a imagem: {e}")
                    driver.quit()  # Fecha o navegador

        except Exception as e:
            print(f"Erro ao escrever ou enviar a mensagem: {e}")

    def upload_file(self, driver, file_path):
        """Faz o upload de um arquivo (áudio ou imagem)"""
        try:
            time.sleep(6)
            # Clicar no botão de anexar (ícone de "+")
            attach_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//span[@data-icon="plus"]')
                )
            )
            attach_button.click()
            time.sleep(1)

            # Localizar o input do tipo "file"
            file_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="app"]/div/span[5]/div/ul/'
                        'div/div/div[2]/li/div/input')
                )
            )

            # Enviar o caminho do arquivo para o input
            file_input.send_keys(file_path)
            time.sleep(2)

            # Localizar o botão de envio e clicar
            send_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                        '//*[@id="app"]/div/div[3]/div/div[2]/div[2]/span/div/'
                        'div/div/div[2]/div/div[2]/div[2]/div/div')
                )
            )
            send_button.click()
        except Exception as e:
            print(f"Erro ao carregar o arquivo: {e}")

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
            wait_time = 60

            for row in csvreader:
                phone_number = row[0]
                self.click_new_chat_button(driver)

                # Executar o bloco se o número for processado com sucesso
                if self.enter_phone_number(driver, phone_number):
                    try:
                        # Escrever a mensagem usando os dados fornecidos
                        greeting_message = self.message_data['greeting']
                        conversion_message = self.message_data['conversion']
                        audio_message = self.message_data['audio']
                        img_media = self.message_data['media']
                        self.write_message(
                            driver,
                            greeting_message,
                            conversion_message,
                            audio_message,
                            img_media
                        )
                        # time.sleep(60)
                        # Alternar o tempo de espera entre 60 e 120 segundos
                        time.sleep(wait_time)
                        wait_time = 120 if wait_time == 60 else 60  # Alternar
                    except Exception as e:
                        print(f"Erro ao processar: {phone_number}: {e}")
                        time.sleep(5)
                        continue  # Pular para o próximo número
                else:
                    print(f"Pulando o número: {phone_number}")

        driver.quit()