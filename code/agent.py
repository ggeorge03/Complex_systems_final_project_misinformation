import numpy as np
from mesa import Agent
import random

class PersonAgent(Agent):
    """Agent representing a person who can be Susceptible (S) or Infected (I)."""
    
    def __init__(self, model, state="S"):
        super().__init__(model)  # **model is required!**
        self.state = state

    def step(self):
        """Agent tries to infect nearby susceptible agents if infected."""
        if self.state == "I":
            neighbors = self.model.space.get_neighbors(self.pos, radius=5, include_center=False)
            for other in neighbors:
                if other.state == "S" and random.random() < self.model.beta:
                    other.state = "I"
