import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter

# ==========================================================
# GLOBAL ENERGY CRISIS CASCADE SIMULATION
# Complexity Science Project
# ==========================================================

np.random.seed(42)

# -------------------------------
# PARAMETERS
# -------------------------------

N = 200
runs = 5000

threshold = 0.48
shock_strength = 0.55
propagation_loss = 0.18

oil_m = 3
ev_probability = 0.035


# -------------------------------
# CASCADE FUNCTION
# -------------------------------

def simulate_avalanche(G):
    """
    Simulates one cascading failure event.

    Nodes = countries / energy sectors
    Edges = energy trade or supply-chain dependence

    A random shock lowers one node's resource level.
    If resource falls below threshold, the node fails.
    Failure transfers stress to neighbouring nodes.
    """

    resource = np.random.uniform(0.42, 1.0, size=G.number_of_nodes())

    failed = set()
    queue = []

    initial_node = np.random.choice(list(G.nodes()))
    resource[initial_node] -= shock_strength * np.random.uniform(0.8, 1.2)

    if resource[initial_node] < threshold:
        failed.add(initial_node)
        queue.append(initial_node)

    while queue:
        node = queue.pop(0)

        for neighbour in G.neighbors(node):
            if neighbour not in failed:

                # Balanced stress transfer
                degree_factor = 1 / np.sqrt(1 + G.degree(neighbour))
                random_factor = np.random.uniform(0.7, 1.3)

                resource[neighbour] -= propagation_loss * degree_factor * random_factor

                if resource[neighbour] < threshold:
                    failed.add(neighbour)
                    queue.append(neighbour)

    return len(failed), failed


# -------------------------------
# NETWORK GENERATION
# -------------------------------

oil_network = nx.barabasi_albert_graph(N, oil_m, seed=42)
ev_network = nx.erdos_renyi_graph(N, ev_probability, seed=42)


# -------------------------------
# RUN SIMULATIONS
# -------------------------------

def run_simulations(G, runs):
    avalanche_sizes = []
    failed_degrees = []

    for _ in range(runs):
        size, failed_nodes = simulate_avalanche(G)
        avalanche_sizes.append(size)

        for node in failed_nodes:
            failed_degrees.append(G.degree(node))

    return avalanche_sizes, failed_degrees


oil_avalanches, oil_failed_degrees = run_simulations(oil_network, runs)
ev_avalanches, ev_failed_degrees = run_simulations(ev_network, runs)


# -------------------------------
# GRAPH 1: OIL NETWORK
# -------------------------------

plt.figure(figsize=(9, 7))
pos = nx.spring_layout(oil_network, seed=42)

node_sizes = [35 + 18 * oil_network.degree(n) for n in oil_network.nodes()]

nx.draw_networkx_edges(oil_network, pos, alpha=0.35, width=0.8)
nx.draw_networkx_nodes(oil_network, pos, node_size=node_sizes, alpha=0.85)

plt.title("Oil-Dominated Energy Network: Scale-Free Connectivity")
plt.axis("off")
plt.tight_layout()
plt.savefig("graph1_oil_scale_free_network.png", dpi=300)
plt.show()


# -------------------------------
# GRAPH 2: EV-MINERAL NETWORK
# -------------------------------

plt.figure(figsize=(9, 7))
pos = nx.spring_layout(ev_network, seed=42)

node_sizes = [35 + 18 * ev_network.degree(n) for n in ev_network.nodes()]

nx.draw_networkx_edges(ev_network, pos, alpha=0.35, width=0.8)
nx.draw_networkx_nodes(ev_network, pos, node_size=node_sizes, alpha=0.85)

plt.title("EV-Mineral Supply Network: Random Connectivity")
plt.axis("off")
plt.tight_layout()
plt.savefig("graph2_ev_random_network.png", dpi=300)
plt.show()


# -------------------------------
# POWER-LAW DISTRIBUTION FUNCTION
# -------------------------------

