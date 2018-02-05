from app import helpers
from . import models


def is_an_available_username(username):
    """Verify if an username is available.

    :username: a string object
    :returns: True or False

    """
    return models.User.objects(username=username).first() is None


def get_users():
    """Get all users info. Accepts specify an username.

    :id: int
    :returns: a dict with the operation result

    """
    users = []

    return {'success': [u.to_json2() for u in users]}


def create_or_update_user(username, password, user_id=None):
    """Creates or updates an user.

    :username: a string object
    :password: a string object (plaintext)
    :user_id: a str object. Indicates an update.
    :returns: a dict with the operation result

    """

    if is_an_available_username(username) is False:
        return {'error': 'The user {!r} already exists.'.format(username)}

    try:
        query = {'id': user_id} if user_id else {'username': username}
        result = models.User.objects(**query).update(
            set__username=username,
            set__password=helpers.encrypt_password(password),
            upsert=True,
            full_result=True
        )
    except Exception as e:
        return {'error': 'Error during the operation: {}'.format(e)}

    if result.get('updatedExisting') is False:
        return {'created': 'Created the user {!r}.'.format(username)}

    return {'updated': 'Updated the user {!r}.'.format(username)}


def delete_user(user_id):
    """Delete an user by user id.

    :user_id: a str object
    :returns: a dict with the operation result

    """

    user = models.User.objects(id=user_id).first()

    if not user:
        return {'error': 'Invalid user id.'}

    user.delete()
    return {'deleted': 'User deleted'}
