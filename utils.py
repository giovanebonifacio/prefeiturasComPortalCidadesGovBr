import json

#CONSTANTES
SIGLA_ESTADO_COLUMN = 4
NOME_MUNICIPIO_COLUMN = 2

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

def write_json_municipios(new_data, column, filename='data.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[column].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

def write_json_erros(new_data, column, filename='error.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[column].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

def write_json_acessadas_sem_validar_html(new_data, column, filename='acessadasSemValidarHtml.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[column].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

def possiveisUrlsPorNomeTratado(estado, nomeTratado):
    return [
        f'https://www.{nomeTratado}.{estado}.gov.br',
        f'http://www.{nomeTratado}.{estado}.gov.br',
        f'https://{nomeTratado}.{estado}.gov.br',
        f'https://{nomeTratado}.{estado}.gov.br',
        f'www.{nomeTratado}.{estado}.gov.br'
    ]