import requests
import json


def get_variables():
    base_url = 'http://172.16.37.129/'
    start_url = base_url + 'api/start'
    test_url = base_url + 'api/test'
    TOKEN = 'tokendj'
    size = 28
    nb_api_calls = 0
    return start_url, test_url, TOKEN, size, nb_api_calls


def call_test_side_effect(param):
    return_dict = {'good': 0, 'wrong_place': 0}
    i = 1
    for el in param:
        if el in '12345':
            return_dict["good"] += (i == int(el))
            return_dict["wrong_place"] += (i != int(el))
        i += 1
    return_str = str(return_dict)
    return_str = return_str.replace('\'', '"')
    return return_str


def call_start_api(mock=False):
    global nb_api_calls
    if mock:
        return '{"size": 5}'
    else:
        get_quizz_info = requests.post(start_url,
                                       data={'token': TOKEN
                                             })
        nb_api_calls += 1
        return get_quizz_info.text


def call_test_api(chain):
    global nb_api_calls
    get_result = requests.post(test_url,
                               data={'token': TOKEN,
                                     'result': chain
                                     }
                               )
    nb_api_calls += 1
    return get_result.text


def to_dict_result(result):
    return json.loads(result)


def get_valid_numbers(size, call_test_api=call_test_api):
    chars = [str(i) for i in range(10)]
    chars.extend([chr(i) for i in range(65, 91)])
    chars.extend([chr(i) for i in range(97, 123)])
    valid = []
    i = 0
    while len(valid) < size:
        test_string = chars[i] * size
        result = to_dict_result(call_test_api(test_string))
        good = result['good']
        valid.extend([chars[i]] * good)
        i += 1
    return valid


def get_pos(indices, nb, tab, left=0, right=5,
            call_test_api=call_test_api, size=5):
    if left == right - 1:
        return left
    middle = (left + right) // 2
    new_numbers = ''.join([el for el in tab])
    result = to_dict_result(call_test_api(new_numbers))
    if result['good']:
        for i in range((left + middle) // 2, middle):
            tab[i] = '|'
        return get_pos(indices, nb, tab, left, middle, call_test_api, size)
    else:
        for i in range(middle, (middle + right) // 2):
            if i not in indices:
                tab[i] = str(nb)
            else:
                tab[i] = '|'
        return get_pos(indices, nb, tab, middle, right, call_test_api, size)


def get_right_position(nb, indices, call_test_api=call_test_api, size=5):
    tab = ['|'] * size
    for i in indices:
        tab[i] = str(nb)
        new_numbers = ''.join([el for el in tab])
        result = to_dict_result(call_test_api(new_numbers))
        if result['good']:
            return i


def get_solution(size, call_test_api=call_test_api):
    valid_numbers = get_valid_numbers(size, call_test_api)
    result_list = [0 for i in range(size)]

    indices = []

    for nb in valid_numbers:
        middle = size // 2

        tab = [str(nb)] * middle + ['|'] * (size - middle)
        for i in indices:
            tab[i] = '|'
        position = get_pos(indices, nb, tab, 0, size, call_test_api, size)
        indices.append(position)
        result_list[position] = nb
    return result_list


if __name__ == '__main__':
    start_url, test_url, TOKEN, size, nb_api_calls = get_variables()
    main_info = to_dict_result(call_start_api())
    if 'Error' not in main_info.keys():  # quizz already started
        size = main_info['size']

    result = get_solution(size)
    call_test_api(''.join([str(el) for el in result]))
