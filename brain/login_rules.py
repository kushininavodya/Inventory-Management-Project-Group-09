from brain.file_helper import read_json, save_json

# Works with user accounts .

def check_login(username, password):
    users = read_json("users.json")
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True
    return False

def add_new_user(username, password):
    users = read_json("users.json")
    for user in users:
        if user["username"] == username:
            return False, "Username already exists!"
    
    users.append({"username": username, "password": password})
    save_json("users.json", users)
    return True, "Sign up successful!"