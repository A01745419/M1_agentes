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
        self.movimientos_robot = 0
        self.suciedad = self.model.num_suciedad

    def move(self):
        self.suciedad = self.model.num_suciedad
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
            radius = 8)
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        limpia = False

        if len(cellmates) != 0:
            for i in cellmates:
                if i.tipo == 0:
                    self.model.num_suciedad -= 1
                    self.tipo = 3
                    i.tipo = 4
                    limpia = True
                elif i.tipo == 4:
                    self.tipo = 1
                
        if len(cellmates) == 0 or limpia == False:
            new_position = self.random.choice(possible_steps)
            cellmates_newp = self.model.grid.get_cell_list_contents([new_position])
            if len(cellmates_newp) == 1:
                if cellmates_newp[0].tipo != 1:
                    self.model.grid.move_agent(self, new_position)
                    self.model.movimientos += 1
                    self.movimientos_robot += 1
            elif len(cellmates_newp) == 0:
                self.model.grid.move_agent(self, new_position)
                self.model.movimientos += 1
                self.movimientos_robot += 1

    def step(self):
        self.suciedad = self.model.num_suciedad

        if self.model.steps_max > 0 and self.model.num_suciedad > 0:
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
        self.movimientos_robot = 0
        self.suciedad = self.model.num_suciedad
            
class LimpiezaModel(Model):
    '''
    Define el modelo del limpieza con robot.
    '''
    def __init__(self, width, height, agents, dirty, steps):
        self.width = width
        self.height = height
        self.num_agents = agents
        self.porcentaje_sucias = dirty 
        self.pasos = steps
        self.steps_max = self.pasos * self.num_agents
        self.num_suciedad = round((self.width * self.height) * self.porcentaje_sucias)
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True #Para la visualizacion usando navegador
        self.movimientos = 0
        self.porcentaje_sucias_final = (self.num_suciedad * 100) // (width * height)
        celdas = []
        self.datacollector = DataCollector(
            model_reporters={"Total Movements":LimpiezaModel.calculate_movements},
            agent_reporters={}
        )
        self.datacollector2 = DataCollector(
            model_reporters={"Total Dirty":LimpiezaModel.calculate_dirty},
            agent_reporters={}
        )
        
        for i in range(self.num_agents):
            a = RobotLimpiezaAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))
        
        for (content, x, y) in self.grid.coord_iter():
            celdas.append([x, y])
        
        for i in range(self.num_agents, (self.num_suciedad + self.num_agents)):
            a = SuciedadAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            pos = self.random.choice(celdas)
            self.grid.place_agent(a, (pos[0], pos[1])) 
            celdas.remove(pos)

    def calculate_movements(model):
        total_movements = 0
        movements_report = [agent.movimientos_robot for agent in model.schedule.agents]
        for x in movements_report:
            total_movements += x
        return total_movements

    def calculate_dirty(model):
        dirty_report = [agent.suciedad for agent in model.schedule.agents]
        for x in dirty_report:
            return x 

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.datacollector2.collect(self)
        self.porcentaje_sucias_final = (self.num_suciedad * 100) // (self.width * self.height)
        print(f'Numero de celdas sucias restantes= {self.num_suciedad}')
        print(f'Porcentaje de celdas sucias restantes= {self.porcentaje_sucias_final} %')
        print(f'Total de movimientos realizados por los {self.num_agents} agentes= {self.movimientos}')
        print(f'Pasos totales restantes= {self.steps_max}')
        print(" ")    
