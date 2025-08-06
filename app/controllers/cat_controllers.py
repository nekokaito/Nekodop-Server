import uuid
from app.db.client import DB



db = DB()
# create cat
def create_cat(req):
    body = req.json()
    cat_id = str(uuid.uuid4())
    db.run(
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
def get_cats(req):
    cats = db.all("SELECT * FROM cats WHERE adopted = 0 AND is_approved = 1")
    cats_list = [dict(cat) for cat in cats]
    res = {
        "message": "Cats retrieved successfully",
        "cats": cats_list
    }
    req.send(200, res)

# get cats (admin)
def get_cats_admin(req):
    cats = db.all("SELECT * FROM cats")
    cats_list = [dict(cat) for cat in cats]
    res = {
        "message": "Cats retrieved successfully",
        "cats": cats_list
    }
    req.send(200, res)

# get cat by id
def get_cat_by_id(req):
    cat_id = req.params["id"]
    print(cat_id)
    cat = db.get("SELECT * FROM cats WHERE id = ?",(cat_id,))
    print(cat)
    res = {
        "message": "Cat retrieved successfully",
        "cat": dict(cat)
    }
    req.send(200,res)
    
# get cat by owner id
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
    is_approved = body.get("isApproved", current_cat["is_approved"])
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
            is_approved = ?,
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
        int(is_approved),
        additional_info,
        cat_id
    ))

    res ={
        "message": "Cat updated successfully",
        "updatedCat": body
    }
    req.send(200, res)

# delete cat by id
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
