from ..controllers.cat_controllers import (
    create_cat,
    get_cats,
    get_cats_by_owner,
    update_cat,
    delete_cat
)

def handel_cat_routes(app):
    # create cat
    @app.post("/create-cat")
    def create_cat_route(req):
        return create_cat(req)

    # get all cats
    @app.get("/get-cats")
    def route(req):
        return get_cats(req)

    # get cats by owner_id
    @app.get("/get-cats/:owner_id")
    def route(req):
        return get_cats_by_owner(req)

    # update cat by id
    @app.put("/update-cat/:cat_id")
    def route(req):
        return update_cat(req)

    # delete cat by id
    @app.delete("/delete-cat/:cat_id")
    def route(req):
        return delete_cat(req)
