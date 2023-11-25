def cpu_str_to_float(cpu_str):
    if cpu_str.endswith('m'):
        return float(cpu_str.rstrip('m')) / 1000
    elif cpu_str.endswith('Mi'):
        return float(cpu_str.rstrip('Mi')) / 1000
    else:
        return float(cpu_str)
