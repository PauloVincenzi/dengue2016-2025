import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime, date
from statistics import stdev

fx_et = ['4 anos ou menos', 'entre 5 e 9', 'entre 10 e 14', 'entre 15 e 19', 'entre 20 e 29', 'entre 30 e 39', 
    'entre 40 e 49', 'entre 50 e 59', 'entre 60 e 69', 'entre 70 e 79', '80 anos ou mais']
fx_et_completa = fx_et + ['faixa_desconhecida']


def calcular_idade(data_nasc, data_notif):
    if pd.isnull(data_nasc) or pd.isnull(data_notif):
        return None  # ou pd.NA
    idade = data_notif.year - data_nasc.year
    if (data_notif.month, data_notif.day) < (data_nasc.month, data_nasc.day):
        idade -= 1
    return idade


def obter_faixa_etaria(idade):
    if idade is None:
        return None
    elif idade <= 4:
        return '4 anos ou menos'
    elif idade <= 9:
        return 'entre 5 e 9'
    elif idade <= 14:
        return 'entre 10 e 14'
    elif idade <= 19:
        return 'entre 15 e 19'
    elif idade <= 29:
        return 'entre 20 e 29'
    elif idade <= 39:
        return 'entre 30 e 39'
    elif idade <= 49:
        return 'entre 40 e 49'
    elif idade <= 59:
        return 'entre 50 e 59'
    elif idade <= 69:
        return 'entre 60 e 69'
    elif idade <= 79:
        return 'entre 70 e 79'
    else:
        return '80 anos ou mais'


def testar_estimativas(media_prop, dp_amost_prop, m, dado):
    for n in range(3):
        print()
        for c in range(4):
            if c == 0:
                z = 2.576
                ic = '99%'
            elif c == 1:
                z = 1.960
                ic = '95%'
            elif c == 2:
                z = 1.645
                ic = '90%'
            else:
                z = 1.282
                ic = '80%'
            if n == 1:
                media = media_prop[n][m-1]
                desvio_padrao = dp_amost_prop[n][m-1]
            elif n == 2:
                media = media_prop[n][m-1]
                desvio_padrao = dp_amost_prop[n][m-1]
            else:
                media = media_prop[n][m-1]
                desvio_padrao = dp_amost_prop[n][m-1]
            estimativa_media = dado / media
            limite_inferior = media - (z * desvio_padrao) / 3
            limite_superior = media + (z * desvio_padrao) / 3

            total_maximo = dado / limite_inferior
            total_minimo = dado / limite_superior
            if m == 1:
                print(f'M{n+1} com intervalo de confiança de {ic}: entre {int(total_minimo)} e {int(total_maximo)} casos notificados de dengue')
            elif m == 2:
                print(f'M{n+1} com intervalo de confiança de {ic}: entre {int(total_minimo)} e {int(total_maximo)} casos confirmados de dengue')
            elif m == 3:
                print(f'M{n+1} com intervalo de confiança de {ic}: entre {int(total_minimo)} e {int(total_maximo)} casos negativos de dengue')
            else:
                print(f'M{n+1} com intervalo de confiança de {ic}: entre {int(total_minimo)} e {int(total_maximo)} óbitos decorrentes de dengue')
        


