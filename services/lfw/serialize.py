from json import dumps

def json_print_dict(_dict):
    """
    This function converts a python dict to a JSON formatted string in a simmilar maner as json.dumps()
    except that the dict values are always printed in the same order by sorting them.
    Also, the values of any inner dicts are also printed in the same order.
    @param _dict: python dict to be serialized to a JSON formatted string
    """
    ret = '{'
    sortedKeys = sorted(_dict.keys())
    for key in sortedKeys:
        ret += dumps(key) + ": "
        if isinstance(_dict[key], dict):
            ret += json_print_dict(_dict[key])
        else:
            ret += dumps(_dict[key])
        if key != sortedKeys[-1]:
            ret += ', '
    ret += '}'
    return ret

