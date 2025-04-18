import networkx as nx
import random
import matplotlib.pyplot as plt

def run_simulation(num_nodes, edge_prob, infection_prob, recovery_prob, time_steps,
                   indiv_learning_effect, antivirus_update_effect, learning_threshold):

    G = nx.erdos_renyi_graph(num_nodes, edge_prob)
    state = {node: 0 for node in G.nodes()}  # 0 = Susceptible, 1 = Infected
    infection_probabilities = {node: infection_prob for node in G.nodes()}

    infected_nodes = random.sample(list(G.nodes()), random.randint(1, 5))
    for node in infected_nodes:
        state[node] = 1

    recovery_prob_current = recovery_prob
    infected_ratios = []
    susceptible_ratios = []

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

    total_recoveries = 0

    def update():
        nonlocal recovery_prob_current, total_recoveries
        new_infected = []
        recovered_count = 0

        for node in G.nodes():
            if state[node] == 1:
                for neighbor in G.neighbors(node):
                    if state[neighbor] == 0 and random.random() < infection_probabilities[neighbor]:
                        new_infected.append(neighbor)

                if random.random() < recovery_prob_current:
                    state[node] = 0
                    recovered_count += 1
                    total_recoveries += 1
                    infection_probabilities[node] = max(0, infection_probabilities[node] * (1 - indiv_learning_effect))

        for node in new_infected:
            state[node] = 1

        infected_count = sum(state.values())
        recovery_prob_current = min(1, recovery_prob**(antivirus_update_effect))

        return infected_count

    for t in range(1, time_steps + 1):
        num_infected = update()
        infected_ratios.append(num_infected / num_nodes)
        susceptible_ratios.append(1 - infected_ratios[-1])

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(range(len(infected_ratios)), infected_ratios, label="Infected", color="red", linewidth=2)
    ax.plot(range(len(susceptible_ratios)), susceptible_ratios, label="Susceptible", color="blue", linewidth=2)
    ax.axhline(y=learning_threshold, color='green', linestyle='--', label="Learning Threshold")

    ax.set_xlabel("Time Step (Starting from Day 0)")
    ax.set_ylabel("Proportion of Nodes")
    ax.set_ylim(0, 1)
    ax.legend()
    ax.set_title("Global Evolution of Infection Over Time")
    ax.grid()
    plt.show()

    plt.figure(figsize=(6, 6))
    node_colors = ["red" if state[node] == 1 else "blue" for node in G.nodes()]
    nx.draw(G, node_color=node_colors, with_labels=False, node_size=50)
    plt.title("Final Network State (Red = Infected, Blue = Susceptible)")
    plt.show()

    final_infected = infected_ratios[-1] * 100
    final_susceptible = susceptible_ratios[-1] * 100
    print(f"Final Infected Proportion: {final_infected:.2f}%")
    print(f"Final Susceptible Proportion: {final_susceptible:.2f}%")
