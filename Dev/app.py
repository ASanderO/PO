from scipy.optimize import linprog

# Definindo os coeficientes da função objetivo
c = [-50, -30, -20]  # Coeficientes negativos para maximizar

# Definindo a matriz de restrições
A = [[2, 1, 1], [1, 2, 1]]  # Coeficientes das restrições
b = [176, 132]  # Lados direitos das restrições

# Definindo os limites das variáveis
bounds = [(0, None), (0, None), (0, None)]  # Limites inferiores e superiores para as variáveis

# Resolvendo o problema de maximização
result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

# Verificando se a solução é ótima
if result.success:
    # Extraindo as quantidades de jogos, sistemas e sites produzidos
    x1, x2, x3 = result.x
    print("Quantidade de jogos produzidos:", int(x1))
    print("Quantidade de sistemas produzidos:", int(x2))
    print("Quantidade de sites produzidos:", int(x3))
    print("Lucro máximo:", -result.fun)  # Convertendo o valor negativo para positivo

    # Calculando as horas consumidas por cada equipe
    equipe1_horas = 2 * x1 + x2 + x3
    equipe2_horas = x1 + 2 * x2 + x3

    # Calculando as horas restantes por cada equipe
    equipe1_horas_restantes = 176 - equipe1_horas
    equipe2_horas_restantes = 132 - equipe2_horas

    print("Horas consumidas pela Equipe 1:", equipe1_horas)
    print("Horas consumidas pela Equipe 2:", equipe2_horas)
    print("Horas restantes da Equipe 1:", equipe1_horas_restantes)
    print("Horas restantes da Equipe 2:", equipe2_horas_restantes)
else:
    print("O problema não possui solução ótima.")
