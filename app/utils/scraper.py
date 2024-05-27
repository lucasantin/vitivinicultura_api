import requests
from bs4 import BeautifulSoup
from flasgger import swag_from

def fetch_data(url):
    """
    Faz uma requisição HTTP GET para a URL especificada e retorna os dados processados.

    Parâmetros:
    url (str): A URL para a qual a requisição será feita.

    Retorna:
    dict: Um dicionário contendo os dados extraídos da página HTML se a requisição for bem-sucedida.
    None: Se a requisição não for bem-sucedida.

    Exemplos:
    >>> fetch_data('http://exemplo.com/dados')
    {'headers': ['Coluna1', 'Coluna2'], 'rows': [['Dado1', 'Dado2'], ['Dado3', 'Dado4']]}
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        data = parse_html(soup)
        return data
    else:
        return None

def parse_html(soup):
    """
    Analisa o HTML da página e extrai dados de uma tabela específica.

    Parâmetros:
    soup (BeautifulSoup): O objeto BeautifulSoup que representa a página HTML.

    Retorna:
    dict: Um dicionário contendo os cabeçalhos da tabela e as linhas de dados.
    {"error": "No table found"}: Se a tabela especificada não for encontrada no HTML.

    Exemplos:
    >>> html = '<table class="tb_base tb_dados"><tr><th>Coluna1</th><th>Coluna2</th></tr><tr><td>Dado1</td><td>Dado2</td></tr></table>'
    >>> soup = BeautifulSoup(html, 'html.parser')
    >>> parse_html(soup)
    {'headers': ['Coluna1', 'Coluna2'], 'rows': [['Dado1', 'Dado2']]}
    """
    table = soup.find('table', class_='tb_base tb_dados')  # Ajuste conforme a estrutura do HTML

    if not table:
        return {"error": "No table found"}

    headers = [header.text.strip() for header in table.find_all('th')]
    rows = []
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if cells:
            row_data = [cell.text.strip() for cell in cells]
            rows.append(row_data)

    data = {
        "headers": headers,
        "rows": rows
    }
    return data