def processar_banco(caminho_csv):
    # Carrega o CSV
    df = pd.read_csv(caminho_csv)


    # Tratar os dados
    df['DT_NASC'] = pd.to_datetime(df['DT_NASC'], format="%Y-%m-%d", errors="coerce")
    df['DT_NOTIFIC'] = pd.to_datetime(df['DT_NOTIFIC'], format="%Y-%m-%d", errors="coerce")
    df['DT_OBITO'] = pd.to_datetime(df['DT_OBITO'], format="%Y-%m-%d", errors="coerce")
    df['RESUL_SORO'] = pd.to_numeric(df['RESUL_SORO'], errors='coerce')
    df['RESUL_NS1'] = pd.to_numeric(df['RESUL_NS1'], errors='coerce')
    df['RESUL_PCR_'] = pd.to_numeric(df['RESUL_PCR_'], errors='coerce')
    df['CLASSI_FIN'] = pd.to_numeric(df['CLASSI_FIN'], errors='coerce')


    # Extrai os dados da coluna como lista
    data_notificacao = df['DT_NOTIFIC'].tolist()
    data_nascimento = df['DT_NASC'].tolist()
    resultado_soro = df['RESUL_SORO'].tolist()
    resultado_ns1 = df['RESUL_NS1'].tolist()
    resultado_pcr = df['RESUL_PCR_'].tolist()
    classif_final = df['CLASSI_FIN'].tolist()
    data_obito = df['DT_OBITO'].tolist()

    # Determinar o ano do banco de dados
    ano = df['DT_NOTIFIC'].dropna().dt.year.mode()[0]

    # Agrupa os dados com um classificador para cada variável
    dados_notificacao = {
        'data_notificacao': data_notificacao,
        'data_nascimento': data_nascimento,
        'resultado_soro': resultado_soro ,
        'resultado_ns1': resultado_ns1, 
        'resultado_pcr': resultado_pcr, 
        'classif_final': classif_final, 
        'data_obito': data_obito,
        'idade': [],
        'faixa_etaria': [],
        'confirmado?': []
    }


    # Determinar a idade do indíviduo no momento da notificação e, logo, a faixa etária que se enquadrava.
    for i in range(len(df)):
        idade = calcular_idade(data_nascimento[i], data_notificacao[i])
        dados_notificacao['idade'].append(idade)
        dados_notificacao['faixa_etaria'].append(obter_faixa_etaria(idade))


    # Determinar se a notificaçao foi confirmada ou não.
    for i in range(len(df)):
        if dados_notificacao['classif_final'][i] == 10 or dados_notificacao['classif_final'][i] == 11 or dados_notificacao['classif_final'][i] == 12:
            dados_notificacao['confirmado?'].append('SIM')
        elif dados_notificacao['resultado_soro'][i] == 1:
            dados_notificacao['confirmado?'].append('SIM')
        elif dados_notificacao['resultado_ns1'][i] == 1:
            dados_notificacao['confirmado?'].append('SIM')
        elif dados_notificacao['resultado_pcr'][i] == 1:
            dados_notificacao['confirmado?'].append('SIM')
        elif None == dados_notificacao['classif_final'][i] == dados_notificacao['resultado_soro'][i] == dados_notificacao['resultado_ns1'][i] == dados_notificacao['resultado_pcr'][i]:
            dados_notificacao['confirmado?'].append(None)
        else:
            dados_notificacao['confirmado?'].append('NÃO')


    # Uma lista com 12 dicionários representando os meses.
    # dentro de cada dicionário (mês), há chaves representando a divisão por faixa etária
    # os valores das chaves são listas com três elementos, onde o primeiro simboliza
    # o nº de notificações, o segundo o nº de casos positivos, o terceiro o nº de casos negativos e o quarto o nº de óbitos
    info_por_mes_e_fx_et = [{cat: [0, 0, 0, 0] for cat in fx_et_completa} for _ in range(12)]


    # Loop de contagem por mês e faixa etária
    for i in range(len(df)):
        data_notif = dados_notificacao['data_notificacao'][i]
        faixa = dados_notificacao['faixa_etaria'][i]

        if pd.isna(data_notif):
            continue  # Não conta se nem a data for válida

        mes_index = data_notif.month - 1

        if faixa is None:
            faixa = 'faixa_desconhecida'

        # Notificações
        info_por_mes_e_fx_et[mes_index][faixa][0] += 1

        # Confirmados
        if dados_notificacao['confirmado?'][i] == 'SIM':
            info_por_mes_e_fx_et[mes_index][faixa][1] += 1
        elif dados_notificacao['confirmado?'][i] == 'NÃO':
            info_por_mes_e_fx_et[mes_index][faixa][2] += 1

        # Óbitos
        if pd.notna(dados_notificacao['data_obito'][i]):
            mes_obito = dados_notificacao['data_obito'][i].month - 1
            info_por_mes_e_fx_et[mes_obito][faixa][3] += 1


    # Lista de meses
    meses = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]


    # Inicializa a lista com 12 sublistas [notificados, confirmados, negativos, óbitos] para cada mês
    info_por_mes = [[0, 0, 0, 0] for _ in range(12)]


    # Atualiza info_por_mes somando os valores por faixa etária para cada mês
    for n_mes in range(12):
        for cat in fx_et_completa:
            info_por_mes[n_mes][0] += info_por_mes_e_fx_et[n_mes][cat][0]  # Notificados
            info_por_mes[n_mes][1] += info_por_mes_e_fx_et[n_mes][cat][1]  # Confirmados
            info_por_mes[n_mes][2] += info_por_mes_e_fx_et[n_mes][cat][2]  # Negativos
            info_por_mes[n_mes][3] += info_por_mes_e_fx_et[n_mes][cat][3]  # Óbitos


    # Exibe totais
    print('-'*150)
    print(f'ANO: {ano}')
    print('-'*150)

    total_notificados = sum(m[0] for m in info_por_mes)
    total_confirmados = sum(m[1] for m in info_por_mes)
    total_negativos = sum(m[2] for m in info_por_mes)
    total_obitos = sum(m[3] for m in info_por_mes)

    print("Total de Notificados:", total_notificados)
    print("Total de Confirmados:", total_confirmados)
    print("Total de Negativos:", total_negativos)
    print("Total de Óbitos:", total_obitos)
    print('-'*150)

    proporcao_m1 = [0, 0, 0, 0]
    proporcao_m2 = [0, 0, 0, 0]
    proporcao_m3 = [0, 0, 0, 0]
    for n_mes in range(3):
        proporcao_m1[0] += info_por_mes[n_mes][0]
        proporcao_m1[1] += info_por_mes[n_mes][1]
        proporcao_m1[2] += info_por_mes[n_mes][2]
        proporcao_m1[3] += info_por_mes[n_mes][3]
    for n_mes in range(6):
        proporcao_m2[0] += info_por_mes[n_mes][0]
        proporcao_m2[1] += info_por_mes[n_mes][1]
        proporcao_m2[2] += info_por_mes[n_mes][2]
        proporcao_m2[3] += info_por_mes[n_mes][3]
    for n_mes in range(9):
        proporcao_m3[0] += info_por_mes[n_mes][0]
        proporcao_m3[1] += info_por_mes[n_mes][1]
        proporcao_m3[2] += info_por_mes[n_mes][2]
        proporcao_m3[3] += info_por_mes[n_mes][3]
    proporcao_m1[0] = proporcao_m1[0] / total_notificados
    proporcao_m1[1] = proporcao_m1[1] / total_confirmados
    proporcao_m1[2] = proporcao_m1[2] / total_negativos
    proporcao_m1[3] = proporcao_m1[3] / total_obitos
    proporcao_m2[0] = proporcao_m2[0] / total_notificados
    proporcao_m2[1] = proporcao_m2[1] / total_confirmados
    proporcao_m2[2] = proporcao_m2[2] / total_negativos
    proporcao_m2[3] = proporcao_m2[3] / total_obitos
    proporcao_m3[0] = proporcao_m3[0] / total_notificados
    proporcao_m3[1] = proporcao_m3[1] / total_confirmados
    proporcao_m3[2] = proporcao_m3[2] / total_negativos
    proporcao_m3[3] = proporcao_m3[3] / total_obitos

    if ano == 2025:
        proporcao_m1 = [0, 0, 0, 0]
        proporcao_m2 = [0, 0, 0, 0]
        proporcao_m3 = [0, 0, 0, 0]
    print(f'Proporção m1: {proporcao_m1}')
    print(f'Proporção m2: {proporcao_m2}')
    print(f'Proporção m3: {proporcao_m3}')

    # Constrói DataFrame com todos os dados por faixa e mês
    dados = []
    for i, mes_dict in enumerate(info_por_mes_e_fx_et):
        for faixa, valores in mes_dict.items():
            dados.append({
                "mês": meses[i],
                "faixa_etária": faixa,
                "confirmados": valores[1],
                "negativos": valores[2],
                "óbitos": valores[3]
            })


    df = pd.DataFrame(dados)
    df["mês"] = pd.Categorical(df["mês"], categories=meses, ordered=True)
    df = df.sort_values(["faixa_etária", "mês"])
    
    print('-'*150)
    return ano, [info_por_mes_e_fx_et, info_por_mes, total_notificados, total_confirmados, total_negativos, total_obitos, proporcao_m1, proporcao_m2, proporcao_m3]

