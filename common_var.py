DEFAULT_TIME_RANGE = 86400000
STATUS_CODE = {0: 200, 1: 409, 2: 404, 9: 500}

Logic = {
    'SUCCESS': 0,
    'CONFLICT': 1,
    'NOT_FOUND': 2,
    'UNKNOWN_ERROR': 9
}


TermColor = {
    'OK': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
    'NORMAL': '\033[0m'
}
