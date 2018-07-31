import requests
from mastermind import get_valid_numbers, to_dict_result, call_test_api
from mastermind import get_right_position

base_url = 'http://172.16.37.129/'

start_url = base_url + 'api/start'
test_url = base_url + 'api/test'

TOKEN = 'tokendj'


def test_call_test_api():
    chain = '34567'
    response = requests.post(test_url,
                        data={'token': TOKEN,
                              'result': chain
                            }
                        )
    assert response.status_code == 200


def test_call_start_api():
    response = requests.post(start_url,
                             data={'token': TOKEN})
    assert response.status_code == 200


def test_get_valid_numbers():
    res = get_valid_numbers()
    res_part_1 = ''.join([str(el) for el in res[:2]])
    res_part_1 += 'ccc'
    res_part_2 = 'cc'
    res_part_2 += ''.join([str(el) for el in res[2:]])
    test_numbers_1 = to_dict_result(call_test_api(res_part_1))
    test_numbers_2 = to_dict_result(call_test_api(res_part_2))
    assert  test_numbers_1['good'] + test_numbers_1['wrong_place'] + test_numbers_2['good'] + test_numbers_2['wrong_place'] == 5


def test_get_right_position():
    valid_numbers = get_valid_numbers()
    nb = str(valid_numbers[0])
    pos = get_right_position(nb, [0, 1, 2, 3, 4])
    l = ['c' for i in range(5)]
    l[pos] = nb
    res_call_test = to_dict_result(call_test_api(''.join(l)))
    assert res_call_test['good'] == 1
