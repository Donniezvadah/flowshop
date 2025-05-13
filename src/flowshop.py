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

def calculate_objectives(sequence: List[int], speeds_assignment: List[List[int]], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculates all four objectives based on a given job sequence and speed assignments.
    sequence: list of job indices (0 to N-1)
    speeds_assignment: list of lists, speeds_assignment[job_idx][machine_idx] = speed_level (0,1,2)
    data: dictionary with all problem parameters
    Returns: dict with all objectives and details
    """
    N = data['N']
    M = data['M']
    L = data['L']
    p_values = [data['p1j'], data['p2j']]
    r_values = data['vl']
    beta_values = data['Conv_l']
    gamma_values = data['IdleConv_i']
    d_jkm_m1 = data['S1jk']
    d_jkm_m2 = data['S2jk']
    s_j_values = [0.0] * N  # If not in data, assume 0
    rho_m_values = [1.0] * M  # If not in data, assume 1.0

    job_completion_times_m1 = [0.0] * N
    job_completion_times_m2 = [0.0] * N
    actual_proc_times = [[0.0] * M for _ in range(N)]

    # Calculate actual processing times based on speeds
    for job_idx_orig in range(N):
        for machine_idx in range(M):
            speed_level = speeds_assignment[job_idx_orig][machine_idx]
            base_proc_time = p_values[machine_idx][job_idx_orig]
            actual_proc_times[job_idx_orig][machine_idx] = base_proc_time / r_values[speed_level]

    # Completion times on M1
    for i, current_job_idx in enumerate(sequence):
        if i == 0:
            setup_time_m1 = d_jkm_m1[current_job_idx][current_job_idx]
            start_time_m1 = setup_time_m1
        else:
            prev_job_idx = sequence[i-1]
            setup_time_m1 = d_jkm_m1[prev_job_idx][current_job_idx]
            start_time_m1 = job_completion_times_m1[prev_job_idx] + setup_time_m1
        job_completion_times_m1[current_job_idx] = start_time_m1 + actual_proc_times[current_job_idx][0]

    # Completion times on M2
    for i, current_job_idx in enumerate(sequence):
        earliest_start_m2_after_m1 = job_completion_times_m1[current_job_idx] + s_j_values[current_job_idx]
        if i == 0:
            setup_time_m2 = d_jkm_m2[current_job_idx][current_job_idx]
            earliest_start_m2_after_prev_job_m2 = setup_time_m2
        else:
            prev_job_idx = sequence[i-1]
            setup_time_m2 = d_jkm_m2[prev_job_idx][current_job_idx]
            earliest_start_m2_after_prev_job_m2 = job_completion_times_m2[prev_job_idx] + setup_time_m2
        start_time_m2 = max(earliest_start_m2_after_m1, earliest_start_m2_after_prev_job_m2)
        job_completion_times_m2[current_job_idx] = start_time_m2 + actual_proc_times[current_job_idx][1]

    c_sup = job_completion_times_m2[sequence[-1]]

    # Objective 1: q (sum of job durations)
    q_val = sum(actual_proc_times[j][m] for j in range(N) for m in range(M))

    # Total processing time on each machine
    total_processing_on_m = [sum(actual_proc_times[j][m] for j in range(N)) for m in range(M)]

    # t_m: total idle time on machine m
    t_m_values = [max(0, c_sup - total_processing_on_m[m]) for m in range(M)]
    sum_t_m = sum(t_m_values)

    # Objective 2: e (total energy consumption)
    energy_processing = 0.0
    for job_idx_orig in range(N):
        for machine_idx in range(M):
            speed_level = speeds_assignment[job_idx_orig][machine_idx]
            base_proc_time = p_values[machine_idx][job_idx_orig]
            energy_processing += (base_proc_time / (60.0 * r_values[speed_level])) * \
                                 beta_values[speed_level] * rho_m_values[machine_idx]
    energy_idle = sum((gamma_values[m] * rho_m_values[m] / 60.0) * t_m_values[m] for m in range(M))
    e_val = energy_processing + energy_idle

    return {
        "obj1_q": q_val,
        "obj2_e": e_val,
        "obj3_c_sup": c_sup,
        "obj4_sum_t_m": sum_t_m,
        "details": {
            "job_comp_m1": job_completion_times_m1,
            "job_comp_m2": job_completion_times_m2,
            "actual_proc_times": actual_proc_times,
            "t_m_values": t_m_values
        }
    }
