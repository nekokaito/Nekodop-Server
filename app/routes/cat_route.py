from ..controllers.cat_controllers import (
    create_cat,
    get_cat_by_id,
    get_cats,
    get_cats_by_owner,
    update_cat,
    delete_cat,
    get_cats_admin
)

def handel_cat_routes(app):
    # create cat (options and post)
    @app.options("/create-cat")
    def route(req):
        req.send(204, "")

    @app.post("/create-cat")
    def create_cat_route(req):
        return create_cat(req)

    # get all cats
    @app.get("/get-cats")
    def route(req):
        return get_cats(req)


    # get all cats (ADMIN)
    @app.get("/admin/get-cats")
    def route(req):
        return get_cats_admin(req)

    # get cat by oid
    @app.get("/get-cat/:id")
    def route(req):
        return get_cat_by_id(req)

    # get cats by owner_id
    @app.get("/get-cats/:owner_id")
    def route(req):
        return get_cats_by_owner(req)

    # update cat by id (options and put)
    @app.options("/update-cat/:cat_id")
    def route(req):
        req.send(204, "")

    @app.put("/update-cat/:cat_id")
    def route(req):
        return update_cat(req)

    # delete cat by id (delete and options)
    @app.options("/delete-cat/:cat_id")
    def route(req):
        req.send(204, "")

    @app.delete("/delete-cat/:cat_id")
    def route(req):
        return delete_cat(req)
