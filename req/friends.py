# ПРОГРАММА ДЛЯ АНАЛИЗА ВОЗРАСТА СВОИХ ДРУЗЕЙ В ВК

import requests
from datetime import datetime
from operator import itemgetter

# токен приложения вк спомощью которого будем запрашивать данные
ACCESS_TOKEN = 'b4c799f7b4c799f7b4c799f713b4b42e6dbb4c7b4c799f7eb8a14d1a54ff17d4af72e75'
#  url_1 для получения id пользователя
URL_1 = 'https://api.vk.com/method/users.get?v=5.71&access_token={token}&user_ids={user_ids}'
#  url_2 для получения списка друзей пользователя
URL_2 = 'https://api.vk.com/method/friends.get?v=5.71&access_token={token}&user_id={user_id}&fields=bdate'

#  Метод для получения id пользователя
def get_user_id(uids):
	r = requests.get(URL_1.format(token = ACCESS_TOKEN, user_ids = uids))
	return eval(r.text)['response'][0]['id']

#  Метод для получения списка друзей пользователя
def get_friends_to_dict(user_id):
	r = requests.get(URL_2.format(token = ACCESS_TOKEN, user_id = user_id))
	return eval(r.text)

# Метод для получения словаря где ключем является возраст, а значением является количество
def get_dict_friends(*friends):
	list_friends = dict()
	now_year = datetime.now().year
	for item in friends[0]:
		try:
			age = now_year - int(item['bdate'].split('.')[2])
		except Exception:
			continue
		if age in list_friends.keys():
			list_friends[age] += 1
		else:
			list_friends[age] = 1
	return list_friends

# метод для конвертации словаря в список кортежей
def convert_dict_to_list(kwargs):
	list_friends = list()
	for key, value in kwargs.items():
		a = (key, value)
		list_friends.append(a)
	return list_friends

# метод для получения отсортированного списка кортежей
def calc_age(uid):
	user_id = get_user_id(uid)
	friends = get_friends_to_dict(user_id)['response']['items']
	dict_to_age_friends = get_dict_friends(friends)
	friends_age_count = convert_dict_to_list(dict_to_age_friends)
	friends_age_count = sorted(friends_age_count, key = itemgetter(0)) # сортировка по первому ключу по возрастанию
	friends_age_count = sorted(friends_age_count, key = itemgetter(1), reverse = True) # сортировка по убыванию по второму ключу
	return friends_age_count
	

if __name__ == '__main__':
	res = calc_age('reigning') # указываем username пользователя вк
	print(res)
