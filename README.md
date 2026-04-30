# Modeling Global Energy Crisis Cascades using Complexity Science

**Course Project:** Complexity Science  
**Name:** Manya Agrawal  
**Entry Number:** 2023CH10882  

## Project Overview

This project applies concepts from complexity science to model cascading failures in global energy systems. The global energy system is represented as a network where nodes represent countries or energy sectors, and edges represent energy trade or supply-chain relationships.

Two types of networks are compared:

1. **Oil-dominated network**: modeled as a scale-free network using the Barabási–Albert model.
2. **EV-mineral network**: modeled as a random network using the Erdős–Rényi model.

The project studies how random shocks, connectivity, and threshold-based failures can produce avalanche-like cascades and self-organized critical behavior.

## Key Concepts

- Complexity science
- Network connectivity
- Noise and stochastic shocks
- Avalanche dynamics
- Cascading failures
- Power-law-like distributions
- Self-organized criticality

## Files Included

| File | Description |
|---|---|
| `energy_cascade_simulation.py` | Python code for generating networks, simulating cascades, and plotting results |
| `proejct report.tex` | LaTeX source file of the project report |
| `proejct report.pdf` | Final compiled PDF report |
| `graph1_oil_scale_free_network.png` | Scale-free oil network graph |
| `graph2_ev_random_network.png` | Random EV-mineral network graph |
| `graph3_oil_avalanche_distribution.png` | Avalanche size distribution for oil network |
| `graph4_ev_avalanche_distribution.png` | Avalanche size distribution for EV-mineral network |
| `graph5_connectivity_vs_failure.png` | Connectivity vs failure participation |
| `graph6_avalanche_comparison.png` | Boxplot comparison of avalanche sizes |
| `graph7_avalanche_time_series.png` | Avalanche time-series plot |

## Requirements

The simulation uses Python with the following libraries:

```bash
pip install numpy matplotlib networkx
