import pdfkit
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# Evitar que a janela feche

options = Options()
options.add_experimental_option("detach", True)

# Evitar problemas de versões
navegador = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

navegador.get('https://portal.pucminas.br/biblioteca/index_padrao.php')
navegador.maximize_window()

# Pesquisar e confirmar
navegador.find_element(By.NAME, 'uquery').send_keys(
    "Livros de Teste de Software")
time.sleep(1)
navegador.find_element(
    By.XPATH, '//*[@id="searchformholdingsid"]/button').click()

# As informações que você está prestes a enviar não estão protegidas "Continuar mesmo assim"
navegador.switch_to.window(navegador.window_handles[-1])
navegador.find_element(By.XPATH, '//*[@id="proceed-button"]').click()
time.sleep(6)

# Captura dos nomes e referências

num_livros = 0
listaLivros = []

for i in range(5):

    time.sleep(5)
    
    # Número de livros encontrados
    listaDeLivros = navegador.find_elements(By.CLASS_NAME, 'result-list-li')
    num_livros += len(listaDeLivros)

    for livro in listaDeLivros:

        nome = livro.find_element(By.CLASS_NAME, 'title-link-wrapper').text
        referencia = livro.find_element(By.CLASS_NAME, 'standard-view-style').text
        # O campor correto para puxar apenas as referências não funciona corretamente, ou dessa forma ou puxar toda a div e salvar toda a informação de cada livro
        
        livro_Dicionario = {"nome": nome, "referencia": referencia}
        listaLivros.append(livro_Dicionario)

    # Passar de página
    if i < 4:

        time.sleep(2)
        proximaPagina = navegador.find_element(By.XPATH, '//*[@id="ctl00_ctl00_MainContentArea_MainContentArea_bottomMultiPage_lnkNext"]')
        proximaPagina.click()
        
    else:
        break

print("Foram identificados", num_livros, "livros\n")

for livro in listaLivros:
    print("Nome: ", livro["nome"].encode("utf-8"))
    print("Referência: ", livro["referencia"])
    print()

# Salvar 
# Criação do arquivo HTML

html = '<html><body>'
html += '<b>Número de livros encontrados: ' + str(num_livros) + '</b><br><br><br>'
for livro in listaLivros:
    html += '<p>Nome: ' + livro["nome"] + '</p>'
    html += '<p>Referência: ' + livro["referencia"] + '</p><br>'
html += '</body></html>'

# Aceitar caracteres especiais
options = {
    
    'encoding': 'UTF-8'
}

# Salvar como PDF
config = pdfkit.configuration(wkhtmltopdf=r'wkhtmltopdf\bin\wkhtmltopdf.exe')
pdfkit.from_string(html, 'lista_livros.pdf', configuration=config, options=options)

# Finaliza o navegador
navegador.quit()