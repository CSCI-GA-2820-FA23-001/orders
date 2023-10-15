"""
Order Creation and Updation Service

This microservice handles the lifecycle of Orders and the Items within.

Paths:
------
GET /orders - Returns a list all of the Orders
GET /orders/{id} - Returns the Order with a given id number
POST /orders - creates a new Order record in the database
PUT /orders/{id} - updates an Order record in the database
DELETE /orders/{id} - deletes an Order record in the database
GET /orders/{id}/items - Returns a list all of the Items in the Order with a given id number
GET /item/{item id} - Returns an Item with a given item id number
POST orders/{id}/items - creates a new Item record in the Order with a given id number
PUT /orders/{id}/items/{item id} - updates an Item record with a given item id in the Order with a given id number
DELETE /orders/{id}/items/{item id} - deletes an Item record with a given item id in the Order with a given id number

"""

from flask import jsonify, request, url_for, abort, make_response
from service.common import status  # HTTP Status Codes
from service.models import Order


# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Order Demo REST API Service",
            version="1.0",
            paths=url_for("list_orders", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Place your REST API code here ...


@app.route("/orders", methods=["GET"])
def list_orders():
    """Returns all of the Orders"""
    app.logger.info("Request for Order list")
    orders = []
    orders = Order.all()
    # Return as an array of dictionaries
    results = [order.serialize() for order in orders]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# READ AN ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["GET"])
def read_orders(order_id):
    """
    Retrieve a single Order

    This endpoint will return an Order based on it's id
    """
    app.logger.info("Request for Order with id: %s", order_id)

    # See if the order exists and abort if it doesn't
    order = Order.find(order_id)
    if not order:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Order with id '{order_id}' could not be found.",
        )

    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


######################################################################
# CREATE A NEW ORDER
######################################################################
@app.route("/orders", methods=["POST"])
def create_orders():
    """
    Creates an Order
    This endpoint will create an Order based the data in the body that is posted
    """
    app.logger.info("Request to create an order")
    check_content_type("application/json")
    order = Order()
    order.deserialize(request.get_json())
    order.create()
    message = order.serialize()
    location_url = url_for("read_orders", order_id=order.id, _external=True)

    app.logger.info("Order with ID [%s] created.", order.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
