import sys
import pytest
import requests
sys.path.append('C:\\Users\\gouri\\Desktop\\CS4360\\senior-experience-group-project-issac-s-index')
sys.path.append('/home/meadnl89/SErepo/issacsindex')
from backend.repositories.serp_api_repository import SerpApiRepository

def test_get_search_results_by_query_success(requests_mock):
    # Arrange
    fake_response_data = {'results': 'some_search_results'}
    requests_mock.get("https://serpapi.com/search.json", json=fake_response_data, status_code=200)
    query = 'test_query'

    # Act
    response = SerpApiRepository.get_search_results_by_query(query)

    # Assert
    assert response == fake_response_data

def test_get_search_results_by_query_api_failure(requests_mock):
    # Arrange
    fake_response_data = {"error": "not found"}
    requests_mock.get("https://serpapi.com/search.json", json=fake_response_data, status_code=404)
    query = 'test_query'

    # Act
    response = SerpApiRepository.get_search_results_by_query(query)

    # Assert
    assert response == fake_response_data

def test_get_search_results_by_query_exception(requests_mock):
    # Arrange
    requests_mock.get("https://serpapi.com/search.json", exc=requests.exceptions.RequestException)
    query = 'test_query'

    # Act & Assert
    with pytest.raises(requests.exceptions.RequestException):
        SerpApiRepository.get_search_results_by_query(query)