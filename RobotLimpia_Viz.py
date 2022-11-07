"""
Visualizador del Juego de la Vida
Autor: Jorge Rmz Uresti
Octubre 8, 2021
"""
from RobotLimpia import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "false",
                 "Layer": 0,
                 "Color": "blue",
                 "r": 0.5}

    portrayal2 = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "black",
                 "r": 0.3}

    portrayal3 = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "black",
                 "r": 0}
    if agent.tipo == 1:
        return portrayal
    elif agent.tipo == 0:
        return portrayal2
    else:
        return portrayal3

ancho = 20
alto = 20
grid = CanvasGrid(agent_portrayal, ancho, alto, 750, 750)
server = ModularServer(LimpiezaModel,
                       [grid],
                       "Robot de Limpieza",
                       {"width":ancho, "height":alto})
server.port = 8521 # The default
server.launch()
