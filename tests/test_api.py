import pytest
import requests


@pytest.fixture()
def api_base_url():
    BASE_URL = "https://jsonplaceholder.typicode.com"
    return BASE_URL


def test_get_user_status_code(api_base_url):
    response = requests.get(f"{api_base_url}/users/1")
    res_status = response.status_code
    assert res_status == 200, \
        f" expected response to have status code 200 but got {res_status}"


def test_get_user_data(api_base_url):
    response = requests.get(f"{api_base_url}/users/1")
    res_status = response.status_code
    res_values = response.json()
    assert res_values["id"] == 1, \
        f" expected response to have id = 1 but got {res_values['id']}"
    assert res_values["name"] == "Leanne Graham", \
        f" expected response to have name as Leanne Graham but got {res_values['name']}"
    assert res_values["email"] == "Sincere@april.biz", \
        f" expected response to have email as Sincere@april.biz but got {res_values['email']}"


def test_get_user_response_time(api_base_url):
    response = requests.get(f"{api_base_url}/users/1")
    res_time = response.elapsed.total_seconds()
    assert res_time < 5, \
        f" expected response to be less than 5 seconds but got {res_time}"


def test_get_invalid_user(api_base_url):
    response = requests.get(f"{api_base_url}/users/999")
    res_status = response.status_code
    assert res_status == 404, \
        f" expected response to have status code 404 but got {res_status}"


def test_create_post(api_base_url):
    new_post = {
        "title": "My Test Post",
        "body": "This is the content",
        "userId": 1
    }
    response = requests.post(f"{api_base_url}/posts", json=new_post)
    res_status = response.status_code
    res_data = response.json()
    assert res_status == 201 and res_data["title"] == "My Test Post", \
        f" expected response to have status code 201 and title as My Test Post but got {res_status} and {res_data['title']}"


def test_get_all_users(api_base_url):
    response = requests.get(f"{api_base_url}/users/")
    res_status = response.status_code
    res_data = response.json()
    length_res_data = len(res_data)
    assert res_status == 200 and length_res_data == 10, \
        f" expected response to have status code 200 and length of the json data is less than 10 but got {res_status} and {length_res_data}"


def test_update_user(api_base_url):
    updated_data = {
        "id": 1,
        "name": "Sindhu Updated",
        "username": "sindhu",
        "email": "sindhu@test.com"
    }
    response = requests.put(f"{api_base_url}/users/1", json=updated_data)
    res_data = response.json()
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"
    assert res_data["name"] == "Sindhu Updated", \
        f"Expected updated name but got {res_data['name']}"


def test_patch_user(api_base_url):
    patch_data = {"name": "Sindhu Patched"}
    response = requests.patch(f"{api_base_url}/users/1", json=patch_data)
    res_data = response.json()
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"
    assert res_data["name"] == "Sindhu Patched", \
        f"Expected patched name but got {res_data['name']}"


def test_delete_user(api_base_url):
    response = requests.delete(f"{api_base_url}/users/1")
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"
    assert response.json() == {}, \
        f"Expected empty response body but got {response.json()}"
