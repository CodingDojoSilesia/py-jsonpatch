def get_path_elements(path_to_split):
    splitted_path = path_to_split.split('/')
    path_elements = filter(str.strip, splitted_path)
    serialized_path = []
    for element in path_elements:
        try:
            serialized_path.append(int(element))
        except ValueError:
            serialized_path.append(element)
    return serialized_path


def is_path_exist(document, *args):
    try:
        doc_reference = document.copy()
        for i in args:
            doc_reference = doc_reference[i]
    except (IndexError, KeyError, TypeError) as e:
        print(e)
        return False
    return True


def remove_by_path(data, keys):
    if len(keys) == 1:
        value = data[keys[0]]
        del data[keys[0]]
        return value
    return remove_by_path(data[keys[0]], keys[1:])


def get_value_by_path(data, keys):
    if len(keys) == 1:
        return data[keys[0]]
    return get_value_by_path(data[keys[0]], keys[1:])


def add_value_by_path(data, keys, value_to_add):
    if len(keys) == 1:
        if type(data) == list:
            data.insert(keys[0], value_to_add)
        else:
            data[keys[0]].append(value_to_add)
        return True
    add_value_by_path(data[keys[0]], keys[1:], value_to_add)


def replace_value_by_path(data, keys, value_to_add):
    if len(keys) == 1:
        if type(data) == list:
            data[keys[0]] = value_to_add
        else:
            data[keys[0]] = value_to_add
        return True
    replace_value_by_path(data[keys[0]], keys[1:], value_to_add)
