import numpy as np
from mesa import Model
from mesa.agent import AgentSet
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
from agent import PersonAgent
import random

def count_infected(model):
    return sum(1 for a in model.population if a.state == "I")

def count_susceptible(model):
    return sum(1 for a in model.population if a.state == "S")

class MisinfoModel(Model):
    """SI model of misinformation spread in a continuous space using AgentSet."""

    def __init__(self, N=100, width=50, height=50, beta=0.3, initial_infected=5, seed=None):
        super().__init__(seed=seed)
        self.N = N
        self.beta = beta

        # Continuous space
        self.width = width
        self.height = height
        self.space = ContinuousSpace(width, height, torus=True)

        # AgentSet (custom name, cannot use model.agents)
        self.population = AgentSet([])

        # Create agents
        for i in range(self.N):
            state = "I" if i < initial_infected else "S"
            agent = PersonAgent(self, state=state)  # <-- pass self as model
            self.population.add(agent)

            # Random initial position
            pos = np.array([random.uniform(0, width), random.uniform(0, height)])
            self.space.place_agent(agent, pos)

        # Data collector
        self.datacollector = DataCollector(
            model_reporters={
                "Infected": count_infected,
                "Susceptible": count_susceptible,
            }
        )

    def step(self):
        """Execute one step of the model."""
        self.population.shuffle_do("step")  # Activate all agents
        self.datacollector.collect(self)
