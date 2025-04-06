from config import Config

def authenticate_user(username, password):
    users = Config.USERS
    if username in users and users[username]['password'] == password:
        return {
            'username': username,
            'name': users[username]['name']
        }
    return None