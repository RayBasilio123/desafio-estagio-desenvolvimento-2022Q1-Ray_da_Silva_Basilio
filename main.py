import csv
import unicodedata
import re

def strip_accents(string):
    """
    Remove acentos e caracteres especiais de uma string
    :param string: String para remoção dos acentos e caracteres especiais
    :return String sem acentos e caracteres especiais:
    """
    return ''.join(ch for ch in unicodedata.normalize('NFKD', string) if not unicodedata.combining(ch))

def read_file(file_path=None):
    
    cadastros_list = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        cadastros = csv.reader(csvfile, delimiter=',')
        for row in cadastros:
            cadastros_list.append({
                'nome': row[0],
                'email': row[1],
                'cpf': row[2],
                'celular': row[3],
                'idade': row[4],
                'data_nascimento': row[5],
                'data_cadastro': row[6]
            })
    return cadastros_list

def validate_cadastro(cadastro):
    """
    Valida os cadastros (nome, cpf, celular, idade, data_nascimento e data_cadastro) e faz uma proposta de adequação:
    
    Validações:

    nome            : tamanho máximo de 25 caracteres
    email           : formato “primeiroNome.últimoNome@gmail.com”
    cpf             : formato "xxx.xxx.xxx-xx" representando um cpf válido
    celular         : formato "(xx) xxxxx-xxxx"
    idade           : inteiro
    data_nascimento : formato "dd/mm/YYYY"
    data_cadastro   : formato "dd/mm/YYYY"

    return:
        dicionario contendo:
            nome, email, cpf, celular, idade, data_nascimento, data_cadastro, status, reason
    """
    validated_erros = []
    name = cadastro['nome']
    email = cadastro['email']
    cpf = cadastro['cpf']
    celular = cadastro['celular']
    idade=cadastro['idade']
    data_nascimento = cadastro['data_nascimento']
    data_cadastro = cadastro['data_cadastro']
          
    
    cpf_pattern = re.compile(r"^\d{3}.\d{3}.\d{3}-\d{2}$")
    celular_pattern = re.compile(r"^\([1-9]{2}\) [9]{1}[0-9]{3}\-[0-9]{5}$")
    # o formato do celular segundo o arquivo de referencia r"^\(\d{2}\) \d{5}-\d{4}$"
    data_pattern = re.compile(r"^\d{2}/\d{2}/\d{4}$")
    idade_pattern = re.compile(r"^\d{1,3}$")

    # Validacao nome
    if type(name) is not str:
        validated_erros.append(f'nome invalido por nao ser uma str')
    if type(name) is str and len(name) >= 25:
        validated_erros.append(f'Nome inválido: {name} - Correção: Precisa ter 25 ou menos caracteres')

    #validacao email
    if type(email) is not str:
        validated_erros.append('email invalido por não ser uma str')
    name_parts = name.split(' ')

    first_name = strip_accents(name_parts[0])
    last_name = strip_accents(name_parts[len(name_parts) - 1])

    email_pattern = f'{first_name}.{last_name}@gmail.com'

    regex = rf"^{email_pattern}$"
    pattern = re.compile(regex, re.IGNORECASE | re.UNICODE)

    if not pattern.match(email):
        validated_erros.append(f'E-mail inválido: {email} - Correção: Precisa estar no formato (primeiroNome.últimoNome@gmail.com) - ' \
                f'Sugestão: {email_pattern.lower()}')
           
        
    #validacao cpf
    if type(cpf) is not str:
        validated_erros.append('cpf invalido por nao ser uma str')
    if type(cpf) is str and not re.fullmatch(cpf_pattern, cpf):
        validated_erros.append(f'CPF inválido: {cpf} - Correção: Precisa estar no formato (xxx.xxx.xxx-xx)')
    
    #validacao celular
    if type(celular) is not str:
        validated_erros.append('celular invalido por nao ser uma str')
    if type(celular) is str and not re.fullmatch(celular_pattern, celular):
        validated_erros.append(f'Celular inválido: {celular} - Correção: Precisa estar no formato ((xx) xxxxx-xxxx)')

  #validacao da data de nascimento 

    if type(data_nascimento) is not str:
        validated_erros.append('data de nascimento invalida por nao ser uma str')
    if type(data_nascimento) is str and not re.fullmatch(data_pattern, data_nascimento):
        validated_erros.append(f'Data de nascimento inválida: {data_nascimento} - Precisa estar no formato (dd/mm/YYYY)')

  #validacao da data de cadrastro

    if type(data_cadastro) is not str:
        validated_erros.append('data de cadastro invalida por nao ser uma str')
    if type(data_cadastro) is str and not re.fullmatch(data_pattern, data_cadastro):
        validated_erros.append(f'Data de cadastro inválida: {data_cadastro} - Precisa estar no formato (dd/mm/YYYY)')
 
 
    #validacao da idade


    if  not re.fullmatch(idade_pattern, idade):
        validated_erros.append(f'Idade inválida: {idade} - Precisa ser um número inteiro')


    if validated_erros !=[] :
        cadastro['status']= "inválido"
        cadastro['reason'] = validated_erros
    else:
        cadastro['status']= "válido"
    
            
    # print(cadastro)
    return (cadastro)

def export_validate_registers(cadastros_list):
    """
    exporta o arquivo dos cadastros validados no formato txt 
    
    """
    file = open('resultados.txt', 'w')
    for cadastro in cadastros_list[1:]:
        vc=validate_cadastro(cadastro)
        
        file.write(str(vc))
        print(str(vc))
        file.write('\n')

    file.close()

if __name__ == '__main__':
    cadastros_list = read_file('cadastros.csv')
    export_validate_registers(cadastros_list)
