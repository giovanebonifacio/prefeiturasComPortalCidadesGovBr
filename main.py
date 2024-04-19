import requests
from requests import exceptions
import ssl
import json
from googlesearch import search
from pymongo import MongoClient
from utils import (possiveisUrlsPorNomeTratado, trataCaracteresEspeciaisGlobal,
                   trataCaracteresEspeciaisComTraco)

# Conecte-se ao MongoDB (ajuste o host e a porta conforme necessário)
client = MongoClient("mongodb://localhost:27017/")

# Escolha o banco de dados e a coleção
db = client["local"]
collection = db["municipiosTcc"]


def verificaSeMunicipioPossuiPortalPrefeitura():
    nomeMunicipioOriginal = municipio.get('municipioTOM').lower()
    estado = municipio.get('uf').lower()
    rowId = municipio.get('_id')

    nomeMunicipioBuscaGoogle = nomeMunicipioOriginal.replace(' ', '+')

    urlBuscaGoogle = f'prefeitura+municipal+de+{nomeMunicipioBuscaGoogle}+{estado}'

    print(urlBuscaGoogle)
    resultadoBuscaGoogle = google(urlBuscaGoogle)

    listaLinksResultadoGoogle = []

    for link in resultadoBuscaGoogle:
        print("Link Google :" + link)
        listaLinksResultadoGoogle.append(link)

        if urlFormatoEsperadoParaPortalDePrefeitura(estado, link):

            print("Link Google padrao pref:" + link)
            if consegueAcessarPortalPrefeituraParaUrl(link):
                print("existePortalPrefeituraParaUrl")
                collection.update_one({'_id': rowId}, {"$set": municipio}, upsert=False)
                return True

    print("não identifica com busca google, tentando acessar possiveis dominios")

    nomeMunicipioTratado = trataCaracteresEspeciaisGlobal(nomeMunicipioOriginal)
    listaDePossiveisURLs = possiveisUrlsPorNomeTratado(estado, nomeMunicipioTratado)

    if '-' or ' ' in nomeMunicipioOriginal:
        nomeMunicipioTratadoComTraco = trataCaracteresEspeciaisComTraco(nomeMunicipioOriginal)

        for url in possiveisUrlsPorNomeTratado(estado, nomeMunicipioTratadoComTraco):
            listaDePossiveisURLs.append(url)

    for possivelUrl in listaDePossiveisURLs:
        listaLinksResultadoGoogle.append(possivelUrl)
        print(possivelUrl)

        if consegueAcessarPortalPrefeituraParaUrl(possivelUrl):
            print("existePortalPrefeituraParaUrl")
            collection.update_one({'_id': rowId}, {"$set": municipio}, upsert=False)
            return True

    return False


def urlFormatoEsperadoParaPortalDePrefeitura(estado, link):
    return (".gov.br" in link or ".atende.net" in link) and (
            f'tcm.{estado}.gov.br' not in link
            and 'datasus.gov.br' not in link
            and 'portaldatransparencia.gov.br' not in link
            and 'ibge.' not in link
            and 'diariooficial' not in link
            and 'comprasnet.gov.br' not in link
            and 'defesacivil.' not in link
            and f'tce.{estado}.gov.br' not in link
    )


def google(query):
    return search(query, num_results=10, lang="pt-br")


def consegueAcessarPortalPrefeituraParaUrl(url):
    try:
        headers = {
            'User-Agent': 'My User Agent 1.0',
            'From': 'youremail@domain.example'  # This is another valid field
        }

        response = requests.get(url, headers=headers, verify=False, timeout=15, allow_redirects=True)

        print(response)
        print(response.status_code)

        if response.status_code == 503 and ('manutenção' or 'manutencao') in response.text.lower():
            print("503 em manutenção")
            municipio['emManutencao'] = True

        if response.status_code != 200:
            municipio['identificouConteudoHtml'] = False
        else:
            responseText = response.text.lower()
            municipio['logoGovCidadesBr'] = pertenceAoPortalCidadesGovBr(responseText)
            municipio['identificouConteudoHtml'] = interpretaHtmlRepresentaPortalPrefeitura(responseText)

        municipio['url'] = url
        return True
    except exceptions.RetryError as retryError:
        print(retryError)
        return False
    except Exception as e:
        print(e)
        return False


def interpretaHtmlRepresentaPortalPrefeitura(texto):
    nomeOriginal = municipio["municipioTOM"].lower()
    nomeTratadoSemEspaco = trataCaracteresEspeciaisGlobal(nomeOriginal)
    nomeTratadoComTraco = trataCaracteresEspeciaisComTraco(nomeOriginal)
    nomeTratadoTracoCharEspecial = nomeOriginal.replace('\'', '’')

    return 'prefeitura' in texto and (
            nomeOriginal in texto or nomeTratadoComTraco in texto or nomeTratadoSemEspaco in texto or nomeTratadoTracoCharEspecial in texto)


def pertenceAoPortalCidadesGovBr(texto):
    return 'govbr-cidades-footer' in texto


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_stdlib_context

    query = {'url': {'$exists': False}}
    for municipio in collection.find(query):
        # for municipio in collection.find():
        print(municipio)
        verificaSeMunicipioPossuiPortalPrefeitura()
