import solara
from mesa.visualization import Slider, SolaraViz, make_space_component, make_plot_component
from model import MisinfoModel

def agent_draw(agent):
    """Draw agents: blue = susceptible, red = infected"""
    if agent.state == "S":
        return {"color": "blue", "size": 5}
    else:
        return {"color": "red", "size": 5}

# Initialize the model
model = MisinfoModel()

# for _ in range(10):  # Simulate 10 steps
model.step()

# Print the collected data to verify
df = model.datacollector.get_model_vars_dataframe()
# print(df)  # Debugging step

plot = make_plot_component({"Susceptible": "tab:blue", "Infected": "tab:green"})

# # Function to extract data for plotting
# def measure(model):
#     df = model.datacollector.get_model_vars_dataframe()
#     if df.empty:
#         return {}
#     return {
#         "Susceptible": df["Susceptible"].tolist(),
#         "Infected": df["Infected"].tolist(),
#     }


# Plot component
# plot = make_plot_component(measure=measure, backend="matplotlib")

# Build SolaraViz page
page = SolaraViz(
    model,
    components=[
        make_space_component(agent_portrayal=agent_draw, backend="matplotlib"),
        plot,
    ],
    model_params={
        "N": Slider("Number of agents", value=100, min=10, max=200, step=10),
        "beta": Slider("Infection probability", value=0.3, min=0.0, max=1.0, step=0.05),
        "initial_infected": Slider("Initial infected", value=5, min=1, max=50, step=1),
    },
    name="Misinformation SI Model",
)

page