bancos_de_dados = ['C:/Users/ABREU/Desktop/Python/requerimento_dengue/bancos_de_dados/csv/DENGON2520190_002016.csv',
                   'C:/Users/ABREU/Desktop/Python/requerimento_dengue/bancos_de_dados/csv/DENGON2520194_002017.csv',
                   'C:/Users/ABREU/Desktop/Python/requerimento_dengue/bancos_de_dados/csv/DENGON2520195_002018.csv',
                   'C:/Users/ABREU/Desktop/Python/requerimento_dengue/bancos_de_dados/csv/DENGON2520196_002019.csv',
                   'C:/Users/ABREU/Desktop/Python/requerimento_dengue/bancos_de_dados/csv/DENGON2520197_002020.csv',
                   'C:/Users/ABREU/Desktop/Python/requerimento_dengue/bancos_de_dados/csv/DENGON2520198_002021.csv',
                   'C:/Users/ABREU/Desktop/Python/requerimento_dengue/bancos_de_dados/csv/DENGON2520199_002022.csv',
                   'C:/Users/ABREU/Desktop/Python/requerimento_dengue/bancos_de_dados/csv/DENGON2520200_002023.csv',
                   'C:/Users/ABREU/Desktop/Python/requerimento_dengue/bancos_de_dados/csv/DENGON2520201_002024.csv',
                   'C:/Users/ABREU/Desktop/Python/requerimento_dengue/bancos_de_dados/csv/DENGON2520202_002025.csv',
                   ]

