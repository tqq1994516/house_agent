def myResponse(data, extra=None):
    if extra:
        return {**{'data': data}, **extra}
    else:
        return data
