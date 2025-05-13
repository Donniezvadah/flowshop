from typing import List, Dict, Any, Tuple
import random
from flowshop import calculate_makespan

def tabu_search(
    data: Dict[str, Any],
    num_iterations: int = 10,
    tabu_tenure: int = 5,
    seed: int = 42
) -> Tuple[List[int], int, List[int]]:
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
    """
    random.seed(seed)
    N = data['N']
    # Initial solution: random permutation
    current_sequence = list(range(N))
    random.shuffle(current_sequence)
    current_makespan = calculate_makespan(current_sequence, data)
    best_sequence = current_sequence[:]
    best_makespan = current_makespan
    makespans = [best_makespan]

    # Tabu list: stores forbidden swaps (i, j) with their expiration iteration
    tabu_list = dict()  # key: (i, j), value: expiration iteration

    for it in range(num_iterations):
        neighborhood = []
        # Generate neighbors by pairwise swaps
        for i in range(N-1):
            for j in range(i+1, N):
                neighbor = current_sequence[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                move = (i, j)
                if tabu_list.get(move, 0) > it:
                    continue  # Move is tabu
                makespan = calculate_makespan(neighbor, data)
                neighborhood.append((makespan, neighbor, move))
        if not neighborhood:
            break
        # Select best neighbor
        neighborhood.sort()
        best_neighbor_makespan, best_neighbor, best_move = neighborhood[0]
        # Aspiration: allow tabu move if it improves best known
        if best_neighbor_makespan < best_makespan:
            best_sequence = best_neighbor[:]
            best_makespan = best_neighbor_makespan
        # Update current solution
        current_sequence = best_neighbor[:]
        current_makespan = best_neighbor_makespan
        makespans.append(best_makespan)
        # Update tabu list
        tabu_list[best_move] = it + tabu_tenure
    return best_sequence, best_makespan, makespans
