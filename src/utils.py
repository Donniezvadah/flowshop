import os
from typing import Dict, List, Any

def parse_flowshop_dataset(filepath: str) -> Dict[str, Any]:
    """
    Parses a 2-machine flowshop dataset from the given txt file.
    Returns a dictionary with all relevant parameters.
    """
    data = {}
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Parse scalar values
    data['N'] = int(lines[0].split(':')[1])  # Number of jobs
    data['M'] = int(lines[1].split(':')[1])  # Number of machines
    data['L'] = int(lines[2].split(':')[1])  # Number of setups
    
    # Parse job processing times
    data['p1j'] = list(map(int, lines[3].split(':')[1].split()))
    data['p2j'] = list(map(int, lines[4].split(':')[1].split()))
    
    # Parse setup and conversion parameters
    data['vl'] = list(map(float, lines[5].split(':')[1].split()))
    data['Conv_l'] = list(map(float, lines[6].split(':')[1].split()))
    data['IdleConv_i'] = list(map(float, lines[7].split(':')[1].split()))
    
    # Parse S1jk and S2jk matrices
    s1_start = lines.index('S1jk:') + 1
    s2_start = lines.index('S2jk:') + 1
    s1_lines = lines[s1_start:s2_start-1]
    s2_lines = lines[s2_start:]
    data['S1jk'] = [list(map(int, row.split())) for row in s1_lines]
    data['S2jk'] = [list(map(int, row.split())) for row in s2_lines]
    
    return data
