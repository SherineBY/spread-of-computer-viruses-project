import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display

def run_simulation(num_nodes, edge_prob, infection_prob, recovery_prob, time_steps,
                   indiv_learning_effect, antivirus_update_effect, learning_threshold):

    # Network creation
    G = nx.erdos_renyi_graph(num_nodes, edge_prob)
    state = {node: 0 for node in G.nodes()}  # 0 = Susceptible, 1 = Infected
    infection_probabilities = {node: infection_prob for node in G.nodes()}  # Probability of node infection

    # Initial infection (1 to 5 infected nodes)
    infected_nodes = random.sample(list(G.nodes()), random.randint(1, 5))
    for node in infected_nodes:
        state[node] = 1

    recovery_prob_current = recovery_prob  # probability of recovery

    infected_ratios = []
    susceptible_ratios = []

    # === DAY 0: Initial conditions ===
    initial_infected_ratio = sum(state.values()) / num_nodes
    initial_susceptible_ratio = 1 - initial_infected_ratio

    print(f"=== DAY 0 ===")
    print(f"Nodes: {num_nodes}, Edge Probability: {edge_prob}")
    print(f"Initial Infection Probability: {infection_prob}")
    print(f"Recovery Probability: {recovery_prob}")
    print(f"Individual Learning Effect: {indiv_learning_effect}")
    print(f"Antivirus Update Effect: {antivirus_update_effect}")
    print(f"Learning Threshold: {learning_threshold * 100}% of the network")
    print(f"Initial Infected Nodes: {len(infected_nodes)} ({initial_infected_ratio * 100:.2f}%)")
    print("=" * 30)

    infected_ratios.append(initial_infected_ratio)
    susceptible_ratios.append(initial_susceptible_ratio)

    total_recoveries = 0  # Total recoveries

    # === update function ===
    def update():
        nonlocal recovery_prob_current, total_recoveries
        new_infected = []
        recovered_count = 0

        for node in G.nodes():
            if state[node] == 1:  # If the node is infected
                for neighbor in G.neighbors(node):
                    if state[neighbor] == 0 and random.random() < infection_probabilities[neighbor]:
                        new_infected.append(neighbor)

                # recovery process
                if random.random() < recovery_prob_current:
                    state[node] = 0  # The node recovers
                    recovered_count += 1
                    total_recoveries += 1
                    # Individual learning: reduced likelihood of infection
                    infection_probabilities[node] = max(0, infection_probabilities[node] * (1 - indiv_learning_effect))

        for node in new_infected:
            state[node] = 1  # Infection of neighbours

        # Global Learning (Update recovery with the correct formula)
        infected_count = sum(state.values())
        recovery_prob_current = min(1, recovery_prob**(antivirus_update_effect))

        return infected_count

    # === simulation loop ===
    for t in range(1, time_steps + 1):
        num_infected = update()
        infected_ratios.append(num_infected / num_nodes)
        susceptible_ratios.append(1 - infected_ratios[-1])

    # === Graph of the course of infection ===
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(range(len(infected_ratios)), infected_ratios, label="Infected", color="red", linestyle='-', linewidth=2)
    ax.plot(range(len(susceptible_ratios)), susceptible_ratios, label="Susceptible", color="blue", linestyle='-', linewidth=2)

    # Added global learning threshold
    ax.axhline(y=learning_threshold, color='green', linestyle='--', label="Learning Threshold")

    ax.set_xlabel("Time Step (Starting from Day 0)")
    ax.set_ylabel("Proportion of Nodes")
    ax.set_ylim(0, 1)
    ax.legend()
    ax.set_title("Global Evolution of Infection Over Time (Including Day 0)")
    ax.grid()
    plt.show()

    # === Final display of network status ===
    plt.figure(figsize=(6, 6))
    node_colors = ["red" if state[node] == 1 else "blue" for node in G.nodes()]
    nx.draw(G, node_color=node_colors, with_labels=False, node_size=50)
    plt.title("Final Network State (Red = Infected, Blue = Susceptible)")
    plt.show()
