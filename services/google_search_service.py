from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
import time
from services.excel_service import ExcelService
from config.settings import GOOGLE_URL


class GoogleSearchService:
    def __init__(self, search_query):
        self.search_query = search_query

    def search_on_google(self):
        # Instala automaticamente o ChromeDriver compatível
        chromedriver_autoinstaller.install()

        # Configuração do WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Inicia o driver do Chrome
        driver = webdriver.Chrome(options=options)
        
        try:
            # Acessa o Google
            driver.get(GOOGLE_URL)
            
            # Encontra a barra de pesquisa e digita a query
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(self.search_query)
            search_box.send_keys(Keys.RETURN)
            
            # Aguarda o carregamento da página
            driver.implicitly_wait(5)

            # Clica no botão "Mais empresas"
            more_companies_button = driver.find_element(
                By.XPATH, "//span[contains(text(),'Mais')]")
            more_companies_button.click()
            
            print(f"Buscando no Google: {self.search_query}")
            
            # Lista para armazenar todos os números encontrados
            all_phone_numbers = []

            while True:
                # Ajusta o tempo de espera para elementos dinâmicos
                driver.implicitly_wait(10)

                try:
                    # Verifica qual container está disponível
                    if driver.find_elements(By.CLASS_NAME, "ykYNg"):
                        div_list_container = driver.find_element(
                            By.CLASS_NAME, "ykYNg")
                        
                        # Lógica para a classe "ykYNg"
                        div_list_items = div_list_container.find_elements(
                            By.CSS_SELECTOR, "div[role='listitem']")
                        
                        for div_item in div_list_items:
                            raw_text = div_item.text
                            phone_numbers = self.extract_phone_numbers(
                                raw_text)
                            all_phone_numbers.extend(phone_numbers)
                            time.sleep(3)
                        
                        # Verifica e clica no botão "Próxima"
                        try:
                            next_button = driver.find_element(
                                By.XPATH,
                                "//button[@aria-label='Próxima'"
                                "and contains(@class, 'VfPpkd-LgbsSe')]"
                            )
                            next_button.click()
                            print("Botão 'Próxima' clicado.")
                            time.sleep(15)
                        except Exception:
                            print("Botão 'Próxima' não encontrado.")
                            break

                    elif driver.find_elements(By.CLASS_NAME, "rlfl__tls"):
                        div_list_container = driver.find_element(
                            By.CLASS_NAME, "rlfl__tls")
                        
                        # Lógica para a classe "VkpGBb"
                        div_list_items = div_list_container.find_elements(
                            By.CSS_SELECTOR, "div.VkpGBb")
                        
                        for div_item in div_list_items:
                            raw_text = div_item.text
                            phone_numbers = self.extract_phone_numbers(
                                raw_text)
                            all_phone_numbers.extend(phone_numbers)
                            time.sleep(3)
                        
                        # Verifica e clica no botão "Mais" para o cenário
                        try:
                            next_button = driver.find_element(By.ID, "pnnext")
                            next_button.click()
                            print("Botão 'Mais' clicado.")
                            time.sleep(15)
                        except Exception:
                            print("Botão 'Mais' não encontrado.")
                            break
                    else:
                        print("Nenhuma classe conhecida encontrada.")
                        break
                except Exception as e:
                    print(f"Erro ao processar elementos: {e}")
                    break

            # Após a busca, salva os números de telefone no CSV
            if all_phone_numbers:
                ExcelService.save_phone_numbers_to_csv(all_phone_numbers)

        except Exception as e:
            print(f"Erro durante a automação: {e}")
        # finally:
        #     driver.quit()

    @staticmethod
    def extract_phone_numbers(text):
        """Extrai números de telefone do texto formatados como desejado."""
        import re

        # Regex para capturar números de telefone no formato
        phone_pattern = r"\(\d{2}\)\s?\d{4,5}-?\d{4}"
        matches = re.findall(phone_pattern, text)
        
        # Formata os números encontrados para o formato desejado
        formatted_numbers = [
            match.replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
            for match in matches
        ]
      
        return formatted_numbers
