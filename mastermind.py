import requests
import json

base_url = 'http://172.16.37.129/'

start_url = base_url + 'api/start'
test_url = base_url + 'api/test'

TOKEN = 'tokendj'


def call_start_api():
    get_quizz_info = requests.post(start_url,
                                   data={'token': TOKEN})
    return get_quizz_info.text


def call_test_api(chain):
    get_result = requests.post(test_url,
                                   data={'token': TOKEN,
                                        'result': chain
                                        }
                                   )
    return get_result.text


def to_dict_result(result):
    return json.loads(result)


def get_valid_numbers():
    global size
    valid_numbers = []
    i = 0
    while len(valid_numbers) < size:
        test_string = str(i) * size
        result = to_dict_result(call_test_api(test_string))
        print(result)
        good = result['good']
        valid_numbers.extend([i for j in range(good)])
        i += 1
    return valid_numbers


def get_right_position(nb, indices):
    test_numbers = "abcde"
    for i in indices:
        new_numbers = test_numbers.replace(chr(i+97), nb)
        result = to_dict_result(call_test_api(new_numbers))
        if result['good']:
            return i


#main_info = to_dict_result(call_start_api())
#size = main_info['size']


size = 5

'''
valid_numbers = get_valid_numbers()

result_list = [0 for i in range(size)]
indices = [i for i in range(size)]

for nb in valid_numbers:
    position = get_right_position(str(nb), indices)
    indices.remove(position)
    result_list[position] = nb

print(result_list)

'''




#res_start = to_dict_result(call_test_api('34567'))
#print(res_start)