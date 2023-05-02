import pulp
import random
import matplotlib.pyplot as plt
import csv
import pandas as pd
from datetime import datetime
import matplotlib as mpl
import alert
from flask import Flask, request, render_template_string, redirect, url_for
import os

def exibir_grafico(resultados, produtos_mes, vazamento_agua, agua_sobrando, mes):
    areas = [f'Área 1 ({produtos_mes["X1"]})', f'Área 2 ({produtos_mes["X2"]})', f'Área 3 ({produtos_mes["X3"]})',
             'Vazamento', 'Sobrando']
    quantidades = [resultados[0], resultados[1], resultados[2], vazamento_agua, agua_sobrando]

    plt.bar(areas, quantidades)
    plt.xlabel('Áreas e situações')
    plt.ylabel('Quantidade de água (litros)')
    plt.title('Quantidade de água utilizada por área')
    plt.xticks(rotation=45)  # Ajuste a rotação dos rótulos do eixo x para evitar sobreposição
    # Cria a pasta "graficos" se ela não existe
    if not os.path.exists('static/graficos'):
        os.makedirs('static/graficos')

    # Salva o gráfico em um arquivo PNG com o nome do mês e a hora atual
    now = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    filename = f'static/graficos/{mes}_{now.replace("/", "-").replace(":", "-")}.png'
    plt.savefig(filename)
    mpl.rcParams['font.size'] = 10
    plt.show()


def exibir_grafico_interativo(valores, produtos, vazamento_agua, agua_sobrando, mes, restricoes):
    df = pd.read_csv('resultados_agricultura.csv', encoding='ISO-8859-1')
    fig = px.line(df, x='Mes', y=['Area 1', 'Area 2', 'Area 3', 'Vazamento', 'Sobrando'],
                  title='Quantidade de água utilizada por área')
    fig.update_layout(xaxis_title='Mês', yaxis_title='Quantidade de água (litros)')
    for i, (area, valor) in enumerate(zip(["Área 1", "Área 2", "Área 3"], valores)):
        if valor < restricoes[area.lower()]["min"]:
            alert(f"A restrição de gasto mínimo para {area} foi violada!")
        elif valor > restricoes[area.lower()]["max"]:
            alert(f"A restrição de gasto máximo para {area} foi violada!")
    pio.show(fig)


# exibir_grafico_interativo()

def salvar_resultados_csv(mes, resultados, produtos_mes, vazamento_agua, agua_sobrando):
    filename = 'resultados_agricultura.csv'
    header = ['Mes', 'Area 1', 'Produto A1', 'Area 2', 'Produto A2', 'Area 3', 'Produto A3', 'Vazamento', 'Sobrando']
    row = [mes, resultados[0], produtos_mes["X1"], resultados[1], produtos_mes["X2"], resultados[2], produtos_mes["X3"],
           vazamento_agua, agua_sobrando]

    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(header)

    with open(filename, mode='a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(row)


def resolve_otimizacao(restricoes_mes, produtos_mes):
    vazamento_agua = random.randint(1, 100)
    print(f"Vazamento de água: {vazamento_agua} litros")
    agua_disponivel = 1000 - vazamento_agua

    total_minimo = sum([restricoes_mes[k][0] for k in restricoes_mes])
    proporcao = agua_disponivel / total_minimo

    restricoes_atualizadas = {}
    for k, (minimo, maximo) in restricoes_mes.items():
        minimo_novo = minimo * proporcao
        restricoes_atualizadas[k] = (minimo_novo, maximo)

    prob = pulp.LpProblem("Minimizar_desperdicio_de_agua", pulp.LpMinimize)

    X1 = pulp.LpVariable("X1", lowBound=restricoes_atualizadas["X1"][0], upBound=restricoes_atualizadas["X1"][1],
                         cat="Continuous")
    X2 = pulp.LpVariable("X2", lowBound=restricoes_atualizadas["X2"][0], upBound=restricoes_atualizadas["X2"][1],
                         cat="Continuous")
    X3 = pulp.LpVariable("X3", lowBound=restricoes_atualizadas["X3"][0], upBound=restricoes_atualizadas["X3"][1],
                         cat="Continuous")

    prob += X1 + X2 + X3 <= agua_disponivel, "Restricao_volume_total"

    minimo_agua = sum([restricoes_atualizadas[k][0] for k in restricoes_atualizadas])
    prob += X1 + X2 + X3 - minimo_agua, "Desperdicio_de_agua"
    prob += X1 + X2 + X3 <= agua_disponivel - 1, "Restricao_agua_sobrando"

    prob.solve()

    agua_sobrando = agua_disponivel - (X1.varValue + X2.varValue + X3.varValue)
    desperdicio_total = prob.objective.value() + vazamento_agua

    print("Status:", pulp.LpStatus[prob.status])
    print(f"Área 1 ({produtos_mes['X1']}):", X1.varValue, "litros")
    print(f"Área 2 ({produtos_mes['X2']}):", X2.varValue, "litros")
    print(f"Área 3 ({produtos_mes['X3']}):", X3.varValue, "litros")
    totalAguaConsumida = X1.varValue + X2.varValue + X3.varValue
    print(f"Total de água consumida:", totalAguaConsumida, "litros")
    print("Água sobrando:", agua_sobrando, "litros")
    print("Desperdício total de água (incluindo vazamento):", desperdicio_total, "litros")
    exibir_grafico((X1.varValue, X2.varValue, X3.varValue), produtos_mes, vazamento_agua, agua_sobrando, mes)
    salvar_resultados_csv(mes, (X1.varValue, X2.varValue, X3.varValue), produtos_mes, vazamento_agua, agua_sobrando)


restricoes = {
    "abril": {"X1": (200, 400), "X2": (300, 500), "X3": (300, 500)},
    "setembro": {"X1": (300, 400), "X2": (300, 400), "X3": (200, 400)},
    "dezembro": {"X1": (200, 300), "X2": (300, 500), "X3": (400, 500)},
    "outros": {"X1": (300, 500), "X2": (200, 400), "X3": (200, 400)}
}

produtos = {
    "abril": {"X1": "Feijão", "X2": "Algodão", "X3": "Cevada"},
    "setembro": {"X1": "Canola", "X2": "Beterraba", "X3": "Soja"},
    "dezembro": {"X1": "Girassol", "X2": "Feijão", "X3": "Milho"},
    "outros": {"X1": "Café", "X2": "Sorgo", "X3": "Cana-de-açúcar"}
}

mes = input("Digite o mês de plantio (exemplo: abril, setembro, dezembro, outros): ").lower()

if mes not in restricoes:
    print("Mês inválido. Use 'abril', 'setembro', 'dezembro' ou 'outros'.")
else:
    resolve_otimizacao(restricoes[mes], produtos[mes])
