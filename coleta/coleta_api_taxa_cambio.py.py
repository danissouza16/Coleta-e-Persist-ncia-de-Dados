import pytest
import requests

BASE_URL = "exemplo"

def teste_get_json():
    response = requests.get(f"{BASE_URL}/movies/json")
    assert response.status_code == 200

def test_get_xml():
    response = requests.get(f"{BASE_URL}/movies/xml")
    assert response.status_code == 200

def test_add_json():
    movies = {"new_key": "new_value"}
    response = requests.post(f"{BASE_URL}/movies/jsonc", json=movies)
    assert response.status_code == 201

def test_add_xml():
    movies = {"new_key_xml": "new_value_xml"}
    response = requests.post(f"{BASE_URL}/movies/xmlc", json=movies)
    assert response.status_code == 201

def test_delete():
    params = {'key': 'new_key'}
    response = requests.delete(f"{BASE_URL}/movies/delete", params=params)
    assert response.status_code == 200