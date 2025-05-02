from cpp_stats.metrics.lcom.base import LCOMClassData

def calculate_connections(data: LCOMClassData) -> tuple[int, int, int]:
    '''
    Returns NP, NDC and NIC for TCC and LCC metrics. 
    '''
    n = len(data.method_data)
    np = n * (n - 1) / 2
    direct_connections = {}
    for method_name, method_data in data.method_data.items():
        for field in method_data.used_fields:
            if field in direct_connections:
                direct_connections[field].add(method_name)
            else:
                direct_connections[field] = set([method_name])

    ndc = 0
    direct_connections_set = set([])
    for _, methods in direct_connections.items():
        for lhv in methods:
            for rhv in methods:
                if lhv == rhv:
                    continue
                direct_connections_set.add((min(lhv, rhv), max(lhv, rhv)))
    ndc = len(direct_connections_set)

    indirect_connections = set([])
    for field_lhv in data.fields:
        for field_rhv in data.fields:
            if field_lhv == field_rhv:
                continue
            if field_lhv not in direct_connections or field_rhv not in direct_connections:
                continue
            lhv_set = direct_connections[field_lhv]
            rhv_set = direct_connections[field_rhv]
            intersection = lhv_set.intersection(rhv_set)
            if len(intersection) == 0:
                continue
            lhv = lhv_set - intersection
            rhv = rhv_set - intersection
            for l_method in lhv:
                for r_method in rhv:
                    indirect_connections.add((min(l_method, r_method), max(l_method, r_method)))
    nic = len(indirect_connections)

    return (np, ndc, nic)
