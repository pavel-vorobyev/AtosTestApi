

def check_for_params(params: [], container):
    for param in params:
        if param not in container:
            return param

    return None
