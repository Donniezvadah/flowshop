import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
import matplotlib.pyplot as plt
from utils import parse_flowshop_dataset
from tabu_search import tabu_search

def main():
    # Load dataset
    data_path = os.path.join(os.path.dirname(__file__), '../data/ps4j2m-setup25_1.2_0.64_19050.txt')
    data = parse_flowshop_dataset(data_path)

    # Run Tabu Search
    best_seq, best_makespan, makespans = tabu_search(data, num_iterations=10, tabu_tenure=5, seed=42)

    # Save best result
    results_path = os.path.join(os.path.dirname(__file__), '../results/results.txt')
    with open(results_path, 'w') as f:
        f.write(f'Best sequence: {best_seq}\n')
        f.write(f'Best makespan: {best_makespan}\n')
        f.write(f'Makespans per iteration: {makespans}\n')

    # Plot makespan over iterations
    plt.figure(figsize=(8, 5))
    plt.plot(makespans, marker='o')
    plt.title('Tabu Search: Makespan over Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Best Makespan')
    plt.grid(True)
    plot_path = os.path.join(os.path.dirname(__file__), '../plots/makespan.png')
    plt.savefig(plot_path)
    plt.close()
    print(f'Best sequence: {best_seq}')
    print(f'Best makespan: {best_makespan}')
    print(f'Results saved to {results_path}')
    print(f'Plot saved to {plot_path}')

if __name__ == '__main__':
    main()
