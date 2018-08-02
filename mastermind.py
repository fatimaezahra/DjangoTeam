import requests
import json


def get_variables():
    base_url = 'http://172.16.37.129/'
    start_url = base_url + 'api/start'
    test_url = base_url + 'api/test'
    TOKEN = 'tokendj'
    size = 8
    nb_api_calls = 0
    return start_url, test_url, TOKEN, size, nb_api_calls


def call_test_side_effect(param):
    return_dict = {'good': 0, 'wrong_place': 0}
    i = 1
    for el in param:
        if el in '12345':
            if i == int(el):
                return_dict["good"] += 1
            else:
                return_dict["wrong_place"] += 1
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
    valid = []
    i = 0
    while len(valid) < size:
        test_string = str(i) * size
        result = to_dict_result(call_test_api(test_string))
        good = result['good']
        valid.extend([i] * good)
        i += 1
    return valid


def get_right_position(nb, indices, call_test_api=call_test_api, size=5):
    test_numbers = ''.join([chr(i+97) for i in range(size)])
    for i in indices:
        new_numbers = test_numbers.replace(chr(i+97), nb)
        result = to_dict_result(call_test_api(new_numbers))
        if result['good']:
            return i


def get_solution(size, call_test_api=call_test_api):
    valid_numbers = get_valid_numbers(size, call_test_api)
    result_list = [0 for i in range(size)]
    indices = [i for i in range(size)]

    for nb in valid_numbers:
        position = get_right_position(str(nb), indices, call_test_api, size)
        indices.remove(position)
        result_list[position] = nb
    return result_list


if __name__ == '__main__':
    start_url, test_url, TOKEN, size, nb_api_calls = get_variables()
    main_info = to_dict_result(call_start_api())
    if 'Error' not in main_info.keys():  # quizz already started
        size = main_info['size']

    result = get_solution(size)
    call_test_api(''.join([str(el) for el in result]))
