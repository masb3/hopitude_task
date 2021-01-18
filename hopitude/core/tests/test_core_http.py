import pytest

from django.urls import reverse, resolve
from core.views import IndexView


class TestIndexView:
    def test_get_index_view_status_code(self, client):
        url = reverse('core:index')
        response = client.get(url)
        assert response.status_code == 200

    def test_get_index_view_csrf(self, client):
        url = reverse('core:index')
        response = client.get(url)
        assert 'csrfmiddlewaretoken' in str(response.content)

    @pytest.mark.django_db
    def test_post_correct_data_index_view_status_code(self, client):
        url = reverse('core:index')
        data = {'status': 1,
                'operating_param': 1,
                'compare': 1,
                'value': 1}
        response = client.post(url, data)
        assert response.status_code == 200

    @pytest.mark.django_db()
    def test_post_incorrect_data_index_view_status_code(self, client):
        url = reverse('core:index')
        response = client.post(url)
        assert response.status_code == 400

    def test_index_url_resolves_index_view(self):
        view = resolve('/')
        assert view.func.__name__ == IndexView.as_view().__name__
