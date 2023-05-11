import requests
from bs4 import BeautifulSoup
import pyshorteners
import os


encurtar = 1
paginas_para_pesquisar = 3


shortner = pyshorteners.Shortener()
while True:
    desde = 1
    numeracao = 1
    all_prices = []
    print('\n')
    for x in range(paginas_para_pesquisar+1):
        url = r'https://lista.mercadolivre.com.br/celulares-telefones/smartwatches-acessorios/smartwatches/samsung/novo/galaxy-watch-4_Desde_' + \
            str(desde)+r'_OrderId_PRICE_PriceRange_500-1200_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondi%C3%A7%C3%A3o%26applied_filter_order%3D5%26applied_value_id%3D2230284%26applied_value_name%3DNovo%26applied_value_order%3D1%26applied_value_results%3D141%26is_custom%3Dfalse'
        page = requests.get(url)

        # Utilize o módulo BeautifulSoup para parsear o conteúdo da página
        soup = BeautifulSoup(page.content, 'html.parser')

        # Encontre todas as tags HTML
        a_tags = soup.find_all('div', {'class': 'andes-card'})

        product_tags = soup.find_all(
            'div', {'class': 'ui-search-result__content-wrapper shops__result-content-wrapper'})

        link_tags = [product_tag.find(
            'a', {'class': 'ui-search-item__group__element shops__items-group-details ui-search-link'}) for product_tag in product_tags]
        title_tags = [product_tag.find(
            'h2', {'class': 'ui-search-item__title shops__item-title'}) for product_tag in product_tags]
        price_tags = [product_tag.find(
            'span', {'class': 'price-tag-fraction'}) for product_tag in product_tags]

        links = [str(i+10) + ' - ' + link_tag['href']
                 for i, link_tag in enumerate(link_tags)]
        titles = [str(i+10) + ' - ' + title_tag.text for i,
                  title_tag in enumerate(title_tags)]
        prices = [str(i+10) + ' - ' + price_tag.text for i,
                  price_tag in enumerate(price_tags)]

        new_links = []
        new_prices = []
        for title in titles:
            new_prices.append(
                tuple(item for item in prices if item.lower().startswith(title[0:3])))
            new_links.append(
                tuple(item for item in links if item.lower().startswith(title[0:3])))

        for i in range(len(titles)):
            formated_title = str(titles[i])
            print(str(numeracao) + ' - ' + formated_title[5:])

            formated_price = str(new_prices[i])
            os.system('color')
            print(str(numeracao) + ' - \033[2;30;46m' +
                  formated_price[7:-3] + '\033[0;0m')
            all_prices.append(int(formated_price[7:-3].replace('.', '')))

            formated_link = str(new_links[i])
            if encurtar == 1:
                print(str(numeracao) + ' - ' +
                      shortner.tinyurl.short(formated_link[7:-3]))
            else:
                print(str(numeracao) + ' - ' + formated_link[7:-3])

            numeracao += 1
            print('\n')

        desde += 48

    all_prices.sort()
    print(all_prices)
    wait = input("\nPressione Enter para continuar...")
