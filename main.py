import requests
import csv
import ssl


# CONSTANTES
SIGLA_ESTADO_COLUMN = 4
NOME_MUNICIPIO_COLUMN = 2

##GLOBAIS
municipiosStatus200MasNaoIdentificouHtml = []
municipiosStatus200MasErroDecoding = []
municipiosLogoGovCidades = []
municipiosErroTimeout = []


# URL_PADRAO = "http://www.maringa.pr.gov.br"


def existePortalPrefeituraParaUrl(url):
    try:
        response = requests.get(url, verify=False, timeout=3, allow_redirects=True)
        print(response)
        print(response.status_code)
        if response.status_code != 200:
            print("chamada não ok")
            return False


        municipiosStatus200MasErroDecoding.append(municipio)

        responseText = response.text

        municipiosStatus200MasErroDecoding.remove(municipio)

        return htmlRepresentaPortalPrefeitura(responseText)
    except Exception as e:
        print(e)
        return False


def htmlRepresentaPortalPrefeitura(texto):
    if 'prefeitura' in texto.lower():
        if 'logo-govcidades' in texto.lower():
            municipiosLogoGovCidades.append(municipio)
        return True
    else:
        municipiosStatus200MasNaoIdentificouHtml.append(municipio)
        return False


def trataCaracteresEspeciaisGlobal(nome):
    nome = nome.lower()
    nome = nome.replace('ã', 'a')
    nome = nome.replace('á', 'a')
    nome = nome.replace('à', 'a')
    nome = nome.replace('â', 'a')
    nome = nome.replace('ã', 'a')
    nome = nome.replace('é', 'e')
    nome = nome.replace('ê', 'e')
    nome = nome.replace('í', 'i')
    nome = nome.replace('ì', 'i')
    nome = nome.replace('ó', 'o')
    nome = nome.replace('õ', 'o')
    nome = nome.replace('ô', 'o')
    nome = nome.replace('ú', 'u')
    nome = nome.replace('ù', 'u')
    nome = nome.replace('ç', 'c')
    nome = nome.replace('d\'a', 'da a')
    nome = nome.replace('d\'o', 'do o')
    nome = nome.replace('d\'e', 'de e')
    nome = nome.replace('-', '')
    nome = nome.replace(' ', '')
    return nome


def trataCaracteresEspeciaisComTraco(nome):
    nome = nome.lower()
    nome = nome.replace('ã', 'a')
    nome = nome.replace('á', 'a')
    nome = nome.replace('à', 'a')
    nome = nome.replace('â', 'a')
    nome = nome.replace('ã', 'a')
    nome = nome.replace('é', 'e')
    nome = nome.replace('ê', 'e')
    nome = nome.replace('í', 'i')
    nome = nome.replace('ì', 'i')
    nome = nome.replace('ó', 'o')
    nome = nome.replace('õ', 'o')
    nome = nome.replace('ô', 'o')
    nome = nome.replace('ú', 'u')
    nome = nome.replace('ù', 'u')
    nome = nome.replace('ç', 'c')
    nome = nome.replace('d\'a', 'da a')
    nome = nome.replace('d\'o', 'do o')
    nome = nome.replace('d\'e', 'de e')
    nome = nome.replace(' ', '-')
    return nome


def municipioPossuiPortalPrefeitura():
    nomeMunicipioOriginal = municipio[NOME_MUNICIPIO_COLUMN]
    nomeMunicipioTratado = trataCaracteresEspeciaisGlobal(nomeMunicipioOriginal)

    estado = municipio[SIGLA_ESTADO_COLUMN].lower()
    listaDePossiveisURLs = possiveisUrlsPorNomeTratado(estado, nomeMunicipioTratado)

    if '-' or ' ' in nomeMunicipioOriginal:
        nomeMunicipioTratadoComTraco = trataCaracteresEspeciaisComTraco(nomeMunicipioOriginal)

        for url in possiveisUrlsPorNomeTratado(estado, nomeMunicipioTratadoComTraco):
            listaDePossiveisURLs.append(url)

    for possivelUrl in listaDePossiveisURLs:
        print(possivelUrl)

        if existePortalPrefeituraParaUrl(possivelUrl):
            print("existePortalPrefeituraParaUrl")
            return True

    return False


def possiveisUrlsPorNomeTratado(estado, nomeTratado):
    return [
        f'https://www.{nomeTratado}.{estado}.gov.br',
        f'http://www.{nomeTratado}.{estado}.gov.br',
        f'https://{nomeTratado}.{estado}.gov.br',
        f'https://{nomeTratado}.{estado}.gov.br',
        f'www.{nomeTratado}.{estado}.gov.br'
    ]


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_stdlib_context

    with open('municipios.csv', mode='r', encoding='utf-8') as planilhaDeMunicipios:
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
    print(
        "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("municipiosSemPortalPrefeitura")
    print(municipiosSemPortalPrefeitura)
    print(
        "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("municipiosStatus200MasErroDecoding")
    print(municipiosStatus200MasErroDecoding)
    print(
        "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("municipiosStatus200MasNaoIdentificouHtml")
    print(municipiosStatus200MasNaoIdentificouHtml)

    print(
        "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("municipiosErroTimeout")
    print(municipiosErroTimeout)

    print(
        "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("municipiosLogoGovCidades")
    print(municipiosLogoGovCidades)

