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
                 "Color": "gray",
                 "r": 0.8}

    portrayal2 = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "black",
                 "r": 0.2}

    portrayal3 = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "blue",
                 "r": 0.5}

    portrayal4 = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "black",
                 "r": 0}
    if agent.tipo == 1: # robot normal
        return portrayal
    elif agent.tipo == 0: # sucio
        return portrayal2
    elif agent.tipo == 3: # robot limpiando
        return portrayal3
    else:
        return portrayal4 # limpio

ancho = 10
alto = 10
agentes = 3
porcentaje_sucias = .20
pasos = 10
grid = CanvasGrid(agent_portrayal, ancho, alto, 750, 750)
server = ModularServer(LimpiezaModel,
                       [grid],
                       "Robot de Limpieza",
                       {"width":ancho, "height":alto, "agents": agentes, "dirty": porcentaje_sucias, "steps": pasos})
server.port = 8521 # The default
server.launch()
