from pulp import LpVariable, LpProblem, LpAffineExpression
from pulp.constants import LpMinimize, LpMaximize

#  Создание задачи ЛП сложный процесс, можно использовать паттерн Строитель.

#  Создание переменной с ограничением снизу
x = LpVariable("x", lowBound=0)
#  Нужна функция для динамического создания переменных типа:
LpVariable('x{}'.format(0), lowBound=0)
#  Структура для хранения таких переменных dict, словарь

#  Создание типа задачи
problem = LpProblem('Задача 1', LpMinimize)
# problem = LpProblem('Задача 2', LpMaximize)

#  Создание целевой функции
problem += LpAffineExpression('Список кортежей: [(x[0],1), (x[1],-3), (x[2],4)]'), 'Функция цели'

#  Создание ограничений
problem += LpAffineExpression('Список кортежей: [(x[0],1), (x[1],-3), (x[2],4)]') == 3, str('0, индекс условия')
#  В задаче может быть несколько типов ограничений: <, <=, >, >=, =.
#  Для создания ограничению следует использовать фабрику.

#  Решение задачи ЛП
problem.solve()

#  Получить результаты решения
variables = problem.variables()  # Значения всех переменных
variables[0].name  # Получить имя переменной
variables[0].varValue  # Получить значение переменной
