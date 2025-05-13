# Flowshop Multi-Objective Tabu Search

This project implements a multi-objective Tabu Search algorithm for a two-machine flowshop scheduling problem, with support for speed scaling and energy-aware objectives. The codebase is modular and tracks four key objectives, saving all metrics and plots for analysis.

## Project Structure

```
flowshop/
  data/         # Input datasets (flowshop problem instances)
  plots/        # Output plots for each objective
  results/      # Output metrics and logs
  src/
    flowshop.py       # Core objective calculations
    main.py           # Main entry point: runs the experiment, saves results, plots
    tabu_search.py    # Tabu Search implementation
    utils.py          # Dataset parsing and utilities
    __init__.py
  hello_im_suffering.ipynb  # Original exploratory notebook
  Model_formulation.pdf     # Problem formulation reference
  README.md
  requirements.txt
```

## Problem Overview

Given a set of jobs and two machines, the goal is to find a job sequence (and optionally, speed assignments) that optimizes the following objectives:

1. **Total Job Durations (Q):** Sum of all processing times.
2. **Total Energy Consumption (E):** Includes both processing and idle energy.
3. **Makespan (C_sup):** Completion time of the last job on the last machine.
4. **Total Idle Time (Sum_t_m):** Sum of idle times for all machines.

## Main Methods and Files

### `src/flowshop.py`

- **`calculate_makespan(sequence, data)`**  
  Computes the makespan for a given job sequence (basic version, ignores setups and speed scaling).

- **`calculate_objectives(sequence, speeds_assignment, data)`**  
  Computes all four objectives for a given job sequence and speed assignment, using all problem parameters (processing times, speed factors, setup times, energy rates, etc.).  
  Returns a dictionary with all objectives and detailed breakdowns.

### `src/tabu_search.py`

- **`tabu_search(data, num_iterations, tabu_tenure, seed)`**  
  Runs the Tabu Search metaheuristic:
  - Starts from a random job sequence (all jobs at normal speed by default).
  - Iteratively explores neighbors by swapping job positions.
  - Tracks a tabu list to avoid cycling.
  - At each iteration, computes all four objectives using `calculate_objectives`.
  - Returns the best sequence, best makespan, and a history of all objectives per iteration.

### `src/main.py`

- Loads a dataset from `data/`.
- Runs Tabu Search and collects all objectives per iteration.
- Saves all metrics to `results/results.txt`.
- Plots the progress of each objective over iterations to `plots/`.
- Prints the best values for each objective.

### `src/utils.py`

- **`parse_flowshop_dataset(filepath)`**  
  Parses a dataset file and returns all problem parameters in a dictionary.

## Outputs

- **`results/results.txt`**  
  Contains the best sequence, best makespan, and all objectives for every iteration.

- **`plots/`**  
  - `makespan.png`: Makespan over iterations.
  - `q_total_job_durations.png`: Total job durations over iterations.
  - `energy_consumption.png`: Total energy consumption over iterations.
  - `total_idle_time.png`: Total idle time over iterations.

## Recent Changes

- **Multi-objective support:**  
  The code now tracks and saves all four objectives, not just makespan.
- **Metrics and plotting:**  
  All objectives are saved per iteration and plotted for analysis.
- **Refactoring:**  
  The core logic from the exploratory notebook was modularized into `flowshop.py` and integrated into the main pipeline.
- **Error handling and reproducibility:**  
  The code is robust to missing parameters and uses fixed random seeds for reproducibility.

## How to Run

1. Place your dataset in the `data/` directory.
2. Run the main script:
   ```bash
   python3 src/main.py
   ```
3. Check `results/results.txt` for metrics and `plots/` for visualizations.

## Requirements

- Python 3.7+
- See `requirements.txt` for dependencies (mainly `matplotlib` for plotting).