# RODAR CADA BANCO DE DADOS E ACUMULAR OS DADOS EM DADOS_GERAIS
dados_gerais = {}
for i in range(10):
    ano, dados = processar_banco(bancos_de_dados[i])
    dados_gerais[ano] = dados

print('=' * 150)
print("RESUMO GERAL DOS DADOS ACUMULADOS")
print('=' * 150)

total_notificados_geral = 0
total_confirmados_geral = 0
total_negativos_geral = 0
total_obitos_geral = 0
info_por_mes_e_fx_et_acumulado = [{cat: [0, 0, 0, 0] for cat in fx_et_completa} for _ in range(12)]
info_por_mes_acumulado = [[0, 0, 0, 0] for _ in range(12)]
soma_m1 = [0, 0, 0, 0]
soma_m2 = [0, 0, 0, 0]
soma_m3 = [0, 0, 0, 0]
media_prop_m1 = [0, 0, 0, 0]
media_prop_m2 = [0, 0, 0, 0]
media_prop_m3 = [0, 0, 0, 0]
dp_amost_prop_m1 = [0, 0, 0, 0]
dp_amost_prop_m2 = [0, 0, 0, 0]
dp_amost_prop_m3 = [0, 0, 0, 0]
lista_prop_m1 = [[] for _ in range(4)]
lista_prop_m2 = [[] for _ in range(4)]
lista_prop_m3 = [[] for _ in range(4)]

for ano, dados in sorted(dados_gerais.items()):
    info_por_mes_e_fx_et, info_por_mes, notificados, confirmados, negativos, obitos, prop_m1, prop_m2, prop_m3 = dados
    total_notificados_geral += notificados
    total_confirmados_geral += confirmados
    total_negativos_geral += negativos
    total_obitos_geral += obitos
    for i in range(4):
        soma_m1[i] += prop_m1[i]
        soma_m2[i] += prop_m2[i]
        soma_m3[i] += prop_m3[i]
    for n_mes in range(12):
        for cat in fx_et_completa:
            info_por_mes_e_fx_et_acumulado[n_mes][cat][0] += info_por_mes_e_fx_et[n_mes][cat][0]
            info_por_mes_e_fx_et_acumulado[n_mes][cat][1] += info_por_mes_e_fx_et[n_mes][cat][1]
            info_por_mes_e_fx_et_acumulado[n_mes][cat][2] += info_por_mes_e_fx_et[n_mes][cat][2]
            info_por_mes_e_fx_et_acumulado[n_mes][cat][3] += info_por_mes_e_fx_et[n_mes][cat][3]
            info_por_mes_acumulado[n_mes][0] += info_por_mes_e_fx_et[n_mes][cat][0]
            info_por_mes_acumulado[n_mes][1] += info_por_mes_e_fx_et[n_mes][cat][1]
            info_por_mes_acumulado[n_mes][2] += info_por_mes_e_fx_et[n_mes][cat][2]
            info_por_mes_acumulado[n_mes][3] += info_por_mes_e_fx_et[n_mes][cat][3]
for i in range(4):
    media_prop_m1[i] = soma_m1[i] / 9
    media_prop_m2[i] = soma_m2[i] / 9
    media_prop_m3[i] = soma_m3[i] / 9
for ano, dados in sorted(dados_gerais.items()):
    _, _, _, _, _, _, prop_m1, prop_m2, prop_m3 = dados
    if ano != 2025:
        for i in range(4):
            lista_prop_m1[i].append(prop_m1[i])
            lista_prop_m2[i].append(prop_m2[i])
            lista_prop_m3[i].append(prop_m3[i])

# Calcular desvio padrão usando a função pronta
dp_amost_prop_m1 = [stdev(lista) for lista in lista_prop_m1]
dp_amost_prop_m2 = [stdev(lista) for lista in lista_prop_m2]
dp_amost_prop_m3 = [stdev(lista) for lista in lista_prop_m3]

