"""
Visualizador de Limpieza con Robot
Autores: Jose Luis Madrigal y Cesar Emiliano Palome
Noviembre 9, 2022
"""
from RobotLimpia import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

def agent_portrayal(agent):
    '''
    Define el color que tendra cada agente en cierto estado.
    '''
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

ancho = 20
alto = 10
agentes = 8
porcentajeSucias = 0.40
pasos = 100
grid = CanvasGrid(agent_portrayal, ancho, alto, 750, 750)
totalMovementsGraph = ChartModule([{"Label": "Total Movements", "Color": "Red"}], data_collector_name='dataCollectorMovements')
totalDirtyGraph = ChartModule([{"Label": "Total Dirty", "Color": "Blue"}], data_collector_name='dataCollectorDirty')
server = ModularServer(LimpiezaModel,
                       [grid, totalMovementsGraph, totalDirtyGraph],
                       "Robot de Limpieza",
                       {"width":ancho, "height":alto, "agents": agentes, "dirty": porcentajeSucias, "steps": pasos})
server.port = 8521 # The default
server.launch()
