import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from settings import valid_email, valid_password, valid_username

@pytest.fixture(autouse=True)
def open_my_pets():
    pytest.driver = webdriver.Chrome('C:\Skillfactory\chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    # Вводим email
    pytest.driver.find_element(By.ID, "email").send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element(By.ID, "pass").send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, "h1").text == "PetFriends"
    # Переходим на страницу "Мои питомцы"
    pytest.driver.find_element(By.LINK_TEXT, u"Мои питомцы").click()
    # Проверяем, что мы оказались на странице с питомцами пользователя
    assert pytest.driver.find_element(By.CSS_SELECTOR, 'div.\\.col-sm-4.left h2').text == valid_username

    yield

    pytest.driver.quit()


def test_all_pets_are_present():
    # Присутствуют все питомцы

    wait = WebDriverWait(pytest.driver, 10)
    # Получаем количество питомцев из статистики
    my_pets_count_from_stat = int(
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.\\.col-sm-4.left'))).text.split('\n')[1].split(': ')[1]
    )

    # Получаем количество строк таблицы
    my_pets_count_from_table = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr')))

    # Сравниваем количество строк таблицы и количество питомцев из статистики
    assert len(my_pets_count_from_table) == my_pets_count_from_stat


def test_half_of_pets_have_photo():
    # Хотя бы у половины питомцев есть фото

    pytest.driver.implicitly_wait(10)
    images = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > th > img')
    is_photo = 0

    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            is_photo += 1

    print(f"Количество питомцев с фото: {is_photo}")
    print(f"Количество питомцев всего: {len(images)}")

    assert is_photo >= (len(images)/2)


def test_all_pets_have_name_age_type():
    # У всех питомцев есть имя, возраст и порода

    empty_names, empty_types, empty_ages = 0, 0, 0

    pytest.driver.implicitly_wait(10)
    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    for i in range(len(names)):
        if names[i].text == '':
            empty_names += 1

    pytest.driver.implicitly_wait(10)
    types = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    for i in range(len(types)):
        if types[i].text == '':
            empty_types += 1

    pytest.driver.implicitly_wait(10)
    ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
    for i in range(len(ages)):
        if ages[i].text == '':
            empty_ages += 1

    print(f"Количество питомцев без имени: {empty_names}")
    print(f"Количество питомцев без породы: {empty_types}")
    print(f"Количество питомцев без возраста: {empty_ages}")

    assert empty_names == 0
    assert empty_types == 0
    assert empty_ages == 0


def test_all_pets_have_different_names():
    # У всех питомцев разные имена

    pytest.driver.implicitly_wait(5)
    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    unic_names = set()

    for i in range(len(names)):
        unic_names.add(names[i].text)

    print(f"Количество имен питомцев: {len(names)}")
    print(f"Количество уникальных имен питомцев: {len(unic_names)}")

    assert len(names) == len(unic_names)

def test_not_repeated_pets():
    # В списке нет повторяющихся питомцев

    pytest.driver.implicitly_wait(5)
    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    pytest.driver.implicitly_wait(5)
    types = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    pytest.driver.implicitly_wait(5)
    ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

    my_pets = []

    for i in range(len(names)):
        new_pet = names[i].text + '/' + types[i].text + '/' + ages[i].text
        if new_pet in my_pets:
            print(f"Найден не уникальный питомец: {new_pet}")
        else:
            my_pets.append(new_pet)

    assert len(my_pets) == len(names)