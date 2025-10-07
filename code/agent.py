from mesa import Agent
import random

class PersonAgent(Agent):
    """A simple agent that can be Susceptible (S) or Infected (I)."""
    def __init__(self, unique_id, model, state="S"):
        super().__init__(unique_id, model)
        self.state = state

    def step(self):
        if self.state == "I":
            # Try recovery
            if random.random() < self.model.gamma:
                self.state = "S"
            else:
                # Try to infect a neighbour
                neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
                if neighbors:
                    other = random.choice(neighbors)
                    if other.state == "S" and random.random() < self.model.beta:
                        other.state = "I"
