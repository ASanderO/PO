from pulp import *

# Cria o problema para maximização
prob = LpProblem("MaximizarLucro", LpMaximize)

# Define as variáveis de decisão
X1 = LpVariable("jogos", lowBound=0, cat='Integer')
X2 = LpVariable("sistemas", lowBound=0, cat='Integer')
X3 = LpVariable("sites", lowBound=0, cat='Integer')

# Define a função objetivo a ser maximizada
prob += 50*X1 + 30*X2 + 20*X3

# Define as restrições de capacidade da equipe 1 e 2
prob += 2*X1 + X2 + X3 <= 176
prob += X1 + 2*X2 + X3 <= 132

prob += X1 >= 0
prob += X2 >= 0
prob += X3 >= 0

# Resolve o problema
prob.solve()

# Imprime o status da solução
print("Status da solução:", LpStatus[prob.status])

# Imprime o valor ótimo da função objetivo
print("Valor ótimo da função objetivo:", value(prob.objective))

# Imprime as horas gastas e restantes para produção dos projetos
print("Horas gastas e restantes:")
print("Equipe 1: gastas =", 2*X1.value() + X2.value() + X3.value(), "restantes =", 176 - (2*X1.value() + X2.value() + X3.value()))
print("Equipe 2: gastas =", X1.value() + 2*X2.value() + X3.value(), "restantes =", 132 - (X1.value() + 2*X2.value() + X3.value()))
print("Quantidades produzidas:")
print("Jogos =", X1.value())
print("Sistemas =", X2.value())
print("Sites =", X3.value())
