import pytest
from django.contrib.auth.models import User

from notes.models import Notes

from .factories import NoteFactory, UserFactory


@pytest.fixture
def logged_user(client):
    # user = User.objects.create_user(username='testuser',
    #                                 email='test@email.com',
    #                                 password='12345')
    user = UserFactory()
    client.login(username=user.username, password='12345')
    return user



@pytest.mark.django_db
def test_list_endpoint_returns_user_notes(client, logged_user):
    # note1 = Notes.objects.create(title='note title', text='', user=logged_user)
    # note2 = Notes.objects.create(title='note title', text='', user=logged_user)
    note1 = NoteFactory(user=logged_user)
    note2 = NoteFactory(user=logged_user)
    response = client.get(path='/smart/notes')
    content = str(response.content)

    assert 200 == response.status_code
    assert "note title" in content
    assert 2 == content.count("<h3>")


@pytest.mark.django_db
def test_list_endpoint_only_lists_notes_from_authenticated_user(client,
                                                                logged_user):
    jon = User.objects.create_user(username='jon',
                                   email='jon@example.com',
                                   password='12345')
    Notes.objects.create(title="Jon note", text='', user=jon)

    note1 = Notes.objects.create(title="One title", text='', user=logged_user)
    note2 = Notes.objects.create(title="Another title", text='',
                                 user=logged_user)

    response = client.get(path='/smart/notes')
    content = str(response.content)

    assert 200 == response.status_code
    assert "Jon note" not in content
    assert "One title" in content
    assert "Another title" in content
    assert 2 == content.count("<h3>")


@pytest.mark.django_db
def test_create_endpoint_receives_form_data(client, logged_user):
    form_data = {'title': 'An impressive title', 'text': 'An interesting text'}
    response = client.post(path='/smart/notes/new',
                           data=form_data,
                           follow=True)

    assert 200 == response.status_code
    assert 'notes/notes_list.html' in response.template_name
    assert 1 == logged_user.notes.count()
    assert "An impressive title" == logged_user.notes.first().title
