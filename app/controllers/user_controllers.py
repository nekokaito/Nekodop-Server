import uuid
from app.db.client import DB


db = DB()

# user register
def register_user(req):
    body = req.json()
    email = body.get('email')
    
    
     # Check if email already exists
    existing_user = db.get("SELECT id FROM users WHERE email = ?", (email,))
    if existing_user:
        res = {
            "error": "Email already registered."
        }
        req.send(409, res)  # 409 Conflict
        return
    
    #user registration
    user_id = str(uuid.uuid4())
    db.run(
      "INSERT INTO users (id,name, email, password, profile_picture) VALUES (?,?, ?, ?, ?)",
      (user_id , body.get('userName'), body.get('email'), body.get('password'), body.get('profilePicture'))
    )
    res ={
        "message": "User created",
        "user":{
            "id":user_id,
            "name": body.get('userName'),
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
    user_id = req.params['id'];
    user = db.get("SELECT * FROM users WHERE id = ?", (user_id,))
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

    name = body.get("userName", current_user["name"])
    email = body.get("email", current_user["email"])
    profile_picture = body.get("profilePicture", current_user["profile_picture"])

    db.run("""
        UPDATE users SET
            name = ?,
            email = ?,
            profile_picture = ?
        WHERE id = ?
    """, (
        name,
        email,
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
    
# update password   
def update_password(req):
    user_id = req.params["user_id"]
    body = req.json()

    current_password = body.get("currentPassword")
    new_password = body.get("newPassword")

    if not current_password or not new_password:
        return req.send(400, {"error": "Missing required fields."})

    user = db.get("SELECT * FROM users WHERE id = ?", (user_id,))
    if not user:
        return req.send(404, {"error": "User not found"})

    # Check if current password matches
    if user["password"] != current_password:
        return req.send(401, {"error": "Current password is incorrect"})

    # Update to new password
    db.run("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))

    return req.send(200, {"message": "Password updated successfully"})



# delete user
def delete_user(req):
    req_id = req.params["req_id"]
    user_id = req.params["user_id"]


    admin = db.get("SELECT * FROM users WHERE id = ? AND user_role = 'admin'", (req_id,))
    if not admin:
        return req.send(404, {"error": "User is not admin"})


    current_user = db.get("SELECT * FROM users WHERE id = ?", (user_id,))
    if not current_user:
        return req.send(404, {"error": "User not found"})

    db.run("DELETE FROM users WHERE id = ?", (user_id,))


    res = {
        "message": "User deleted successfully",
        "deletedUser": {
            "id": user_id
        }
    }
    req.send(200, res)



# is_admin
def is_admin(req):
    user_id = req.params['id']
    user = db.get("SELECT user_role FROM users WHERE id = ?", (user_id,))
    is_admin = True if user and user['user_role'] == 'admin' else False
    req.send(200, is_admin) 
    

