import uuid
from app.db.client import DB


db = DB()

# user register
def register_user(req):
    body = req.json()
    user_id = str(uuid.uuid4())
    db.run(
      "INSERT INTO users (id,name, email, password, profile_picture) VALUES (?,?, ?, ?, ?)",
      (user_id , body.get('user_name'), body.get('email'), body.get('password'), body.get('profilePicture'))
    )
    res ={
        "message": "User created",
        "user":{
            "id":user_id,
            "name": body.get('user_name'),
            "email": body.get('email'),
            "profilePicture": body.get('profilePicture'),
        }
    }
    req.send(200, res)

# use login
def login(req):
    body = req.json()
    email = body.get('email')
    password = body.get('password')
    user = db.get("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    print(dict(user) if user else "No user found")
    if user:
        user_dict = dict(user)
        req.send(200, {
            "message": "Login successful",
            "user": {
                "id": user_dict['id'],
                "name": user_dict['name'],
                "email": user_dict['email'],
                "profilePicture": user_dict['profile_picture']
            }
        })
    else:
        req.send(401, {"message": "Invalid email or password"})

# get user by id
def get_user(req):
    user = db.get("SELECT * FROM users WHERE id = ?", (req.params['id'],))
    res ={
        "message": "User retrieved successfully",
        "user": dict(user)
    }
    req.send(200, res)

# get users
def get_users(req):
    users = db.all("SELECT * FROM users")
    users_list = [dict(user) for user in users]
    res ={
        "message": "Users retrieved successfully",
        "users": users_list
    }
    req.send(200, res)
    
# update user
def update_user(req): 
    user_id = req.params["user_id"]
    body = req.json()


    current_user = db.get("SELECT * FROM users WHERE id = ?", (user_id,))
    if not current_user:
        return req.send(404, {"error": "User not found"})

    name = body.get("name", current_user["name"])
    email = body.get("email", current_user["email"])
    password = body.get("password", current_user["password"])
    profile_picture = body.get("profilePicture", current_user["profile_picture"])

    db.run("""
        UPDATE users SET
            name = ?,
            email = ?,
            password = ?,
            profile_picture = ?
        WHERE id = ?
    """, (
        name,
        email,
        password,
        profile_picture,
        user_id
    ))

    res ={
        "message": "User updated successfully",
        "updatedUser": {
            "id": user_id,
            "name": name,
            "email": email,
            "profilePicture": profile_picture
        }
    }
    req.send(200, res)

    

# is_admin
def is_admin(req):
    user_id = req.params['id']
    user = db.get("SELECT user_role FROM users WHERE id = ?", (user_id,))
    is_admin = True if user and user['user_role'] == 'admin' else False
    req.send(200, is_admin)

