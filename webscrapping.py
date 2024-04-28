from parsel import Selector
import cloudscraper
import json
import pandas as pd

scraper = cloudscraper.create_scraper()

data_to_save = []  # Lista para armazenar os dados

for i in range(1, 500):
    #r = scraper.get(f'https://www.olx.com.br/estado-rj?q=imoveis?{i}')
    #r = scraper.get(f'https://www.olx.com.br/estado-rj?q=imoveis%20rj{i}')
    #r = scraper.get(f'https://www.olx.com.br/estado-rj/rio-de-janeiro-e-regiao?q=imoveis%20rj{i}')
    r = scraper.get(f'https://www.olx.com.br/estado-rj/rio-de-janeiro-e-regiao?q=imoveis{i}')
    response = Selector(text=r.text)
    html = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').get())
    houses = html.get('props').get('pageProps').get('ads')

    for house in houses:
        # Acessando 'locationDetails' e obtendo o valor do bairro ('neighbourhood') e o valor do município('municipality')
        neighbourhood = house.get('locationDetails', {}).get('neighbourhood')
        municipality = house.get('locationDetails', {}).get('municipality')
        # Acessando a lista de propriedades
        properties = house.get('properties', [])

        # Inicializando as variáveis para armazenar os valores de 'rooms' e 'bathrooms'
        rooms = None
        bathrooms = None

        # Iterando sobre as propriedades para encontrar os valores de 'rooms' e 'bathrooms'
        for prop in properties:
            if prop.get('name') == 'rooms':
                rooms = prop.get('value')
            elif prop.get('name') == 'bathrooms':
                bathrooms = prop.get('value')

        data_to_save.append({
            'title': house.get('title'),
            'price': house.get('price'),
            'locations': house.get('locations'),
            'neighbourhood': neighbourhood, 
            'municipality':municipality,
            'category': house.get('category'),
            'rooms': rooms,
            'bathrooms': bathrooms
        })

# Criar DataFrame do Pandas
df = pd.DataFrame(data_to_save)

# Salvar o DataFrame em um arquivo xlsx
df.to_excel('dados_olx.xlsx', index=False)
print("Dados salvos com sucesso no arquivo 'dados_olx.xlsx'")