def plot_avalanche_distribution(avalanche_sizes, title, filename):
    counts = Counter(avalanche_sizes)

    sizes = np.array(sorted(counts.keys()))
    frequencies = np.array([counts[s] for s in sizes])

    valid = sizes > 0
    sizes = sizes[valid]
    frequencies = frequencies[valid]

    plt.figure(figsize=(8, 6))
    plt.scatter(sizes, frequencies, s=35, label="Simulation data")

    # Fit only intermediate avalanche sizes
    fit_mask = (sizes >= 2) & (sizes <= np.percentile(sizes, 90))

    if np.sum(fit_mask) >= 4:
        log_sizes = np.log10(sizes[fit_mask])
        log_freq = np.log10(frequencies[fit_mask])

        slope, intercept = np.polyfit(log_sizes, log_freq, 1)
        alpha = -slope

        fitted = 10 ** (intercept + slope * np.log10(sizes[fit_mask]))

        plt.plot(
            sizes[fit_mask],
            fitted,
            linestyle="--",
            linewidth=2,
            label=f"Power-law fit, α ≈ {alpha:.2f}"
        )
    else:
        alpha = np.nan

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Avalanche Size, s")
    plt.ylabel("Frequency")
    plt.title(title)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

    return alpha


# -------------------------------
# GRAPH 3 AND 4: AVALANCHE DISTRIBUTIONS
# -------------------------------

alpha_oil = plot_avalanche_distribution(
    oil_avalanches,
    "Avalanche Size Distribution in Oil Network",
    "graph3_oil_avalanche_distribution.png"
)

alpha_ev = plot_avalanche_distribution(
    ev_avalanches,
    "Avalanche Size Distribution in EV-Mineral Network",
    "graph4_ev_avalanche_distribution.png"
)


# -------------------------------
# GRAPH 5: CONNECTIVITY VS FAILURE
# -------------------------------

plt.figure(figsize=(8, 6))

plt.hist(
    oil_failed_degrees,
    bins=25,
    alpha=0.65,
    label="Oil Scale-Free Network"
)

plt.hist(
    ev_failed_degrees,
    bins=25,
    alpha=0.65,
    label="EV Random Network"
)

plt.xlabel("Degree of Failed Nodes")
plt.ylabel("Frequency")
plt.title("Relation Between Connectivity and Failure Participation")
plt.legend()
plt.grid(True, linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig("graph5_connectivity_vs_failure.png", dpi=300)
plt.show()


# -------------------------------
# GRAPH 6: AVALANCHE SIZE COMPARISON
# -------------------------------

plt.figure(figsize=(8, 6))

plt.boxplot(
    [oil_avalanches, ev_avalanches],
    labels=["Oil Scale-Free", "EV Random"],
    showfliers=True
)

plt.ylabel("Avalanche Size")
plt.title("Comparison of Avalanche Sizes in Different Energy Networks")
plt.grid(True, linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig("graph6_avalanche_comparison.png", dpi=300)
plt.show()


# -------------------------------
# GRAPH 7: AVALANCHE TIME SERIES
# -------------------------------

plt.figure(figsize=(9, 5))

plt.plot(oil_avalanches[:300], label="Oil Scale-Free Network", linewidth=1.2)
plt.plot(ev_avalanches[:300], label="EV Random Network", linewidth=1.2)

plt.xlabel("Simulation Run")
plt.ylabel("Avalanche Size")
plt.title("Avalanche Events Over Repeated Random Shocks")
plt.legend()
plt.grid(True, linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig("graph7_avalanche_time_series.png", dpi=300)
plt.show()


# -------------------------------
# SUMMARY
# -------------------------------

print("\nSimulation Summary")
print("------------------")
print(f"Number of nodes: {N}")
print(f"Number of simulation runs: {runs}")

print("\nOil Scale-Free Network")
print(f"Average avalanche size: {np.mean(oil_avalanches):.2f}")
print(f"Median avalanche size: {np.median(oil_avalanches):.2f}")
print(f"Maximum avalanche size: {np.max(oil_avalanches)}")
print(f"Power-law exponent α: {alpha_oil:.2f}")

print("\nEV-Mineral Random Network")
print(f"Average avalanche size: {np.mean(ev_avalanches):.2f}")
print(f"Median avalanche size: {np.median(ev_avalanches):.2f}")
print(f"Maximum avalanche size: {np.max(ev_avalanches)}")
print(f"Power-law exponent α: {alpha_ev:.2f}")

print("\nGenerated graph files:")
print("graph1_oil_scale_free_network.png")
print("graph2_ev_random_network.png")
print("graph3_oil_avalanche_distribution.png")
print("graph4_ev_avalanche_distribution.png")
print("graph5_connectivity_vs_failure.png")
print("graph6_avalanche_comparison.png")
print("graph7_avalanche_time_series.png")