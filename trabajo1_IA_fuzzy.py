import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

# Definición del universo alineado con las propiedades de la ontología
#Variable de entrada
poder = ctrl.Antecedent(np.arange(0, 101, 1), 'poder')             
amenaza = ctrl.Antecedent(np.arange(0, 11, 1), 'amenaza')           
popularidad = ctrl.Antecedent(np.arange(0, 101, 1), 'popularidad')

#Variable de salida
perfil_impacto = ctrl.Consequent(np.arange(0, 101, 1), 'perfil_impacto') 

#Funciones de pertenencia y modificadores
#Variables de entrada
poder['Bajo'] =  fuzzy.trimf(poder.universe, [0, 0, 35])
poder['Medio'] = fuzzy.trapmf(poder.universe, [25, 35, 65, 70])
poder['Alto'] =  fuzzy.gaussmf(poder.universe, 100, 12)
poder['Muy_Alto'] = poder['Alto'].mf**2  # Modificador de concentración
poder['Ligeramente_Alto'] = np.sqrt(poder['Alto'].mf)  # Modificador de dilatación

amenaza['Baja'] = fuzzy.trapmf(amenaza.universe, [0, 0, 2, 3])
amenaza['Media'] = fuzzy.gaussmf(amenaza.universe, 5, 1)
amenaza['Alta'] = fuzzy.trimf(amenaza.universe, [7, 10, 10])
amenaza['Muy_Alta'] = amenaza['Alta'].mf**2 # Modificador de concentración
amenaza['Ligeramente_Alta'] = np.sqrt(amenaza['Alta'].mf) # Modificador de dilatación

popularidad['Baja'] = fuzzy.trimf(popularidad.universe, [0, 0, 30])
popularidad['Media'] = fuzzy.gaussmf(popularidad.universe, 50, 10)
popularidad['Alta'] =  fuzzy.trapmf(popularidad.universe, [70, 80, 100, 100])
popularidad['Muy_Alta'] = popularidad['Alta'].mf**2 # Modificador de concentración

# Usado para desempatar 2 personajes al final 
# Variable de salida 
perfil_impacto['Callejero'] = fuzzy.trapmf(perfil_impacto.universe, [0, 0, 10, 30])
perfil_impacto['Global'] = fuzzy.trimf(perfil_impacto.universe, [30, 50, 70])
perfil_impacto['Cosmico'] = fuzzy.gaussmf(perfil_impacto.universe, 100, 7)

# Reglas difusas 
reglas_difusas = [
    # Regla 1: Intersección (AND)
    ctrl.Rule(poder['Bajo'] & amenaza['Baja'], perfil_impacto['Callejero']),

    # Regla 2: Intersección (AND) con Modificadores ("Muy")
    ctrl.Rule(poder['Muy_Alto'] & amenaza['Muy_Alta'], perfil_impacto['Cosmico']),

    # Regla 3: Intersección (AND) y Unión (OR) combinadas
    ctrl.Rule(popularidad['Alta'] & (poder['Medio'] | amenaza['Media']), perfil_impacto['Global']),

    # Regla 4: Negación (NOT ~) + Intersección (AND)
    ctrl.Rule(~popularidad['Alta'] & poder['Bajo'], perfil_impacto['Callejero']),

    # Regla 5: Unión (OR) con Modificadores ("Ligeramente" y "Muy")
    ctrl.Rule(poder['Ligeramente_Alto'] | popularidad['Muy_Alta'], perfil_impacto['Global']),

    # Regla 6: Intersección (AND) y Negación (NOT ~)
    ctrl.Rule(amenaza['Alta'] & ~poder['Bajo'], perfil_impacto['Cosmico']),

    # Regla 7: Intersección (AND) 
    ctrl.Rule(poder['Medio'] & popularidad['Baja'], perfil_impacto['Callejero']),

    # Regla 8: Intersección (AND) con Modificador en amenaza
    ctrl.Rule(popularidad['Alta'] & amenaza['Muy_Alta'], perfil_impacto['Cosmico']),

    # Regla 9: Múltiple Negación (NOT ~) e Intersección (AND)
    ctrl.Rule(~amenaza['Alta'] & ~poder['Alto'] & popularidad['Media'], perfil_impacto['Global'])
]

# Creación del sistema con la lista de Reglas difusas
sistema_control_difuso = ctrl.ControlSystem(reglas_difusas)

# Esta función toma los valores de poder, amenaza y popularidad de los personajes restantes 
# en el desempate difuso y los valores ingresados por el usuario 
def evaluar_perfil_difuso(v_poder, v_amenaza, v_popularidad):
    # Ejecuta la inferencia difusa y retorna la defuzzificación por Centroide (0 a 100).
    simulador = ctrl.ControlSystemSimulation(sistema_control_difuso)
    simulador.input['poder'] = float(v_poder)
    simulador.input['amenaza'] = float(v_amenaza)
    simulador.input['popularidad'] = float(v_popularidad)
    simulador.compute()
    return simulador.output['perfil_impacto']

# Ejemplo de prueba rápida en la celda:
score_ejemplo = evaluar_perfil_difuso(64, 5, 100)
print(f"Spiderman {score_ejemplo}")