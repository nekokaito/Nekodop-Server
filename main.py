from app import App
from database import DB
import uuid

app = App()
db = DB()

# user register
@app.post("/register")
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
@app.post("/login")
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

# get users
@app.get("/get-users")
def get_users(req):
    users = db.all("SELECT * FROM users")
    users_list = [dict(user) for user in users]
    res ={
        "message": "Users retrieved successfully",
        "users": users_list
    }
    req.send(200, res)

# create cat
@app.post("/create-cat")
def create_cat(req):
    body = req.json()
    cat_id = str(uuid.uuid4())
    cat = db.run(
    """
    INSERT INTO cats (
        id,
        cat_owner_id,
        cat_name,
        cat_image,
        cat_age,
        cat_gender,
        cat_description,
        owner_name,
        owner_address,
        owner_phone,
        owner_email,
        adopted,
        additional_information
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        cat_id,
        body.get('catOwnerId'),
        body.get('catName'),
        body.get('catImage'),
        body.get('catAge'),
        body.get('catGender'),
        body.get('catDescription'),
        body.get('ownerName'),
        body.get('ownerAddress'),
        body.get('ownerPhone'),
        body.get('ownerEmail'),
        int(body.get('adopted')),
        body.get('additionalInformation')
    )
)

    res = {
  "message": "Cat posted for adoption",
  "catPost": body
}

    req.send(200, res)

# get cats
@app.get("/get-cats")
def get_cats(req):
    cats = db.all("SELECT * FROM cats")
    cats_list = [dict(cat) for cat in cats]
    res = {
        "message": "Cats retrieved successfully",
        "cats": cats_list
    }
    req.send(200, res)

# get cat by owner id
@app.get("/get-cats/:owner_id")
def get_cats_by_owner(req):
    owner_id = req.params["owner_id"]
    cats = db.all("SELECT * FROM cats WHERE cat_owner_id = ?", (owner_id,))
    cats_list = [dict(cat) for cat in cats]
    res = {
        "message": "Cats retrieved successfully",
        "cats": cats_list
    }
    req.send(200, res)

# update cat by id
@app.put("/update-cat/:cat_id")
def update_cat(req):
    cat_id = req.params["cat_id"]
    body = req.json()


    current_cat = db.get("SELECT * FROM cats WHERE id = ?", (cat_id,))
    if not current_cat:
        return req.send(404, {"error": "Cat not found"})


    cat_name = body.get("catName", current_cat["cat_name"])
    cat_image = body.get("catImage", current_cat["cat_image"])
    cat_age = body.get("catAge", current_cat["cat_age"])
    cat_gender = body.get("catGender", current_cat["cat_gender"])
    cat_description = body.get("catDescription", current_cat["cat_description"])
    owner_address = body.get("ownerAddress", current_cat["owner_address"])
    owner_phone = body.get("ownerPhone", current_cat["owner_phone"])
    owner_email = body.get("ownerEmail", current_cat["owner_email"])
    adopted = body.get("adopted", current_cat["adopted"])
    additional_info = body.get("additionalInformation", current_cat["additional_information"])

    db.run("""
        UPDATE cats SET
            cat_name = ?,
            cat_image = ?,
            cat_age = ?,
            cat_gender = ?,
            cat_description = ?,
            owner_address = ?,
            owner_phone = ?,
            owner_email = ?,
            adopted = ?,
            additional_information = ?
        WHERE id = ?
    """, (
        cat_name,
        cat_image,
        cat_age,
        cat_gender,
        cat_description,
        owner_address,
        owner_phone,
        owner_email,
        int(adopted),
        additional_info,
        cat_id
    ))

    res ={
        "message": "Cat updated successfully",
        "updatedCat": body
    }
    req.send(200, res)

# delete cat by id
@app.delete("/delete-cat/:cat_id")
def delete_cat(req):
    cat_id = req.params["cat_id"]


    current_cat = db.get("SELECT * FROM cats WHERE id = ?", (cat_id,))
    if not current_cat:
        return req.send(404, {"error": "Cat not found"})

    db.run("DELETE FROM cats WHERE id = ?", (cat_id,))  # Correct tuple syntax


    res = {
        "message": "Cat deleted successfully",
        "deletedCat": {
            "id": cat_id
        }
    }
    req.send(200, res)


app.run()
