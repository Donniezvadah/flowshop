from typing import List, Dict, Any, Tuple
import random
from flowshop import calculate_makespan, calculate_objectives

def tabu_search(
    data: Dict[str, Any],
    num_iterations: int = 10,
    tabu_tenure: int = 5,
    seed: int = 42
) -> Tuple[List[int], int, List[int], List[Dict[str, float]]]:
    """
    Performs Tabu Search to minimize makespan in a 2-machine flowshop problem.
    Args:
        data: Problem data as parsed by parse_flowshop_dataset.
        num_iterations: Number of iterations to run.
        tabu_tenure: Number of iterations a move remains tabu.
        seed: Random seed for reproducibility.
    Returns:
        best_sequence: The best job sequence found.
        best_makespan: The makespan of the best sequence.
        makespans: List of best makespan at each iteration (for plotting).
        objectives_history: List of dicts with all objectives per iteration (for metrics/plotting).
    """
    random.seed(seed)
    N = data['N']
    M = data['M']
    L = data['L']
    # Initial solution: random permutation and random speeds
    current_sequence = list(range(N))
    random.shuffle(current_sequence)
    speeds_assignment = [[random.randint(0, L-1) for _ in range(M)] for _ in range(N)]
    current_obj = calculate_objectives(current_sequence, speeds_assignment, data)
    current_makespan = current_obj['obj3_c_sup']
    best_sequence = current_sequence[:]
    best_makespan = current_makespan
    best_speeds = [row[:] for row in speeds_assignment]
    makespans = [best_makespan]
    objectives_history = [
        {
            'obj1_q': current_obj['obj1_q'],
            'obj2_e': current_obj['obj2_e'],
            'obj3_c_sup': current_obj['obj3_c_sup'],
            'obj4_sum_t_m': current_obj['obj4_sum_t_m']
        }
    ]

    # Tabu list: stores forbidden moves with their expiration iteration
    tabu_list = dict()  # key: move tuple, value: expiration iteration

    for it in range(num_iterations):
        neighborhood = []
        # 1. Generate neighbors by pairwise swaps
        for i in range(N-1):
            for j in range(i+1, N):
                neighbor_seq = current_sequence[:]
                neighbor_seq[i], neighbor_seq[j] = neighbor_seq[j], neighbor_seq[i]
                move = ('swap', i, j)
                if tabu_list.get(move, 0) > it:
                    continue  # Move is tabu
                neighbor_obj = calculate_objectives(neighbor_seq, speeds_assignment, data)
                makespan = neighbor_obj['obj3_c_sup']
                neighborhood.append((makespan, neighbor_seq, [row[:] for row in speeds_assignment], move, neighbor_obj))
        # 2. Generate neighbors by changing speed assignment for one job on one machine
        for job_idx in range(N):
            for machine_idx in range(M):
                current_speed = speeds_assignment[job_idx][machine_idx]
                for speed_level in range(L):
                    if speed_level != current_speed:
                        neighbor_speeds = [row[:] for row in speeds_assignment]
                        neighbor_speeds[job_idx][machine_idx] = speed_level
                        move = ('speed', job_idx, machine_idx, current_speed)
                        if tabu_list.get(move, 0) > it:
                            continue  # Move is tabu
                        neighbor_obj = calculate_objectives(current_sequence, neighbor_speeds, data)
                        makespan = neighbor_obj['obj3_c_sup']
                        neighborhood.append((makespan, current_sequence[:], neighbor_speeds, move, neighbor_obj))
        if not neighborhood:
            break
        # Select best neighbor (minimize makespan)
        neighborhood.sort(key=lambda x: x[0])
        best_neighbor_makespan, best_neighbor_seq, best_neighbor_speeds, best_move, best_neighbor_obj = neighborhood[0]
        # Aspiration: allow tabu move if it improves best known
        if best_neighbor_makespan < best_makespan:
            best_sequence = best_neighbor_seq[:]
            best_makespan = best_neighbor_makespan
            best_speeds = [row[:] for row in best_neighbor_speeds]
        # Update current solution
        current_sequence = best_neighbor_seq[:]
        speeds_assignment = [row[:] for row in best_neighbor_speeds]
        current_makespan = best_neighbor_makespan
        makespans.append(best_makespan)
        objectives_history.append({
            'obj1_q': best_neighbor_obj['obj1_q'],
            'obj2_e': best_neighbor_obj['obj2_e'],
            'obj3_c_sup': best_neighbor_obj['obj3_c_sup'],
            'obj4_sum_t_m': best_neighbor_obj['obj4_sum_t_m']
        })
        # Update tabu list
        tabu_list[best_move] = it + tabu_tenure
    return best_sequence, best_makespan, makespans, objectives_history
