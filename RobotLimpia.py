"""
Logica de Limpieza con Robot que incluye agentes y modelo
Autores: Jose Luis Madrigal y Cesar Emiliano Palome
Noviembre 9, 2022
"""
# La clase `Model` se hace cargo de los atributos a nivel del modelo, maneja los agentes. 
# Cada modelo puede contener múltiples agentes y todos ellos son instancias de la clase `Agent`.
from mesa import Agent, Model 

# Debido a que necesitamos un solo agente por celda elegimos `SingleGrid` que fuerza un solo objeto por celda.
from mesa.space import MultiGrid

# Con `SimultaneousActivation` hacemos que todos los agentes se activen de manera simultanea.
from mesa.time import SimultaneousActivation
import numpy as np
from mesa.datacollection import DataCollector

class RobotLimpiezaAgent(Agent):
    '''
    Representa a un robot de limpieza que encuentra celdas sucias para eliminarlas.
    '''
    def __init__(self, unique_id, model):
        '''
        Crea un agente con estado inicial aleatorio de 0 o 1, también se le asigna un identificador 
        formado por una tupla (x,y). También se define un tipo que determina el agente que es,
        un numero de movimientos y de suciedad.
        '''
        super().__init__(unique_id, model)
        self.tipo = 1
        self.movimientosRobot = 0
        self.suciedad = self.model.numSuciedad

    def move(self):
        self.suciedad = self.model.numSuciedad
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
            radius = 8)
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        limpia = False

        if len(cellmates) != 0:
            for i in cellmates:
                if i.tipo == 0:
                    self.model.numSuciedad -= 1
                    self.tipo = 3
                    i.tipo = 4
                    limpia = True
                elif i.tipo == 4:
                    self.tipo = 1
                
        if len(cellmates) == 0 or limpia == False:
            new_position = self.random.choice(possibleSteps)
            cellmatesNewPos = self.model.grid.get_cell_list_contents([new_position])
            if len(cellmatesNewPos) == 1:
                if cellmatesNewPos[0].tipo != 1:
                    self.model.grid.move_agent(self, new_position)
                    self.model.movimientos += 1
                    self.movimientosRobot += 1
            elif len(cellmatesNewPos) == 0:
                self.model.grid.move_agent(self, new_position)
                self.model.movimientos += 1
                self.movimientosRobot += 1

    def step(self):
        self.suciedad = self.model.numSuciedad

        if self.model.steps_max > 0 and self.model.numSuciedad > 0:
            self.move()
            self.model.steps_max -= 1
        else:
            print("FIN DE LA SIMULACION")


class SuciedadAgent(Agent):
    '''
    Representa a la suciedad que puede encontrarse en alguna celda.
    '''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.tipo = 0
        self.movimientosRobot = 0
        self.suciedad = self.model.numSuciedad
            
class LimpiezaModel(Model):
    '''
    Define el modelo del limpieza con robot.
    '''
    def __init__(self, width, height, agents, dirty, steps):
        self.width = width
        self.height = height
        self.numAgents = agents
        self.porcentajeSucias = dirty 
        self.pasos = steps
        self.steps_max = self.pasos * self.numAgents
        self.numSuciedad = round((self.width * self.height) * self.porcentajeSucias)
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True #Para la visualizacion usando navegador
        self.movimientos = 0
        self.porcentajeSuciasFinal = (self.numSuciedad * 100) // (width * height)
        celdas = []
        self.dataCollectorMovements = DataCollector(
            model_reporters={"Total Movements":LimpiezaModel.calculateMovements},
            agent_reporters={}
        )
        self.dataCollectorDirty = DataCollector(
            model_reporters={"Total Dirty":LimpiezaModel.calculateDirty},
            agent_reporters={}
        )
        
        for i in range(self.numAgents):
            a = RobotLimpiezaAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))
        
        for (content, x, y) in self.grid.coord_iter():
            celdas.append([x, y])
        
        for i in range(self.numAgents, (self.numSuciedad + self.numAgents)):
            a = SuciedadAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            pos = self.random.choice(celdas)
            self.grid.place_agent(a, (pos[0], pos[1])) 
            celdas.remove(pos)

    def calculateMovements(model):
        totalMovements = 0
        movementsReport = [agent.movimientosRobot for agent in model.schedule.agents]
        for x in movementsReport:
            totalMovements += x
        return totalMovements

    def calculateDirty(model):
        dirtyReport = [agent.suciedad for agent in model.schedule.agents]
        for x in dirtyReport:
            return x 

    def step(self):
        self.schedule.step()
        self.dataCollectorMovements.collect(self)
        self.dataCollectorDirty.collect(self)
        self.porcentajeSuciasFinal = (self.numSuciedad * 100) // (self.width * self.height)
        print(f'Numero de celdas sucias restantes= {self.numSuciedad}')
        print(f'Porcentaje de celdas sucias restantes= {self.porcentajeSuciasFinal} %')
        print(f'Total de movimientos realizados por los {self.numAgents} agentes= {self.movimientos}')
        print(f'Pasos totales restantes= {self.steps_max}')
        print(" ")    
