import json, uuid

DATA_PATH = 'lesson_ws/data/users.json'

def get_users() -> dict:
    with open(DATA_PATH, encoding='utf-8') as f:
        data = json.load(f)
    users_data = data.get('users_data', {}) 
    return users_data

def save_user(user_data: dict) -> None:
    id = str(uuid.uuid4())
    user_data.setdefault('id', id)
    with open(DATA_PATH, 'r+', encoding='utf-8') as f:
        data = f.read()
        if data:
            data = json.loads(data)
        else:
            data = {}
        users_data = data.setdefault('users_data', {})
        users_data[user_data['id']] = user_data
        data['users_data'] = users_data
        f.seek(0) 
        json.dump(data, f, indent=1)

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

def destroy(id) -> None:
    users_data = get_users()
    del users_data[id]
    data = {'users_data': users_data}
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1)    
