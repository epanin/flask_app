import json

DATA_PATH = 'lesson_ws/data/users.txt'

def get_users() -> list:
    with open(DATA_PATH, encoding='utf-8') as f:
        data = json.load(f)
    users_data = data.get('users_data', {})
    users_list = [info for info in users_data.values()] 
    return users_list

def save_user(user_data: dict) -> None:
    with open(DATA_PATH, 'w+r', encoding='utf-8') as f:
        data = json.load(f)
        users_data = data.get('users_data', {})
        users_data[user_data.id] = user_data
        data['users_data'] = users_data
        json.dump(users_data, f)

def find_user(id: str) -> dict|None:
    with open(DATA_PATH, encoding='utf-8') as f:
        data = json.load(f)
    users_data = data.get('users_data', {})
    user_info = users_data.get(id, None)
    return user_info

def validate(user_data: dict) -> dict:
    errors = {}
    if not user_data['name']:
        errors['name'] = "Can't be blank"
    if not user_data['email']:
        errors['email'] = "Can't be blank"
    return errors 