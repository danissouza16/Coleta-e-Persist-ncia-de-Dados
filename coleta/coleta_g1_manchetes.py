from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json
import time
import ssl

# Certifique-se de que o módulo SSL está habilitado no ambiente
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass


service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)


def send_to_discord(webhook_url, message):
    """Função para enviar mensagem para um webhook do Discord."""
    payload = {"content": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    return response.status_code

def save_to_crudcrud(api_url, data):
    """Função para salvar dados no site CRUDCRUD."""
    response = requests.post(api_url, json=data)
    return response.status_code

try:

    browser.get("https://www.amazon.com.br/")
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))


    search_box = browser.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys("notebook")
    search_box.send_keys(Keys.RETURN)


    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a-link-normal s-line-clamp-4 s-link-style a-text-normal")))
    products = browser.find_elements(By.CSS_SELECTOR, "a-link-normal s-line-clamp-4 s-link-style a-text-normal")

    if not products:
        raise Exception("Nenhum produto encontrado na pesquisa.")

    first_product = products[0]

    product_name_element = first_product.find_element(By.CSS_SELECTOR, "h2 a span")
    product_link_element = first_product.find_element(By.CSS_SELECTOR, "h2 a")

    product_name = product_name_element.text
    product_link = product_link_element.get_attribute("href")

    print(f"Produto encontrado: {product_name}")
    print(f"Link do produto: {product_link}")


    product_link_element.click()
    browser.switch_to.window(browser.window_handles[1])


    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "productTitle")))
    product_title = browser.find_element(By.ID, "productTitle").text

    try:
        product_price = browser.find_element(By.CSS_SELECTOR, ".a-price span.a-offscreen").text
    except:
        product_price = "Preço não disponível"

    print(f"Título do produto: {product_title}")
    print(f"Preço do produto: {product_price}")


    discord_webhook_url = "https://discord.com/api/webhooks/1318447832176267265/_Xoqts4mPXjSn9u5YHqUOaQVUMX3uKp3ffrhfmXWvSLOXKCrytmoZb4_Z670iAM6wt-0"  # Substituir pelo webhook real
    discord_message = f"Produto: {product_title}\nPreço: {product_price}\nLink: {product_link}"
    discord_status = send_to_discord(discord_webhook_url, discord_message)
    print(f"Mensagem enviada ao Discord: {discord_status == 204}")


    crudcrud_api_url = "https://crudcrud.com/api/1b236bb8dba741b48a01b39b7a9ee984"  
    product_data = {
        "title": product_title,
        "price": product_price,
        "link": product_link
    }
    crudcrud_status = save_to_crudcrud(crudcrud_api_url, product_data)
    print(f"Dados salvos no CRUDCRUD: {crudcrud_status == 201}")

except Exception as e:
    print(f"Erro encontrado: {e}")

finally:
    time.sleep(5) 
    browser.quit()
