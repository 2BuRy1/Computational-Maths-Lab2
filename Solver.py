import math
import sympy as sp


def solve(data):
    if data[0]:
        return solve_system(data)
    else:
        return solve_equation(data)


def parse_interval(interval_str):
    try:
        a, b = map(float, interval_str.replace(",", ".").split(';'))
        return a, b
    except ValueError:
        raise ValueError("Некорректный формат интервала. Введите два числа через запятую.")


def check_root_existence(f, a, b):
    if f(a) * f(b) > 0:
        return "На данном интервале нет корня или несколько. Выберите другой интервал."
    return None


def solve_by_hord(data):
    equation, interval_str, precision_str = data[1], data[3], data[4]
    a, b = parse_interval(interval_str)
    eps = float(precision_str.replace(",", "."))

    equation = equation.split("=")[0].strip().replace("^", "**")

    f = lambda x: eval(equation, {"x": x, "sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log, "e" : math.e})
    root_check = check_root_existence(f, a, b)
    if root_check:
        return root_check

    iterations = 0
    while abs(b - a) > eps:
        x_i = a - (b - a) / (f(b) - f(a)) * f(a)
        if f(x_i) == 0:
            result = f"Решение: {x_i}, Значение функции: {f(x_i)}, Количество итераций: {iterations}"
            return result
        elif f(a) * f(x_i) < 0:
            b = x_i
        else:
            a = x_i
        iterations += 1
    result = f"Решение: {x_i}, Значение функции: {f(x_i)}, Количество итераций: {iterations}"
    return result


def solve_by_sec(data):
    equation, interval_str, precision_str = data[1], data[3], data[4]
    a, b = parse_interval(interval_str)
    eps = float(precision_str.replace(",", "."))

    equation = equation.split("=")[0].strip().replace("^", "**")

    f = lambda x: eval(equation, {"x": x, "sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log , "e" : math.e})
    root_check = check_root_existence(f, a, b)
    if root_check:
        return root_check

    x0, x1 = a, b
    iterations = 0
    while abs(x1 - x0) > eps:
        x_new = x1 - (x1 - x0) / (f(x1) - f(x0)) * f(x1)
        x0, x1 = x1, x_new
        iterations += 1
    result = f"Решение: {x1}, Значение функции: {f(x1)}, Количество итераций: {iterations}"
    return result


def symbolic_derivative(equation):
    x = sp.Symbol('x')
    expr = sp.sympify(equation)
    derivative_expr = sp.diff(expr, x)
    return sp.lambdify(x, derivative_expr, modules=['math'])


def solve_by_iterations(data):
    equation, interval_str, precision_str = data[1], data[3], data[4]
    a, b = parse_interval(interval_str)
    eps = float(precision_str.replace(",", "."))

    equation = equation.split("=")[0].strip().replace("^", "**")

    f = lambda x: eval(equation, {"x": x, "sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log, "e" : math.e})
    df = symbolic_derivative(equation)
    maxEl = max(df(a)), df(b)
    lamda = 1 / max(abs(df(a)), abs(df(b)))
    if maxEl > 0:   lamda = -1 / max(abs(df(a)), abs(df(b)))
    phi = lambda x: x + lamda * f(x)
    dphi = lambda x: 1 + lamda * df(x)

    root_check = check_root_existence(f, a, b)
    if root_check:
        return root_check

    q = max(abs(dphi(a)), abs(dphi(b)))
    if q >= 1:
        return "Метод простой итерации не сходится на данном интервале. Выберите другой метод или интервал."

    x_i = a
    iterations = 0
    while abs(f(x_i)) > eps:
        x_i = phi(x_i)
        iterations += 1

    result = f"Решение: {x_i}, Значение функции: {f(x_i)}, Количество итераций: {iterations}"
    return result



def solve_equation(data):
    if data[2] == "Метод Хорд":
        return solve_by_hord(data)
    elif data[2] == "Метод Cекущих":
        return solve_by_sec(data)
    elif data[2] == "Метод простых итераций":
        return solve_by_iterations(data)
    else:
        return "Неизвестный метод."


def check_convergence(phi_functions, initial_guess):


    x1, x2 = sp.symbols('x1 x2')


    def symbolic_phi1(x1, x2):
        return -0.15 * x1 ** 2 - 0.25 * x2 ** 2 + 0.4

    def symbolic_phi2(x1, x2):
        return -0.3 * x1 ** 2 - 0.2 * x1 * x2 + 0.6

    def symbolic_phi3(x1, x2):
        return (1 - sp.cos(x2)) / 0.8

    def symbolic_phi4(x1, x2):
        return 4 - 2 * x1 ** 2


    if phi_functions == [system1_phi1, system1_phi2]:
        phi_expressions = [symbolic_phi1(x1, x2), symbolic_phi2(x1, x2)]
    else:
        phi_expressions = [symbolic_phi3(x1, x2), symbolic_phi4(x1, x2)]

    jacobian_matrix = [[sp.diff(phi_expressions[i], var) for var in (x1, x2)] for i in range(2)]


    x1_val, x2_val = initial_guess
    jacobian_values = [[float(jacobian_matrix[i][j].subs({x1: x1_val, x2: x2_val})) for j in range(2)] for i in range(2)]

    max_row_sum = max(sum(abs(jacobian_values[i][j]) for j in range(2)) for i in range(2))
    return max_row_sum < 1


def system1_phi1(x1, x2):
    return -0.15 * x1 ** 2 - 0.25 * x2 ** 2 + 0.4


def system1_phi2(x1, x2):
    return -0.3 * x1 ** 2 - 0.2 * x1 * x2 + 0.6


def system2_phi1(x1, x2):
    return (1 - math.cos(x2)) / 0.8

def system2_phi2(x1, x2):
    return 4 - 2 * x1**2

def solve_system(data):
    system_choice = data[1]
    initial_guess = parse_interval(data[2])
    epsilon = float(data[3].replace(",", "."))

    if system_choice == "0.15x1^2 + 0.25x2^2 + x1 - 0.4 = 0, 0.3x1^2 + 0.2x1x2 + x2 - 0.6 = 0":
        phi_functions = [system1_phi1, system1_phi2]
    elif system_choice == "0.8x1 + cos(x2) -1 = 0, x1^2 + 0.5x2 - 2 = 0":
        phi_functions = [system2_phi1, system2_phi2]
    else:
        return "Неизвестная система уравнений."

    if not check_convergence(phi_functions, initial_guess):
        return "Метод простой итерации не сходится. Выберите другой метод или интервал."

    x_k = initial_guess[:]
    iterations = 0

    while True:
        x_k1 = [phi(x_k[0], x_k[1]) for phi in phi_functions]
        error = [abs(x_k1[i] - x_k[i]) for i in range(2)]
        iterations += 1

        if max(error) <= epsilon:
            break

        x_k = x_k1[:]

    return {"Решение": x_k1, "Число итераций": iterations, "Погрешность": error}