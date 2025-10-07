from mesa import Model
from mesa.space import MultiGrid
from mesa.scheduler import RandomActivation
from mesa.datacollection import DataCollector
import random

from agent import PersonAgent

class MisinfoModel(Model):
    """SIS model of misinformation spread."""
    def __init__(self, N=100, width=10, height=10, beta=0.3, gamma=0.1, initial_infected=0.05):
        super().__init__()
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.beta = beta
        self.gamma = gamma

        # Create agents
        for i in range(self.num_agents):
            state = "I" if random.random() < initial_infected else "S"
            agent = PersonAgent(i, self, state)
            self.schedule.add(agent)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        # Data collector
        self.datacollector = DataCollector(
            model_reporters={
                "Infected": lambda m: sum([1 for a in m.schedule.agents if a.state == "I"]),
                "Susceptible": lambda m: sum([1 for a in m.schedule.agents if a.state == "S"])
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
