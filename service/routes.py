"""
Order Creation and Updating Service

This microservice handles the lifecycle of Orders and the Items within.

Paths:
------
GET /orders - Returns a list all of the Orders
GET /orders/{id} - Returns the Order with a given id number
POST /orders - creates a new Order record in the database
PUT /orders/{id} - updates an Order record in the database
DELETE /orders/{id} - deletes an Order record in the database
GET /orders/{id}/items - Returns a list all of the Items in the Order with a given id number
GET /orders/{id}/items/{item id} - Returns an Item with a given item id number
POST orders/{id}/items - creates a new Item record in the Order with a given id number
PUT /orders/{id}/items/{item id} -
updates an Item record with a given item id in the Order with a given id number
DELETE /orders/{id}/items/{item id} -
deletes an Item record with a given item id in the Order with a given id number
POST /orders/{id}/repeat - creates a copy of an existing Order in the database
PUT /orders/{id}/cancel - cancels an order
"""

from flask import jsonify, abort
from flask_restx import Resource, fields, reqparse
from service.common import status  # HTTP Status Codes
from service.models import Order, Item

# Import Flask application
from . import app, api


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return app.send_static_file("index.html")


# Define the model so that the docs reflect what can be sent
create_orders_model = api.model(
    "Orders",
    {
        "customer_id": fields.Integer(required=True, description="Customer ID"),
        "total_price": fields.Float(
            required=False,
            description="The total price of the order",
        ),
        "items": fields.List(
            fields.String, required=False, description="List of items in the order"
        ),
        "status": fields.String(required=True, description="The status of the order"),
        "creation_time": fields.DateTime(
            required=False, description="The creation time of the order"
        ),
        "last_updated_time": fields.DateTime(
            required=False, description="The last updated time of the order"
        )
        # pylint: disable=protected-access
    },
)

