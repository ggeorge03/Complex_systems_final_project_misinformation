import solara
from mesa.visualization import Slider, SolaraViz, make_space_component, make_plot_component
from model import MisinfoModel


def agent_draw(agent):
    """Display agents: blue = susceptible, red = infected."""
    if agent.state == "S":
        return {"color": "blue", "size": 5}
    else:  # Infected
        return {"color": "red", "size": 5}


# Initiate the model
model = MisinfoModel()


# Function to return collected data dynamically
def get_data(model):
    df = model.datacollector.get_model_vars_dataframe()
    return df if not df.empty else None  # Avoid crashing on empty data


# Define a function to extract the correct measure for the plot
def measure(model):
    df = get_data(model)
    if df is None:
        return {}
    return {
        "Susceptible": df["Susceptible"].tolist(),
        "Infected": df["Infected"].tolist(),
    }


# Create the plot component
plot = make_plot_component(
    measure=measure,
    backend="matplotlib",
)


# Build the SolaraViz page
page = SolaraViz(
    model,
    components=[
        make_space_component(agent_portrayal=agent_draw, backend="matplotlib"),
        plot,
    ],
    model_params={
        "N": Slider("Number of agents", value=100, min=10, max=200, step=10),
        "beta": Slider("Infection prob (β)", value=0.3, min=0.0, max=1.0, step=0.05),
        "gamma": Slider("Recovery prob (γ)", value=0.1, min=0.0, max=1.0, step=0.05),
        "initial_infected": Slider("Initial infected fraction", value=0.05, min=0.0, max=1.0, step=0.05),
    },
    name="Misinformation SIS Model",
)

page  # required for Solara
