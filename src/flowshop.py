from typing import List, Dict, Any

def calculate_makespan(sequence: List[int], data: Dict[str, Any]) -> int:
    """
    Calculates the makespan for a given job sequence in a 2-machine flowshop.
    Args:
        sequence: List of job indices (0-based) representing the job order.
        data: Dictionary containing problem parameters as parsed by parse_flowshop_dataset.
    Returns:
        The makespan (total completion time) for the sequence.
    """
    N = data['N']
    p1j = data['p1j']
    p2j = data['p2j']
    # For now, we ignore setups and conversions for a basic implementation
    # (can be extended for full problem later)

    # Initialize completion times
    C1 = [0] * N  # Completion times on machine 1
    C2 = [0] * N  # Completion times on machine 2

    for i, job in enumerate(sequence):
        if i == 0:
            C1[i] = p1j[job]
            C2[i] = C1[i] + p2j[job]
        else:
            C1[i] = C1[i-1] + p1j[job]
            C2[i] = max(C1[i], C2[i-1]) + p2j[job]
    
    makespan = C2[-1]
    return makespan
