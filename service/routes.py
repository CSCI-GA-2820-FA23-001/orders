"""
My Service

Describe what your service does here
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
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Place your REST API code here ...


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
