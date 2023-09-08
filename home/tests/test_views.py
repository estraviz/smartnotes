import pytest
from django.contrib.auth.models import User
from django.urls import reverse


def test_home_endpoint_returns_welcome_page(client):
    url = reverse("home")
    response = client.get(url)

    assert response.status_code == 200
    assert "Check out these smart notes!" in str(response.content)


def test_signup_endpoint_returns_form_for_unauthenticated_user(client):
    response = client.get(path="/signup")

    assert response.status_code == 200
    assert "home/register.html" in response.template_name
    assert "Enter the same password as before, for verification" in str(
        response.content
    )


@pytest.mark.django_db
def test_signup_endpoint_redirects_authenticated_user(client):
    """
    When a user is authenticated and trys to acces the signup page,
    she should be redirected to the notes list page.
    """
    user = User.objects.create_user(
        username="test", email="myemail@example.com", password="test"
    )
    client.login(username=user.username, password="test")
    response = client.get(path="/signup", follow=True)
    print(type(response))

    assert response.status_code == 200
    assert "notes/notes_list.html" in response.template_name
