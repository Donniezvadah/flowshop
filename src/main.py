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
    best_seq, best_makespan, makespans, objectives_history = tabu_search(data, num_iterations=10, tabu_tenure=5, seed=42)

    # Find best for each objective
    best_csup_idx = min(range(len(objectives_history)), key=lambda i: objectives_history[i]['obj3_c_sup'])
    best_q_idx = min(range(len(objectives_history)), key=lambda i: objectives_history[i]['obj1_q'])
    best_e_idx = min(range(len(objectives_history)), key=lambda i: objectives_history[i]['obj2_e'])
    best_idle_idx = min(range(len(objectives_history)), key=lambda i: objectives_history[i]['obj4_sum_t_m'])

    # Save all objectives per iteration and bests
    results_path = os.path.join(os.path.dirname(__file__), '../results/results.txt')
    with open(results_path, 'w') as f:
        f.write(f'Best sequence (makespan): {best_seq}\n')
        f.write(f'Best makespan: {best_makespan}\n')
        f.write('Objectives per iteration:\n')
        for i, obj in enumerate(objectives_history):
            f.write(f'Iter {i}: Q={obj["obj1_q"]:.2f}, E={obj["obj2_e"]:.4f}, C_sup={obj["obj3_c_sup"]:.2f}, Sum_t_m={obj["obj4_sum_t_m"]:.2f}\n')
        f.write('\n')
        f.write(f'Best Q: {objectives_history[best_q_idx]["obj1_q"]:.2f} \n')
        f.write(f'Best E: {objectives_history[best_e_idx]["obj2_e"]:.4f} \n')
        f.write(f'Best C_sup: {objectives_history[best_csup_idx]["obj3_c_sup"]:.2f}\n')
        f.write(f'Best Sum_t_m: {objectives_history[best_idle_idx]["obj4_sum_t_m"]:.2f}\n')
        f.write('\n')
        # f.write(f'Best Q sequence: {best_seq if best_q_idx == best_csup_idx else "see CSV"}\n')
        # f.write(f'Best E sequence: {best_seq if best_e_idx == best_csup_idx else "see CSV"}\n')
        # f.write(f'Best Sum_t_m sequence: {best_seq if best_idle_idx == best_csup_idx else "see CSV"}\n')
        # # Optionally, you could save the speed assignments if you return them from tabu_search

    # Save objectives history as CSV for further analysis
    csv_path = os.path.join(os.path.dirname(__file__), '../results/objectives_history.csv')
    with open(csv_path, 'w') as f:
        f.write('iteration,Q,E,C_sup,Sum_t_m\n')
        for i, obj in enumerate(objectives_history):
            f.write(f'{i},{obj["obj1_q"]},{obj["obj2_e"]},{obj["obj3_c_sup"]},{obj["obj4_sum_t_m"]}\n')

    # Plot all objectives
    plot_dir = os.path.join(os.path.dirname(__file__), '../plots')
    os.makedirs(plot_dir, exist_ok=True)
    # Makespan
    plt.figure(figsize=(8, 5))
    plt.plot([obj['obj3_c_sup'] for obj in objectives_history], marker='o')
    plt.title('Tabu Search: Makespan (C_sup) over Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Makespan (C_sup)')
    plt.grid(True)
    plt.savefig(os.path.join(plot_dir, 'makespan.png'))
    plt.close()
    # Q
    plt.figure(figsize=(8, 5))
    plt.plot([obj['obj1_q'] for obj in objectives_history], marker='o', color='tab:blue')
    plt.title('Tabu Search: Total Job Durations (Q) over Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Total Job Durations (Q)')
    plt.grid(True)
    plt.savefig(os.path.join(plot_dir, 'q_total_job_durations.png'))
    plt.close()
    # E
    plt.figure(figsize=(8, 5))
    plt.plot([obj['obj2_e'] for obj in objectives_history], marker='o', color='tab:orange')
    plt.title('Tabu Search: Total Energy Consumption (E) over Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Total Energy Consumption (E)')
    plt.grid(True)
    plt.savefig(os.path.join(plot_dir, 'energy_consumption.png'))
    plt.close()
    # Sum_t_m
    plt.figure(figsize=(8, 5))
    plt.plot([obj['obj4_sum_t_m'] for obj in objectives_history], marker='o', color='tab:green')
    plt.title('Tabu Search: Total Idle Time (Sum_t_m) over Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Total Idle Time (Sum_t_m)')
    plt.grid(True)
    plt.savefig(os.path.join(plot_dir, 'total_idle_time.png'))
    plt.close()

    # Print best values for each objective
    print(f'Best sequence (makespan): {best_seq}')
    print(f'Best makespan (C_sup): {objectives_history[best_csup_idx]["obj3_c_sup"]:.2f}')
    print(f'Best Q (total durations): {objectives_history[best_q_idx]["obj1_q"]:.2f}')
    print(f'Best E (energy): {objectives_history[best_e_idx]["obj2_e"]:.4f} ')
    print(f'Best Sum_t_m (idle): {objectives_history[best_idle_idx]["obj4_sum_t_m"]:.2f}')
    print(f'Results saved to {results_path}')
    print(f'Objectives history CSV saved to {csv_path}')
    print(f'Plots saved to {plot_dir}')

if __name__ == '__main__':
    main()
