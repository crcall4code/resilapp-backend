from lxml import html
import requests


def imn():
    page = requests.get(
        'https://www.imn.ac.cr/web/imn/avisos-meteorologicos/-/asset_publisher/jUexp4gzJzdk/content/id/475880')
    tree = html.fromstring(page.content)
    WeatherNews = tree.xpath('//div[@class="col-sm-9"]//h4//text()')
    WeatherNewsDateTime = tree.xpath('//div[@class="col-sm-9"]//h6//text()')
    counter = 0
    for news in WeatherNews:
        local_news = dict(
            Aviso = news,
            Fecha = WeatherNewsDateTime[counter],
            Hora = WeatherNewsDateTime[counter+1]
        )
        counter+=2
        print(local_news)


def lis():
    page = requests.get('http://www.lis.ucr.ac.cr/')
    tree = html.fromstring(page.content)
    sismos = tree.xpath('//html//body//div[1]//section//div//div[2]//table//tbody//text()')
    length_sismos = len(sismos)
    elements_sismos = int(length_sismos / 9)
    for x in range(elements_sismos):
        local_quake_data = []
        for y in range(9):
            local_quake_data.append(sismos.pop())
        sismo_data = dict(
            Localidad=local_quake_data[0],
            Magnitud=local_quake_data[2],
            Longitud=local_quake_data[4],
            Latitud=local_quake_data[5],
            Hora_local=local_quake_data[7]
        )
        print(sismo_data)


if __name__ == '__main__':
    print("SISMOLOGICO")
    lis()
    print("***********************")
    print("METEOROLOGICO")
    imn()
