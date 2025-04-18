import ipywidgets as widgets

# === interactive UI ===
num_nodes_slider = widgets.IntSlider(value=100, min=50, max=500, step=50, description='Nodes:')
edge_prob_slider = widgets.FloatSlider(value=0.05, min=0.01, max=0.2, step=0.01, description='Edge Prob:')
infection_prob_slider = widgets.FloatSlider(value=0.3, min=0.1, max=0.5, step=0.05, description='Infection Prob:')
recovery_prob_slider = widgets.FloatSlider(value=0.3, min=0.05, max=0.5, step=0.05, description='Recovery Prob:')
time_steps_slider = widgets.IntSlider(value=200, min=50, max=500, step=50, description='Time Steps:')

indiv_learning_slider = widgets.FloatSlider(value=0.1, min=0, max=0.5, step=0.05, description='Indiv Learn:')
global_learning_slider = widgets.FloatSlider(value=0.2, min=0, max=1, step=0.1, description='Antivirus Effect:')
threshold_slider = widgets.FloatSlider(value=0.4, min=0.2, max=0.6, step=0.05, description='Threshold:')

run_button = widgets.Button(description="Run Simulation")

# Launch the simulation with the
def on_button_click(b):
    run_simulation(num_nodes_slider.value, edge_prob_slider.value, infection_prob_slider.value,
                   recovery_prob_slider.value, time_steps_slider.value,
                   indiv_learning_slider.value, global_learning_slider.value, threshold_slider.value)

run_button.on_click(on_button_click)

# viewing widgets
display(num_nodes_slider, edge_prob_slider, infection_prob_slider, recovery_prob_slider, time_steps_slider,
        indiv_learning_slider, global_learning_slider, threshold_slider, run_button)
