from http import HTTPStatus
from src.app import User, Role, db

def test_get_user_sucess(client):
    # Given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username='john-doe', password='test', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    # When
    response = client.get(f"/users/{user.id}")
    
    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": user.id,
        "username": user.username,
    }


def test_get_not_found(client):
    # Given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user_id = 1

    # When
    response = client.get(f"/users/{user_id}")
    
    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_list_users(client):
    # Given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username='john-doe', password='test', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post('/auth/login', json={'username': user.username, 'password': user.password})
    access_token = response.json["access_token"]

    # When
    response = client.get(f"/users/", headers={'Authorization': f'Bearer {access_token}'})
    
    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "users": [
        {
            "id": user.id,
            "username": user.username,
            "role": {
                "id": user.role.id,
                "name": user.role.name
                }
        }
    ]

    }
    