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

    
    # TABELA NÚMERO DE CASOS NOTIFICADOS POR MÊS

    notificados_por_mes = [info_por_mes[i][0] for i in range(12)]
    total_notificados = sum(notificados_por_mes)

    meses_com_total = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', 'Total']
    notificados_com_total = notificados_por_mes + [total_notificados]

    df_notificados = pd.DataFrame({
        "Mês": meses_com_total,
        "Notificados": notificados_com_total
    })

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.axis('off')

    tabela = ax.table(
        cellText=df_notificados.values,
        colLabels=df_notificados.columns,
        loc='center',
        cellLoc='center'
    )

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(12)
    tabela.scale(1.2, 1.2)

    total_row = len(df_notificados)
    for col in range(2):
        cell = tabela[total_row, col]
        cell.set_fontsize(12)
        cell.set_text_props(weight='bold')

    plt.title(f"Tabela do número de Casos Notificados por Mês em {ano}", fontsize=14, pad=20)
    plt.tight_layout()
    plt.show()


    # TABELA CONFIRMADOS POR MÊS E FAIXA ETÁRIA

    dados_confirmados = {
        cat: [info_por_mes_e_fx_et[mes][cat][1] for mes in range(12)]
        for cat in fx_et
    }
    df_confirmados = pd.DataFrame(dados_confirmados)
    df_confirmados.index = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

    subtotal = df_confirmados.sum()
    df_confirmados.loc['Subtotal'] = subtotal

    df_confirmados["Subtotal"] = df_confirmados.sum(axis=1)

    subtotal_colunas = df_confirmados.sum(axis=0)

    fig, ax = plt.subplots(figsize=(18, 6))
    ax.axis('off')

    tabela = ax.table(
        cellText=df_confirmados.values,
        rowLabels=df_confirmados.index,
        colLabels=df_confirmados.columns,
        loc='center',
        cellLoc='center'
    )

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)
    tabela.scale(1.2, 1.2)

    num_rows, num_cols = df_confirmados.shape
    for col in range(num_cols):
        tabela[num_rows, col].set_text_props(weight='bold')
    for row in range(num_rows + 1):
        tabela[row, num_cols - 1].set_text_props(weight='bold')

    plt.title(f"Tabela de casos Confirmados por Faixa Etária e Mês em {ano}", fontsize=14, pad=20)
    plt.tight_layout()
    plt.show()


    # GRÁFICO DE LINHAS

    df_plot = df_confirmados.drop(index='Subtotal')
    df_plot = df_plot.drop(columns='Subtotal')

    plt.figure(figsize=(14, 6))

    for faixa in df_plot.columns:
        plt.plot(df_plot.index, df_plot[faixa], marker='o', label=faixa)

    plt.title(f"Gráfico de casos Confirmados por Faixa Etária e Mês em {ano}")
    plt.xlabel("Mês")
    plt.ylabel("Número de Casos Confirmados")

    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # <- AQUI

    plt.legend(title="Faixa Etária", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


    # TABELA NÚMERO DE ÓBITOS POR MÊS E ANO

    obitos_por_mes = [info_por_mes[i][3] for i in range(12)]
    total_obitos = sum(obitos_por_mes)

    meses_com_total = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', 'Total']
    obitos_com_total = obitos_por_mes + [total_obitos]

    df_obitos = pd.DataFrame({
        "Mês": meses_com_total,
        "Óbitos": obitos_com_total
    })

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.axis('off')

    tabela = ax.table(
        cellText=df_obitos.values,
        colLabels=df_obitos.columns,
        loc='center',
        cellLoc='center'
    )

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(12)
    tabela.scale(1.2, 1.2)

    total_row = len(df_obitos)
    for col in range(2):
        cell = tabela[total_row, col]
        cell.set_fontsize(12)
        cell.set_text_props(weight='bold')

    plt.title(f"Tabela do número de Óbitos por Mês em {ano}", fontsize=14, pad=20)
    plt.tight_layout()
    plt.show()
    
    print('-'*150)
    return ano, [info_por_mes_e_fx_et, info_por_mes, total_notificados, total_confirmados, total_negativos, total_obitos]

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

for ano, dados in sorted(dados_gerais.items()):
    info_por_mes_e_fx_et, info_por_mes, notificados, confirmados, negativos, obitos = dados
    total_notificados_geral += notificados
    total_confirmados_geral += confirmados
    total_negativos_geral += negativos
    total_obitos_geral += obitos
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


# TABELA DO NÚMERO DE CASOS NOTIFICADOS POR MÊS (ACUMULADO)

notificados_por_mes = [info_por_mes_acumulado[i][0] for i in range(12)]
total_notificados = sum(notificados_por_mes)

meses_com_total = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', 'Total']
notificados_com_total = notificados_por_mes + [total_notificados]

df_notificados = pd.DataFrame({
    "Mês": meses_com_total,
    "Notificados": notificados_com_total
})

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.axis('off')

tabela = ax.table(
    cellText=df_notificados.values,
    colLabels=df_notificados.columns,
    loc='center',
    cellLoc='center'
)

tabela.auto_set_font_size(False)
tabela.set_fontsize(12)
tabela.scale(1.2, 1.2)

total_row = len(df_notificados)
for col in range(2):
    cell = tabela[total_row, col]
    cell.set_fontsize(12)
    cell.set_text_props(weight='bold')

plt.title("Tabela do número de Casos Notificados por Mês (Acumulado)", fontsize=14, pad=20)
plt.tight_layout()
plt.show()


# TABELA DE CASOS CONFIRMADOS POR MÊS E FAIXA ETÁRIA (ACUMULADO)

dados_confirmados = {
    cat: [info_por_mes_e_fx_et_acumulado[mes][cat][1] for mes in range(12)]
    for cat in fx_et_completa
}
df_confirmados = pd.DataFrame(dados_confirmados)
df_confirmados.index = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# Soma por coluna (total por faixa etária)
subtotal = df_confirmados.sum()
df_confirmados.loc['Subtotal'] = subtotal

# Soma por linha (total por mês)
df_confirmados["Subtotal"] = df_confirmados.sum(axis=1)

fig, ax = plt.subplots(figsize=(18, 6))
ax.axis('off')

tabela = ax.table(
    cellText=df_confirmados.values,
    rowLabels=df_confirmados.index,
    colLabels=df_confirmados.columns,
    loc='center',
    cellLoc='center'
)

tabela.auto_set_font_size(False)
tabela.set_fontsize(10)
tabela.scale(1.2, 1.2)

num_rows, num_cols = df_confirmados.shape
for col in range(num_cols):
    tabela[num_rows, col].set_text_props(weight='bold')
for row in range(num_rows + 1):
    tabela[row, num_cols - 1].set_text_props(weight='bold')

plt.title("Tabela de casos Confirmados por Faixa Etária e Mês (Acumulado)", fontsize=14, pad=20)
plt.tight_layout()
plt.show()


# GRÁFICO DE LINHAS DE CASOS CONFIRMADOS POR FAIXA ETÁRIA AO LONGO DOS MESES (ACUMULADO)

df_plot = df_confirmados[fx_et].drop(index='Subtotal')

plt.figure(figsize=(14, 6))

for faixa in df_plot.columns:
    plt.plot(df_plot.index, df_plot[faixa], marker='o', label=faixa)

plt.title("Gráfico de casos Confirmados por Faixa Etária e Mês (Acumulado)")
plt.xlabel("Mês")
plt.ylabel("Número de Casos Confirmados")

plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

plt.legend(title="Faixa Etária", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# NÚMERO DE ÓBITOS POR MÊS (ACUMULADO)

obitos_por_mes = [info_por_mes_acumulado[i][3] for i in range(12)]
total_obitos = sum(obitos_por_mes)

meses_com_total = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', 'Total']
obitos_com_total = obitos_por_mes + [total_obitos]

df_obitos = pd.DataFrame({
    "Mês": meses_com_total,
    "Óbitos": obitos_com_total
})

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.axis('off')

tabela = ax.table(
    cellText=df_obitos.values,
    colLabels=df_obitos.columns,
    loc='center',
    cellLoc='center'
)

tabela.auto_set_font_size(False)
tabela.set_fontsize(12)
tabela.scale(1.2, 1.2)

total_row = len(df_obitos)
for col in range(2):
    cell = tabela[total_row, col]
    cell.set_fontsize(12)
    cell.set_text_props(weight='bold')

plt.title("Tabela do número de Óbitos por Mês (Acumulado)", fontsize=14, pad=20)
plt.tight_layout()
plt.show()

print('=' * 150)
