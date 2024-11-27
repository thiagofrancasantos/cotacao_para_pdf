from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from reportlab.pdfgen import canvas
import time

# Função para capturar a cotação
def capturar_cotacao():
    # Configurar o Selenium para usar o Firefox
    service = Service('./geckodriver.exe', log_output='geckodriver.log')  # Usando log_output em vez de log_path
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')  # Executar sem abrir o navegador
    options.add_argument('--no-sandbox')
    driver = webdriver.Firefox(service=service, options=options)

    # Acessar o site de cotação
    url = "https://www.google.com/search?q=cotação+dólar"
    driver.get(url)
    time.sleep(2)  # Aguardar carregamento da página

    # Capturar o valor da cotação
    try:
        elemento_cotacao = driver.find_element(By.XPATH, "//span[contains(@class, 'DFlfde')]")
        cotacao = elemento_cotacao.text
    except Exception as e:
        print("Erro ao capturar cotação:", e)
        cotacao = None
    finally:
        driver.quit()  # Garantir que o navegador seja fechado

    return cotacao

# Função para gerar o PDF
def gerar_pdf(cotacao):
    nome_arquivo = "cotacao_dolar.pdf"
    c = canvas.Canvas(nome_arquivo)
    c.drawString(100, 750, "Relatório de Cotação do Dólar")
    c.drawString(100, 700, f"Cotação atual do dólar: {cotacao}")
    c.drawString(100, 650, f"Data: {time.strftime('%d/%m/%Y %H:%M:%S')}")
    c.save()
    print(f"Relatório salvo como: {nome_arquivo}")

# Fluxo principal
if __name__ == "__main__":
    cotacao_dolar = capturar_cotacao()
    if cotacao_dolar:
        print(f"Cotação capturada: {cotacao_dolar}")
        gerar_pdf(cotacao_dolar)
    else:
        print("Não foi possível capturar a cotação.")
