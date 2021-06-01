def myResponse(code, data, extra=None):
    return {**{'code': code, 'data': data}, **extra}
