# La clase `Model` se hace cargo de los atributos a nivel del modelo, maneja los agentes. 
# Cada modelo puede contener múltiples agentes y todos ellos son instancias de la clase `Agent`.
from mesa import Agent, Model 

# Debido a que necesitamos un solo agente por celda elegimos `SingleGrid` que fuerza un solo objeto por celda.
from mesa.space import MultiGrid

# Con `SimultaneousActivation` hacemos que todos los agentes se activen de manera simultanea.
from mesa.time import SimultaneousActivation
import numpy as np

class RobotLimpiezaAgent(Agent):
    '''
    Representa a un agente o una celda con estado vivo (1) o muerto (0)
    '''
    def __init__(self, unique_id, model):
        '''
        Crea un agente con estado inicial aleatorio de 0 o 1, también se le asigna un identificador 
        formado por una tupla (x,y). También se define un nuevo estado cuyo valor será definido por las 
        reglas mencionadas arriba.
        '''
        super().__init__(unique_id, model)
        self.tipo = 1


    def move(self):
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
            elif len(cellmates_newp) == 0:
                self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()


class SuciedadAgent(Agent):
    '''
    Representa a un agente o una celda con estado vivo (1) o muerto (0)
    '''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.tipo = 0
            
class LimpiezaModel(Model):
    '''
    Define el modelo del juego de la vida.
    '''
    def __init__(self, width, height):
        self.num_agents = 3
        self.porcentajesucias = .20
        self.num_suciedad = round((width * height) * self.porcentajesucias)
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True #Para la visualizacion usando navegador
        self.movimientos = 0
        celdas = []
        
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
        
        
    
    def step(self):
        self.schedule.step()
        print(self.movimientos)