print('-'*150)
print("Info por mês e faixa etária:", info_por_mes_e_fx_et_acumulado)
print('='*150)
print("Info por mês:", info_por_mes_acumulado)
print('=' * 150)
print("TOTAIS GERAIS DE TODOS OS ANOS")
print('=' * 150)
print(f"Total Geral de Notificados: {total_notificados_geral}")
print(f"Total Geral de Confirmados: {total_confirmados_geral}")
print(f"Total Geral de Negativos: {total_negativos_geral}")
print(f"Total Geral de Óbitos: {total_obitos_geral}")
print('=' * 150)
print(f'Média proporção m1: {media_prop_m1}')
print(f'Média proporção m2: {media_prop_m2}')
print(f'Média proporção m3: {media_prop_m3}')
print('=' * 150)
print(f'Desvio Padrão proporção m1: {dp_amost_prop_m1}')
print(f'Desvio Padrão proporção m2: {dp_amost_prop_m2}')
print(f'Desvio Padrão proporção m3: {dp_amost_prop_m3}')


# ESTIMAR

# Para estimar o total de notificações, casos confirmados e óbitos por dengue em um ano em curso com dados parciais (até o mês M), 
# foi construída uma estimativa com base nas proporções acumuladas em anos anteriores, utilizando intervalos de confiança para prever o 
# total anual com um grau de incerteza mensurado estatisticamente.

print('-'*150)
print('ESTIMAR: NÚMERO DE NOTIFICAÇÕES / NÚMERO DE CASOS CONFIRMADOS / NÚMERO DE CASOS NEGATIVOS / Nº DE ÓBITOS DO ANO INTEIRO')
print('COM BASE EM DADOS JÁ COLETADOS ATÉ DETERMINADO MÊS DO ANO EM QUESTÃO')
n = 0
while n not in (1, 2, 3):
    print('-'*150)
    print('Digite [1] para inserir dados (já coletados) até o fim de março (temos informações de 25 % do ano)')
    print('Digite [2] para inserir dados (já coletados) até o fim de junho (temos informações de 50 % do ano)')
    print('Digite [3] para inserir dados (já coletados) até o fim de setembro (temos informações de 75 % do ano)')
    try:
        n = int(input('Sua escolha: '))
    except ValueError:
        print('Entrada inválida! Digite um número de 1 a 3.\n')
        n = 0
print('Qual dado você quer estimar?')
m = 0
while m not in (1, 2, 3, 4):
    print('-'*150)
    print('Digite [1] para estimar o número de notificações')
    print('Digite [2] para estimar o número de casos confirmados')
    print('Digite [3] para estimar o número de casos negativos')
    print('Digite [4] para estimar o número de óbitos')
    try:
        m = int(input('Sua escolha: '))
    except ValueError:
        print('Entrada inválida! Digite um número de 1 a 4.\n')
        m = 0
print('-'*150)
dado = int(input('Digite o número já coletado do dado que deseja estimar: '))
if n == 1:
    media = media_prop_m1[m-1]
    desvio_padrao = dp_amost_prop_m1[m-1]
elif n == 2:
    media = media_prop_m2[m-1]
    desvio_padrao = dp_amost_prop_m2[m-1]
else:
    media = media_prop_m3[m-1]
    desvio_padrao = dp_amost_prop_m3[m-1]
estimativa_media = dado / media
limite_inferior = media - ((1.96 * desvio_padrao) / 3)
limite_superior = media + ((1.96 * desvio_padrao) / 3)

total_maximo = dado / limite_inferior
total_minimo = dado / limite_superior

nomes_meses = {1: "março", 2: "junho", 3: "setembro"}

if m == 1:
    print(f"\n>>> Estimativa para o nº de casos de dengue notificados, assumindo que a média do parâmetro m\n se aproxima de uma distribuição normal e que até {nomes_meses[n]} constam {dado} casos notificados:")
elif m == 2:
    print(f"\n>>> Estimativa para o nº de casos de dengue confirmados, assumindo que a média do parâmetro m\n se aproxima de uma distribuição normal e que até {nomes_meses[n]} constam {dado} casos confirmados:")
elif m == 3:
    print(f"\n>>> Estimativa para o nº de casos de dengue negativos, assumindo que a média do parâmetro m\n se aproxima de uma distribuição normal e que até {nomes_meses[n]} constam {dado} casos negativos:")
else:
    print(f"\n>>> Estimativa para o nº de óbitos associados a dengue, assumindo que a média do parâmetro m\n se aproxima de uma distribuição normal e que até {nomes_meses[n]} constam {dado} óbitos por dengue:")

print(f"Estimativa total: {int(estimativa_media)}")
print(f'Intervalo de 95 % de confiança estimado para o total estimado: ({int(total_minimo)}, {int(total_maximo)}).\n')
