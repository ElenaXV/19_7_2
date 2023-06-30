from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, invalid_auth_key

import pytest
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/pet.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# Написать 10 различных тестов для данного REST API-интерфейса.

#1
def test_add_photo_to_pet(pet_photo='images/pet2.jpg'):
    """Проверяем возможность изменить фото у ранее добавленного животного"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

    # Берём id первого питомца из списка и отправляем запрос на удаление

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']


#2
def test_add_new_pet_without_photo(name='Майло', animal_type='тойтерьер',
                                     age='5'):
    """Проверяем возможность добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name



# 3
@pytest.mark.xfail
def test_get_api_key_with_invalid_email_and_valid_password(email=invalid_email, password=valid_password):
    '''Проверяем запрос с валидным паролем и с невалидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# 4
@pytest.mark.xfail
def test_get_api_key_with_valid_email_and_invalid_password(email=valid_email, password=invalid_password):
    '''Проверяем запрос с невалидным паролем и с валидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# 5
@pytest.mark.xfail
def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=invalid_password):
    '''Проверяем получение api-ключа с данными незарегистрированного пользователя'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# 6
@pytest.mark.xfail
def test_get_all_pets_with_invalid_key(filter=''):
    """ Получение списка питомцев с несуществующим api-ключом"""

    auth_key = invalid_auth_key
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status != 200


# 7
@pytest.mark.xfail
def test_add_new_pet_with_invalid_data(name='', animal_type='', age='', pet_photo='images\pet.jpg'):
    """Негативный сценарий. Проверяем что можно добавить питомца с некорректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200

# 8
@pytest.mark.xfail
def test_add_new_pet_with_negativ_age(name='Том', animal_type='подзаборный',
                                     age='-5'):
    """Негативный сценарий. Проверяем возможность добавить питомца с отрицательным возрастом"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['age'] == age

# 9
@pytest.mark.xfail
def test_add_new_pet_with_digit_age_number(name='Барбоскин', animal_type='двортерьер',
                                     age='4748', pet_photo='images/pet.jpg'):
    """Негативный сценарий. Проверяем что можно добавить питомца с числом более трех знаков в переменной age"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['age'] == age

# 10
@pytest.mark.xfail
def test_add_new_pet_with_ivvalid_photo(name='Матроскин', animal_type='двортерьер',
                                     age='7', pet_photo='images/text.txt'):
    """Негативный сценарий. Проверяем что можно добавить питомца с фото не подходящего формата """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
