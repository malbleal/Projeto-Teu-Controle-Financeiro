import csv
import json
from datetime import datetime
from datetime import timezone
from datetime import timedelta

def salvar_csv(dados, nome_arquivo):

    arquivo_existente = False

    try:
        with open(nome_arquivo, 'r') as file:
            arquivo_existente = True

    except FileNotFoundError:
        pass

    with open(nome_arquivo, 'a', newline='') as file:

        writer = csv.writer(file)

        if not arquivo_existente:
            writer.writerow(['id_usuario', 'data_investimento', 'data_atual', 'Investimento', 'Montante'])

        writer.writerow(dados)

def read(id_usuario):
    linhas_encontradas = []

    with open('dados.csv', 'r') as arquivo:
        csvreader = csv.reader(arquivo)
        cabecalho = next(csvreader)
        linhas_encontradas.append(cabecalho)

        for row in csvreader:
            if row[0] == id_usuario:
                linhas_encontradas.append(row)

    return linhas_encontradas


def salvar_em_json(registros, nome_salvar):
    with open(nome_salvar, 'w') as arq_json:
        json.dump(registros, arq_json)


def ler_em_json(nome_salvar):
    try:
        with open(nome_salvar, 'r') as arq_json:
            dados_json = json.load(arq_json)
        return dados_json
    except FileNotFoundError:
        return []

# def exportar_relatorio():

def retorna_hoje(offset: int = -3) -> datetime.date:
    """
    Essa funcao retorna a data de hoje no fuso horario informado.
    Por padrão o fuso horario é o UTC -3:00, America/Sao_Paulo
    """
    timezone_offset = offset  # America/Sao_Paulo (UTC−03:00)
    tzinfo = timezone(timedelta(hours=timezone_offset))
    today = datetime.now(tzinfo).date()
    return today

def calcula_diferenca_dias(data_fim:datetime.date,data_ini:datetime.date)->int:
    """
    Recebe duas datas e calcula a diferenca de dias entre elas.
    """
    dif = data_fim - data_ini
    dias = dif.days
    return dias

def cabecalho():
    print("| {:<10} | {:<15} | {:<15} | {:<10} | {:<16} |".format(
        "ID", "Tipo", "Categoria", "Valor", "Data do Registro"
    ))
    print("-" * 76)

def print_info(dados):
    for registro in dados:
        print("| {:<10} | {:<15} | {:<15} | {:<10} | {:<16} |".format(
            registro['id_registro'],
            registro['tipo'],
            registro['categoria'],
            registro['valor'],
            registro['data_registro']
        ))

    print("-" * 76)


def adicionar_registro(id_usuario):
    registros = ler_em_json('registros.json')

    data = str(retorna_hoje())
    tipo = input('Digite o tipo do registro Despesa: d, Receita: r, Investimento: i, Sair: s\n')

    if tipo == 's':
        return
    elif tipo == 'd':
        tipo = "Despesa"
    elif tipo == 'r':
        tipo = "Receita"
    elif tipo == 'i':
        tipo = "Investimento"
    else:
        print('Tipo inválido. Saindo...')
        return

    valor = float(input(f'digite o valor do(a) {tipo}: '))
    categoria = input(f'digite a categoria do(a) {tipo}: ')

    try:
        id_registro = max([i['id_registro'] for i in registros]) + 1
    except:
        id_registro = 0

    # Separar a data em dia, mês e ano
    ano, mes, dia = map(int, data.split('-'))

    # Tratar despesas como valores negativos
    if tipo == 'Despesa':
        valor = -valor

    # Adicionar novo registro à lista
    novo_registro = {'id_registro': id_registro, 'id_usuario': id_usuario, 'tipo': tipo, 'categoria': categoria,
                     'valor': valor, 'dia': dia, 'mes': mes, 'ano': ano, 'data_registro': data}
    registros.append(novo_registro)
    salvar_em_json(registros, 'registros.json')


def ler_registro(id_usuario):
    registros = ler_em_json('registros.json')
    consulta_registros = [registro for registro in registros if registro['id_usuario'] == id_usuario]

    print(f"\nRegistros do usuário {id_usuario} ")

    # funções pra printar cabeçalho e informações filtradas
    cabecalho()
    print_info(consulta_registros)


def editar_registro(id_usuario):
    data = str(retorna_hoje())
    ano, mes, dia = map(int, data.split('-'))

    registros = ler_em_json('registros.json')
    consulta_registros = [registro for registro in registros if registro['id_usuario'] == id_usuario]
    print(f"\nRegistros do usuário {id_usuario} ")

    # funções pra printar cabeçalho e informações filtradas
    cabecalho()
    print_info(consulta_registros)

    id_registro_para_editar = int(input("Informe o ID do REGISTRO que deseja editar "))
    indice_para_editar = [i for i, registro in enumerate(registros) if
                          registro['id_registro'] == id_registro_para_editar]

    tipo = input('Digite o novo TIPO do registro - Despesa: d, Receita: r, Investimento: i\n')
    valor = float(input('Digite o novo VALOR do registro\n'))

    if tipo == 'd':
        tipo = "Despesa"
    elif tipo == 'r':
        tipo = "Receita"
    elif tipo == 'i':
        tipo = "Investimento"
    else:
        print('Opção inválida. Saindo...')
        return

    # Tratar despesas como valores negativos
    if tipo == 'Despesa':
        valor = -valor

    registros[indice_para_editar[0]]['valor'] = valor
    registros[indice_para_editar[0]]['tipo'] = tipo
    registros[indice_para_editar[0]]['dia'] = dia
    registros[indice_para_editar[0]]['mes'] = mes
    registros[indice_para_editar[0]]['ano'] = ano

    salvar_em_json(registros, 'registros.json')

    print("Registro Editado!")


