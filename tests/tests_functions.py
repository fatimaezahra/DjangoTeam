import requests
from mastermind import (get_valid_numbers, to_dict_result, call_start_api,
                        get_right_position, get_solution, get_variables,
                        call_test_side_effect)
from mock import Mock


size = 5




def call_start_side_effect():
    return '{"size": 5}'


def test_call_start_api():
     response = call_start_api(True)
     response_dict = to_dict_result(response)
     assert 'size' in response_dict.keys() and response_dict['size'] == 5


def test_call_test_side_effect():
    response = call_test_side_effect('54321')
    response_dict = to_dict_result(response)
    assert response_dict['good'] == 1 and response_dict['wrong_place'] == 4


def test_call_test_api():
    response = call_test_side_effect('54321')
    response_dict = to_dict_result(response)
    assert response_dict['good'] == 1 and response_dict['wrong_place'] == 4


def test_call_to_dict_result():
    result_str = '{"good": 1, "wrong_place":3}'
    result_dict = to_dict_result(result_str)
    assert result_dict == {'good': 1, 'wrong_place': 3}


def test_get_valid_numbers():
    res = get_valid_numbers(5, call_test_side_effect)
    res_part_1 = ''.join([str(el) for el in res[:2]]) + 'ccc'
    res_part_2 = 'cc' +  ''.join([str(el) for el in res[2:]])
    test_numbers_1 = to_dict_result(call_test_side_effect(res_part_1))
    test_numbers_2 = to_dict_result(call_test_side_effect(res_part_2))
    assert test_numbers_1['good'] + test_numbers_2['good'] == 5


def test_get_right_position():
    valid_numbers = get_valid_numbers(5, call_test_side_effect)
    nb = str(valid_numbers[0])
    pos = get_right_position(nb, [0, 1, 2, 3, 4], call_test_side_effect, 5)
    l = ['c' for i in range(5)]
    l[pos] = nb
    res_call_test = to_dict_result(call_test_side_effect(''.join(l)))
    assert res_call_test['good'] == 1


def test_get_solution():
    result_list = get_solution(5, call_test_side_effect)
    assert result_list == [1, 2, 3, 4, 5]


def test_init_variables():
    variables = get_variables()
    assert variables == ('http://172.16.37.129/api/start',
                         'http://172.16.37.129/api/test',
                         'tokendj', 8, 0)