orders_model = api.inherit(
    "OrdersModel",
    create_orders_model,
    {
        "id": fields.Integer(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)

# query string arguments
orders_args = reqparse.RequestParser()
orders_args.add_argument(
    "customer_id",
    type=int,  #changed from str
    location="args",
    required=False,
    help="List Orders by customer ID",
)
orders_args.add_argument(
    "date", type=str, location="args", required=False, help="List Orders by date"
)
orders_args.add_argument(
    "status",
    type=str,
    location="args",
    required=False,
    help="List Orders by status",
)

######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# CHECK HEALTH
######################################################################
@app.route("/health")
def health():
    """Health URL response"""
    app.logger.info("Request for Health URL")
    return (
        jsonify(
            status="OK",
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  PATH: /orders/{id}
######################################################################
@api.route("/orders/<order_id>")
@api.param("order_id", "The Order identifier")
class OrdersResource(Resource):
    """
    OrdersResource class

    Allows the manipulation of a single Order
    GET /orders/{id} - Returns an Order with the id
    PUT /orders/{id} - Update an Order with the id
    DELETE /orders/{id} -  Deletes an Order with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE AN ORDER
    # ------------------------------------------------------------------
    @api.doc("get_order")
    @api.response(404, "Order not found")
    def get(self, order_id):
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

        return order.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING ORDER
    # ------------------------------------------------------------------
    @api.doc("update_order")
    @api.response(404, "Order not found")
    @api.response(400, "The posted Order data was not valid")
    @api.expect(orders_model)
    @api.marshal_with(orders_model)
    def put(self, order_id):
        """
        Update an Order

        This endpoint will update an Order based the body that is posted
        """
        app.logger.info("Request to update order with id: %s", order_id)

        # See if the order exists and abort if it doesn't
        order = Order.find(order_id)
        if not order:
            abort(
                status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found."
            )

        # Update from the json in the body of the request
        order.deserialize(api.payload)
        order.id = order_id
        order.update()

        return order.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN ORDER
    # ------------------------------------------------------------------
    @api.doc("delete_order")
    @api.response(204, "Order deleted")
    def delete(self, order_id):
        """
        Deletes an Order
        This endpoint will delete an Order with the ID given.
        """
        app.logger.info("Request to delete an order with order ID %s", order_id)

        # See if the order exists and delete if it exists
        order = Order.find(order_id)
        if order:
            order.delete()
            app.logger.info("Order with id [%s] was deleted", order_id)

        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /orders
######################################################################
@api.route("/orders", strict_slashes=False)
class OrdersCollection(Resource):
    """Handles all interactions with collections of Orders"""

    # ------------------------------------------------------------------
    # LIST ALL ORDERS
    # ------------------------------------------------------------------
    @api.doc("list_orders")
    @api.expect(orders_args, validate=False)
    # @api.marshal_list_with(orders_model)
    def get(self):
        """Returns all of the Orders"""
        app.logger.info("Request for Order list")
        orders = []
        args = orders_args.parse_args()
        customer_id = args["customer_id"]
        date = args["date"]
        order_status = args["status"]
        if customer_id:
            orders = Order.find_by_customer_id(customer_id)
        elif date:
            orders = Order.find_by_date(date)
        elif order_status:
            orders = Order.find_by_status(order_status)
        else:
            orders = Order.all()

        # Return as an array of dictionaries
        results = [order.serialize() for order in orders]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW ORDER
    # ------------------------------------------------------------------
    @api.doc("create_order")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_orders_model)
    @api.marshal_with(orders_model, code=201)
    def post(self):
        """
        Creates an Order
        This endpoint will create an Order based the data in the body that is posted
        """
        app.logger.info("Request to create an order")
        order = Order()
        order.deserialize(api.payload)
        order.create()
        message = order.serialize()
        location_url = api.url_for(OrdersResource, order_id=order.id, _external=True)

        app.logger.info("Order with ID [%s] created.", order.id)
        return message, status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  PATH: /orders/{id}/cancel
######################################################################
@api.route("/orders/<order_id>/cancel")
@api.param("order_id", "The Order identifier")
class CancelResource(Resource):
    """Cancel actions on a Order"""

    @api.doc("cancel_order")
    @api.response(404, "Order not found")
    def put(self, order_id):
        """
        Cancel an Order
        This endpoint will cancel an Order with the ID given.
        """
        app.logger.info("Request to cancel an order with order ID %s", order_id)

        # See if the order exists and delete if it exists
        order = Order.find(order_id)
        if not order:
            abort(
                status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found."
            )

        order.status = "Canceled"
        order.update()
        # changing prices to strings because Decimals can't be serialized

        return order.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /orders/{id}/repeat
######################################################################
@api.route("/orders/<order_id>/repeat")
@api.param("order_id", "The Order identifier")
class RepeatResource(Resource):
    """Repeat actions on a Order"""

    @api.doc("repeat_order")
    # @api.marshal_with(orders_model, code=200)
    def post(self, order_id):
        """
        Repeat an Order
        This endpoint will repeat an Order with the ID given.
        """
        app.logger.info("Request to repeat an order with order ID %s", order_id)

        # See if the order exists and delete if it exists
        order = Order.find(order_id)
        if not order:
            abort(
                status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found."
            )

        new_order = order.copy()

        return new_order.serialize(), status.HTTP_200_OK


create_items_model = api.model(
    "Items",
    {
        "order_id": fields.Integer(required=True, description="Order ID"),
        "name": fields.String(
            required=False,
            description="The name of item",
        ),
        "price": fields.Float(required=False, description="The price of item"),
        "description": fields.String(
            required=False, description="The description of item"
        ),
        "quantity": fields.Integer(required=False, description="The quantity of item")
        # pylint: disable=protected-access
    },
)

items_model = api.inherit(
    "ItemsModel",
    create_items_model,
    {
        "id": fields.Integer(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)


######################################################################
#  PATH: /orders/<order_id>/items/<item_id>
######################################################################
@api.route("/orders/<order_id>/items/<item_id>")
@api.param("order_id", "The Order identifier")
@api.param("item_id", "The Item identifier")
class ItemsResource(Resource):
    """
    ItemsResource class

    Allows the manipulation of a single Item
    GET /orders/<order_id>/items/<item_id> -
    Returns an Item with the item_id inside order with order_id
    PUT /orders/<order_id>/items/<item_id> -
    Update an Item with the item_id inside order with order_id
    DELETE /orders/<order_id>/items/<item_id> -
    Deletes an Item with the item_id inside order with order_id
    """

    # ------------------------------------------------------------------
    # RETRIEVE AN ITEM
    # ------------------------------------------------------------------
    @api.doc("get_item")
    @api.response(404, "Item not found")
    @api.marshal_with(items_model)
    def get(self, order_id, item_id):
        """
        Get an Item

        This endpoint returns just an item
        """
        app.logger.info("Request to get Item %s for Order id: %s", item_id, order_id)

        # See if the item exists and abort if it doesn't
        item = Item.find(item_id)
        if not item:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Item with id '{item_id}' could not be found.",
            )

        return item.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING ITEM
    # ------------------------------------------------------------------
    @api.doc("update_item")
    @api.response(404, "Item not found")
    @api.response(400, "The posted Item data was not valid")
    @api.expect(items_model)
    @api.marshal_with(items_model)
    def put(self, order_id, item_id):
        """
        Update an Item

        This endpoint will update an item based the body that is posted
        """
        app.logger.info("Request to update item %s for order id: %s", item_id, order_id)

        # See if the item exists and abort if it doesn't
        item = Item.find(item_id)
        if not item:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Item with id '{item_id}' could not be found.",
            )
        order = Order.find(order_id)
        # Update from the json in the body of the request
        item.deserialize(api.payload)
        item.id = item_id
        item.update()
        order.update()

        return item.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN ITEM
    # ------------------------------------------------------------------
    @api.doc("delete_item")
    @api.response(204, "Item deleted")
    def delete(self, order_id, item_id):
        """
        Delete an Item

        This endpoint will delete an Item based the item id specified in the path
        """
        app.logger.info("Request to delete Item %s for Order id: %s", item_id, order_id)

        # See if the item exists and delete it if it does
        item = Item.find(item_id)
        order = Order.find(order_id)
        if item:
            item.delete()
        order.update()

        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /orders/<order_id>/items
######################################################################
@api.route("/orders/<order_id>/items", strict_slashes=False)
class ItemsCollection(Resource):
    """Handles all interactions with collections of Items"""

    # ------------------------------------------------------------------
    # LIST ALL ITEMS OF AN ORDER
    # ------------------------------------------------------------------
    @api.doc("list_items")
    @api.response(404, "Order not found")
    @api.marshal_list_with(items_model)
    def get(self, order_id):
        """Returns all of the items for an order"""
        app.logger.info("Request for all items for order with id: %s", order_id)

        # See if the order exists and abort if it doesn't
        order = Order.find(order_id)
        if not order:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Order with id '{order_id}' could not be found.",
            )

        # Get the items for the order
        results = [item.serialize() for item in order.items]

        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW ITEM TO AN ORDER
    # ------------------------------------------------------------------
    @api.doc("add_item")
    @api.response(400, "The posted data was not valid")
    @api.response(404, "Order not found")
    @api.expect(create_items_model)
    @api.marshal_with(items_model, code=201)
    def post(self, order_id):
        """
        Create an item in order

        This endpoint will create an item to an order
        """
        app.logger.info("Request to create an item for order with id: %s", order_id)

        # See if the order exists and abort if it doesn't
        order = Order.find(order_id)
        if not order:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Order with id '{order_id}' could not be found.",
            )

        # Create an item from the json data
        item = Item()
        item.deserialize(api.payload)

        # Append the item to the order
        order.items.append(item)
        order.update()

        # Prepare a message to return
        message = item.serialize()
        # print(message)

        return message, status.HTTP_201_CREATED