def deletar_registro(id_usuario):
    registros = ler_em_json('registros.json')
    registros_do_usuario = [registro for registro in registros if registro['id_usuario'] == id_usuario]

    print(f"\nRegistros do usuário {id_usuario} ")

    # funções pra printar cabeçalho e informações filtradas
    cabecalho()
    print_info(registros_do_usuario)

    id_registro_para_deletar = int(input("Informe o ID do REGISTRO que deseja deletar "))

    escolha = input(f'Tem certeza que deseja DELETAR o registro {id_registro_para_deletar}? S/N ')

    if escolha.upper() == 'S':
        registros = [registro for registro in registros if registro['id_registro'] != id_registro_para_deletar]

        salvar_em_json(registros, 'registros.json')

        print("Registro Deletado!")

    elif escolha.upper() == 'N':
        print("Operação Cancelada ")

    else:
        print("Opção Inválida ")
        print("Voltando para o menu principal ")



def filtrar_registro(id_usuario):
    registros = ler_em_json('registros.json')

    filtro_tipo = int(input(" 1 - dia\n 2 - mês\n 3 - ano\n Utilize os indices para a escolha: "))
    

    consulta_registros1 = []

    if filtro_tipo == 1:
        
        filtro_tipo = 'Dia'
        filtro_valor = int(input(f"Digite o valor do filtro para o(a) {filtro_tipo}: "))
        
        consulta_registros1 = [registro for registro in registros if
                               registro['id_usuario'] == id_usuario and registro['dia'] == filtro_valor]
        
    elif filtro_tipo == 2:
        
        filtro_tipo = 'Mês'
        filtro_valor = int(input(f"Digite o valor do filtro para o(a) {filtro_tipo}: "))
        
        consulta_registros1 = [registro for registro in registros if
                               registro['id_usuario'] == id_usuario and registro['mes'] == filtro_valor]
        
    elif filtro_tipo == 3:
        
        filtro_tipo = 'Ano'
        filtro_valor = int(input(f"Digite o valor do filtro para o(a) {filtro_tipo}: "))
        
        consulta_registros1 = [registro for registro in registros if
                               registro['id_usuario'] == id_usuario and registro['ano'] == filtro_valor]
        
    else:
        print("Tipo de filtro inválido. Voltando para o menu principal.")
        return

    print(f"\nRegistros do usuário {id_usuario} filtrados pelo {filtro_tipo} {filtro_valor}")

    # funções pra printar cabeçalho e informações filtradas
    cabecalho()
    print_info(consulta_registros1)


def investimento(id_usuario):
    registros = ler_em_json('registros.json')
    registros_do_usuario = [registro for registro in registros if registro['id_usuario'] == id_usuario]

    data = retorna_hoje()

    for i in registros_do_usuario:
        if i['tipo'] == "Investimento":
            data_datetime = datetime.strptime(i["data_registro"], "%Y-%m-%d").date()
            dif = calcula_diferenca_dias(data, data_datetime)
            valor = i['valor']
            taxa = 0.1/100
            rendimento = valor*(1 + taxa)**dif
            formatado = "{:.2f}".format(rendimento)
            # print(f'R${rendimento:.2f}')
            dados_para_salvar = [id_usuario, i["data_registro"], str(data), valor, formatado]

            salvar_csv(dados_para_salvar, 'Meus_investimentos.csv')
            print('Seus dados foram salvos em um arquivo único.')

    


def menu_principal():
    menu = int(input(
        ' 1 - Criar novo Registro\n 2 - Visualizar Registro\n 3 - Editar Registro\n 4 - Deletar Registro\n 5 - Visualizar por Filtro (dia,mês,ano)\n 6 - Investimento\n 7 - Trocar usuário\n 0 - Sair do Programa\n O que deseja fazer? (utilize os índices para utilizar o menu) '))

    if menu == 1:  # Adicionar registro
        adicionar_registro(id_usuario)

    elif menu == 2:  # Visualizar registro
        ler_registro(id_usuario)

    elif menu == 3:  # Editar registro
        editar_registro(id_usuario)

    elif menu == 4:  # Deletar registro
        deletar_registro(id_usuario)

    elif menu == 5:  # Filtrar por Dia/Mês/Ano
        filtrar_registro(id_usuario)

    elif menu == 6: #Investimento
        investimento(id_usuario)

    elif menu == 7: #Trocar de usuário
        return 7

    elif menu == 0: #Sair do programa
        return 0

    else:
        print('Opção Inválida')


id_usuario = input("Informe o ID do Usuário: ")

menu = 1
while menu != 0:
    menu = menu_principal()
    if menu == 7:
        id_usuario = input("Informe o ID do Usuário: ")
    elif menu == 0:
        print('Encerrando o programa!')



        
        