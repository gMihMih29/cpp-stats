'''
Contains base logic for TCC and LCC calculations.
'''

from cpp_stats.metrics.lcom.base import LCOMClassData

def __get_direct_connections(data: LCOMClassData) -> (set[str], dict[str, set[str]]):
    '''
    Returns set and dictionary of direct connections in class.
    '''
    direct_connections = {}
    for field in data.fields:
        direct_connections[field] = set([])
    for method_name, method_data in data.method_data.items():
        for field in method_data.used_fields:
            if field not in direct_connections:
                direct_connections[field] = set([])
            direct_connections[field].add(method_name)

    direct_connections_set = set([])
    for _, methods in direct_connections.items():
        for lhv in methods:
            for rhv in methods:
                if lhv == rhv:
                    continue
                direct_connections_set.add((min(lhv, rhv), max(lhv, rhv)))
    return direct_connections_set, direct_connections

def __get_indirect_connections(
    data: LCOMClassData,
    direct_connections: dict[str, set[str]]) -> set[str]:
    '''
    Returns set of indirect connections in class.
    '''
    indirect_connections = set([])
    for field_lhv in data.fields:
        for field_rhv in data.fields:
            if (field_lhv == field_rhv
                or field_lhv not in direct_connections
                or field_rhv not in direct_connections):
                continue
            lhv_set = direct_connections[field_lhv].copy()
            rhv_set = direct_connections[field_rhv].copy()
            intersection = lhv_set.intersection(rhv_set)
            if len(intersection) == 0:
                continue
            lhv_set = lhv_set - intersection
            rhv_set = rhv_set - intersection
            for lhv in lhv_set:
                for rhv in rhv_set:
                    indirect_connections.add((min(lhv, rhv), max(lhv, rhv)))
    return indirect_connections

def calculate_connections(data: LCOMClassData) -> tuple[int, int, int]:
    '''
    Returns NP, NDC and NIC for TCC and LCC metrics. 
    '''
    direct_connection_set, direct_connection_dict = __get_direct_connections(data)

    indirect_connections = __get_indirect_connections(data, direct_connection_dict)

    return (
        len(data.method_data) * (len(data.method_data) - 1) / 2,
        len(direct_connection_set),
        len(indirect_connections)
    )
