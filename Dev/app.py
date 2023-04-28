from flask import Flask, render_template, request
from pulp import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def form_post():
    if request.method == 'POST':
        # Obter as entradas do formulário
        equipe1 = int(request.form['equipe1'])
        equipe2 = int(request.form['equipe2'])
        habilidades = request.form.getlist('habilidades')

        # Definir as capacidades dos funcionários
        alex_capacidade = {'jogos': 2, 'sistemas': 1, 'sites': 1}
        devjr1_capacidade = {'jogos': 1, 'sistemas': 2, 'sites': 1}
        devsr1_capacidade = {'jogos': 1, 'sistemas': 1, 'sites': 2}
        hayana_capacidade = {'jogos': 2, 'sistemas': 1, 'sites': 1}
        devjr2_capacidade = {'jogos': 1, 'sistemas': 2, 'sites': 1}
        devsr2_capacidade = {'jogos': 1, 'sistemas': 1, 'sites': 2}

        # Criar o problema de programação linear
        prob = LpProblem("Produção de software", LpMaximize)

        x1 = LpVariable("jogos", 0, None, LpInteger)
        x2 = LpVariable("sistemas", 0, None, LpInteger)
        x3 = LpVariable("sites", 0, None, LpInteger)

        # Definir a função objetivo
        prob += 50 * x1 + 30 * x2 + 20 * x3, "Lucro líquido"

        # Definir as restrições
        # Equipe 1
        prob += 2 * alex_capacidade['jogos'] * x1 + devjr1_capacidade['sistemas'] * x2 + devsr1_capacidade[
            'sites'] * x3 <= equipe1, "Capacidade da equipe 1"
        # Equipe 2
        prob += hayana_capacidade['jogos'] * x1 + 2 * devjr2_capacidade['sistemas'] * x2 + devsr2_capacidade[
            'sites'] * x3 <= equipe2, "Capacidade da equipe 2"

        # Verificar se algum funcionário está faltando
        if len(habilidades) < 6:
            # Definir as capacidades dos funcionários faltantes
            faltantes_capacidade = {}
            if 'alex' not in habilidades:
                faltantes_capacidade['alex'] = {'jogos': 2, 'sistemas': 1, 'sites': 1}
            if 'devjr1' not in habilidades:
                faltantes_capacidade['devjr1'] = {'jogos': 1, 'sistemas': 2, 'sites': 1}
            if 'devsr1' not in habilidades:
                faltantes_capacidade['devsr1'] = {'jogos': 1, 'sistemas': 1, 'sites': 2}
            if 'hayana' not in habilidades:
                faltantes_capacidade['hayana'] = {'jogos': 2, 'sistemas': 1, 'sites': 1}
            if 'devjr2' not in habilidades:
                faltantes_capacidade['devjr2'] = {'jogos': 1, 'sistemas': 2, 'sites': 1}
            if 'devsr2' not in habilidades:
                faltantes_capacidade['devsr2'] = {'jogos': 1, 'sistemas': 1, 'sites': 2}

            # Definir as variáveis dos funcionários faltantes
            faltantes_vars = []
            for funcionario in faltantes_capacidade.keys():
                for projeto in faltantes_capacidade[funcionario].keys():
                    var_name = f"{funcionario}_{projeto}"
                    var = LpVariable(var_name, 0, None, LpInteger)
                    faltantes_vars.append(var)

                    # Adicionar as restrições de capacidade das equipes
                    prob += 2 * x1_vars[0] + x2_vars[0] + x3_vars[0] <= 176, "Horas disponíveis da equipe 1"
                    prob += x1_vars[1] + 2 * x2_vars[1] + x3_vars[1] <= 132, "Horas disponíveis da equipe 2"

                    # Adicionar as capacidades dos funcionários faltantes às restrições
                    for funcionario in faltantes_capacidade.keys():
                        for projeto in faltantes_capacidade[funcionario].keys():
                            var_name = f"{funcionario}_{projeto}"
                            coeficiente = faltantes_capacidade[funcionario][projeto]
                            if funcionario == 'alex':
                                prob += 2 * coeficiente * x1 <= lpSum([var for var in faltantes_vars if
                                                                       var.name == var_name]), f"Capacidade de {funcionario} no projeto de {projeto}"
                            elif funcionario == 'devjr1':
                                prob += coeficiente * x2 <= lpSum([var for var in faltantes_vars if
                                                                   var.name == var_name]), f"Capacidade de {funcionario} no projeto de {projeto}"
                            elif funcionario == 'devsr1':
                                prob += coeficiente * x3 <= lpSum([var for var in faltantes_vars if
                                                                   var.name == var_name]), f"Capacidade de {funcionario} no projeto de {projeto}"
                            elif funcionario == 'hayana':
                                prob += coeficiente * x1 <= lpSum([var for var in faltantes_vars if
                                                                   var.name == var_name]), f"Capacidade de {funcionario} no projeto de {projeto}"
                            elif funcionario == 'devjr2':
                                prob += coeficiente * x2 <= lpSum([var for var in faltantes_vars if
                                                                   var.name == var_name]), f"Capacidade de {funcionario} no projeto de {projeto}"
                            elif funcionario == 'devsr2':
                                prob += coeficiente * x3 <= lpSum([var for var in faltantes_vars if
                                                                   var.name == var_name]), f"Capacidade de {funcionario} no projeto de {projeto}"

                    # Remover a capacidade dos funcionários faltantes das restrições originais
                    if 'alex' not in habilidades:
                        devjr1_vars = [var for var in prob.variables() if var.name == 'alex_jogos']
                        prob -= devjr1_vars
                    if 'devjr1' not in habilidades:
                        devjr1_vars = [var for var in prob.variables() if var.name == 'devjr1_sistemas']
                        prob -= devjr1_vars
                    if 'devsr1' not in habilidades:
                        devsr1_vars = [var for var in prob.variables() if var.name == 'devsr1_sites']
                        prob -= devsr1_vars
                    if 'hayana' not in habilidades:
                        hayana_vars = [var for var in prob.variables() if var.name == 'hayana_jogos']
                        prob -= hayana_vars
                    if 'devjr2' not in habilidades:
                        devjr2_vars = [var for var in prob.variables() if var.name == 'devjr2_sistemas']
                        prob -= devjr2_vars
                    if 'devsr2' not in habilidades:
                        devsr2_vars = [var for var in prob.variables() if var.name == 'devsr2_sites']
                        prob -= devsr2_vars

                # Resolver o problema de programação linear
            prob.solve()

            # Gerar o resultado
            if LpStatus[prob.status] == "Optimal":
                return render_template('result.html', x1=int(x1.varValue), x2=int(x2.varValue), x3=int(x3.varValue),
                                       lucro=int(value(prob.objective)), equipe_1_horas=176 - int(lpSum([2*x1 + x2 + x3 for x1, x2, x3 in zip(x1_vars, x2_vars, x3_vars)])),
                                       equipe_2_horas=132 - int(lpSum([x1 + 2*x2 + x3 for x1, x2, x3 in zip(x1_vars, x2_vars, x3_vars)])))
            else:
                return render_template('result.html', message="Não foi possível encontrar uma solução ótima.")
        else:
            return render_template('result.html', message="Não foi possível encontrar uma solução.")
    else:
        return render_template('form.html')


