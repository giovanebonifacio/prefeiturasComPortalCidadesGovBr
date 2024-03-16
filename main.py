from urllib.request import urlopen
import csv

#CONSTANTES
SIGLA_ESTADO_COLUMN = 4
NOME_MUNICIPIO_COLUMN = 2
# URL_PADRAO = "http://www.maringa.pr.gov.br"


def existePortalPrefeituraParaUrl(url):
    try:
        response = urlopen(url)
        if response.code != 200:
            return False

        print("chamada ok")
        html_bytes = response.read()
        html = html_bytes.decode("utf-8")

        return htmlRepresentaPortalPrefeitura(html)
    except Exception:
        return False

def htmlRepresentaPortalPrefeitura(html):
    if 'prefeitura' in html.lower():
        return True
    else:
        return False

def trataCaracteresEspeciais(nome):
    nome = nome.lower()
    nome = nome.replace('ã','a')
    nome = nome.replace('á','a')
    nome = nome.replace('à','a')
    nome = nome.replace('â','a')
    nome = nome.replace('ã','a')
    nome = nome.replace('é','e')
    nome = nome.replace('ê','e')
    nome = nome.replace('í','i')
    nome = nome.replace('ì','i')
    nome = nome.replace('ó','o')
    nome = nome.replace('õ','o')
    nome = nome.replace('ô','o')
    nome = nome.replace('ú','u')
    nome = nome.replace('ù','u')
    nome = nome.replace('ç','c')
    nome = nome.replace('d\'a','da a')
    nome = nome.replace('d\'o','do o')
    nome = nome.replace('d\'e','de e')
    nome = nome.replace(' ', '')

    return nome


def municipioPossuiPortalPrefeitura():
    nomeMunicipioOriginal = municipio[NOME_MUNICIPIO_COLUMN]
    nomeMunicipioTratado = trataCaracteresEspeciais(nomeMunicipioOriginal)
    estado = municipio[SIGLA_ESTADO_COLUMN].lower()


    listaDePossiveisURLs = [
         f'https://www.{nomeMunicipioTratado}.{estado}.gov.br',
         f'http://www.{nomeMunicipioTratado}.{estado}.gov.br',
         f'https://{nomeMunicipioTratado}.{estado}.gov.br',
         f'https://{nomeMunicipioTratado}.{estado}.gov.br',
         f'www.{nomeMunicipioTratado}.{estado}.gov.br'
    ]

    for possivelUrl in listaDePossiveisURLs:
        print(possivelUrl)
        if existePortalPrefeituraParaUrl(possivelUrl):
            print("existePortalPrefeituraParaUrl")
            return True

    return False


if __name__ == '__main__':

    with open('municipios.csv',mode='r', encoding='utf-8') as planilhaDeMunicipios:
        listaDeMunicipios = csv.reader(planilhaDeMunicipios, delimiter=';')

        municipiosComPortalPrefeitura = []
        municipiosSemPortalPrefeitura = []

        for municipio in listaDeMunicipios:
            if municipioPossuiPortalPrefeitura():
                municipiosComPortalPrefeitura.append(municipio)
            else:
                municipiosSemPortalPrefeitura.append(municipio)

    print("municipiosComPortalPrefeitura")
    print(municipiosComPortalPrefeitura)
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

    print("municipiosComPortalPrefeitura")
    print(municipiosSemPortalPrefeitura)

