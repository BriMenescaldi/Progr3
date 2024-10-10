"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from problem import OptProblem
from random import choice
from time import time


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local 
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            else:

                actual = problem.result(actual, act)
                value = value + diff[act]
                self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""

    def solve(self, problem: OptProblem):
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        #Iniciar una lista donde guardar los maximos locales y un contador, así como el limite
        maximosLocales = {}
        limite = 20

        numeroReseteos = 0

        while numeroReseteos <= limite:
            # Determinar las acciones que se pueden aplicar y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val == max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:

                #maximos locales = {'valorObjetivo': 'estado'}
                #print(value)

                maximosLocales[value] = actual

                #reseteo el actual
                actual = problem.random_reset()
                value = problem.obj_val(actual)

                numeroReseteos += 1
                self.niters += 1
                continue

            # Sino, nos movemos al sucesor
            else:

                actual = problem.result(actual, act)
                value = problem.obj_val(actual)
                self.niters += 1
                continue


        #Una vez terminado el bucle, busco el mejor maximo local

        lista = []
        for valor, estado in maximosLocales.items():
            lista.append(valor)

        #elijo el que tiene un menor valor
        mejor = max(lista)

        #seteo el resultado y el costo
        end = time()
        self.time = end - start
        self.tour = maximosLocales[mejor]
        self.value = mejor

        return


class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""
    def solve(self, problem: OptProblem):
        start = time()
        actual = problem.init
        value = problem.obj_val(problem.init)
        limite = 1000
        mejor = actual
        tabu = []
        tabuLimite = 50

        while self.niters <= limite:
            #actoar tabu aca
            #Determino las acciones posibles
            diff = problem.val_diff(actual)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val == max(diff.values()) and act not in tabu]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            #Comprobar si el que tenemos es menor que el nuevo
            #Si el nuevo es mayor, actualizar el mejor
            if problem.obj_val(mejor) < problem.obj_val(problem.result(actual, act)):
                mejor = problem.result(actual, act)

            accionInversa = (act[1], act[0])

            if len(tabu) == tabuLimite:
                tabu.pop(0) #Saco el primero agregado
            tabu.append(accionInversa)

            actual = problem.result(actual, act)
            value = problem.obj_val(actual)
            self.niters += 1

        end = time()
        self.time = end - start
        self.tour = mejor
        self.value = problem.obj_val(mejor)

        return