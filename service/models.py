"""
Models for YourResourceModel

All of the models are stored in this module
"""
import logging
from abc import abstractmethod
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# Function to initialize the database
def init_db(app):
    """Initializes the SQLAlchemy app"""
    Order.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class PersistentBase:
    """Base class added persistent methods"""

    def __init__(self):
        self.id = None  # pylint: disable=invalid-name

    @abstractmethod
    def serialize(self) -> dict:
        """Convert an object into a dictionary"""

    @abstractmethod
    def deserialize(self, data: dict) -> None:
        """Convert a dictionary into an object"""

    def delete(self):
        """Removes an Order from the data store"""
        logger.info("Deleting an Order %d", self.id)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the records in the database"""
        logger.info("Processing all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a record by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)


class Item(db.Model, PersistentBase):
    """
    Class that represents an Address
    """

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(
        db.Integer, db.ForeignKey("order.id", ondelete="CASCADE"), nullable=False
    )
    name = db.Column(db.String(64))
    price = db.Column(db.Float(4))
    description = db.Column(db.String(128))
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return f"<Item {self.name} id=[{self.id}] order[{self.order_id}]>"

    def __str__(self):
        return f"{self.name}: {self.price}, {self.description}, {self.quantity}"

    def serialize(self) -> dict:
        """Converts an Order into a dictionary"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "quantity": self.quantity,
        }

    def deserialize(self, data: dict) -> None:
        """
        Populates an Item from a dictionary

        Args:
            data (dict): An itemcontaining the resource data
        """
        try:
            self.order_id = data["order_id"]
            self.name = data["name"]
            self.price = data["price"]
            self.description = data["description"]
            self.quantity = data["quantity"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Item: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Item: body of request contained "
                "bad or no data " + error.args[0]
            ) from error
        return self

    def create(self):
        """
        Creates an Order to the database
        """
        logger.info("Creating an order")
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates an Order to the database
        """
        logger.info("Updating an Order %d", self.id)
        db.session.commit()


class Order(db.Model, PersistentBase):
    """
    Class that represents an Order
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    creation_time = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    last_updated_time = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    items = db.relationship("Item", backref="order", passive_deletes=True)
    total_price = db.Column(db.Float(4))

    def __repr__(self):
        return f"<Order from {self.customer_id} id=[{self.id}]>"

    def serialize(self):
        """Serializes an Order into a dictionary"""
        order = {
            "id": self.id,
            "customer_id": self.customer_id,
            "creation_time": self.creation_time.isoformat(),
            "last_updated_time": self.last_updated_time.isoformat(),
            "items": [],
            "total_price": self.total_price,
        }

        for item in self.items:
            order["items"].append(item.serialize())

        return order

    def deserialize(self, data):
        """
        Deserializes an Order from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.customer_id = data["customer_id"]
            self.total_price = data["total_price"]
            # handle inner list of addresses
            item_list = data.get("items")
            for json_item in item_list:
                item = Item()
                item.deserialize(json_item)
                self.items.append(item)

        except KeyError as error:
            raise DataValidationError(
                "Invalid Order: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Order: body of request contained "
                "bad or no data - " + error.args[0]
            ) from error
        return self

    def get_total_price(self) -> float:
        """It can calculate the total price of the order"""
        total = float(0.0)
        for item in self.items:
            total += float(item.price) * float(item.quantity)

        return total

    def create(self):
        """
        Creates an Order to the database
        """
        logger.info("Creating an order")
        self.id = None  # id must be none to generate next primary key

        # Set the creation_time and last_updated_time as the time this function is called.
        self.creation_time = datetime.now()
        self.last_updated_time = self.creation_time

        # Calculate the total_price for the order

        self.total_price = self.get_total_price()

        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates an Order to the database
        """
        logger.info("Updating an Order %d", self.id)

        # Set the last_updated_time as the time this function is called.
        self.last_updated_time = datetime.now()

        # Calculate the total_price for the order

        self.total_price = self.get_total_price()
        print(self.total_price)

        db.session.commit()

    @classmethod
    def find_by_customer_id(cls, customer_id):
        """Returns all Orders with the given customer_id

        Args:
            customer_id (integer): the customer_id of the Order you want to match
        """
        logger.info("Processing customer_id query for %d ...", customer_id)
        return cls.query.filter(cls.customer_id == customer_id)

    def delete(self):
        """
        Deletes an Order in the database
        """
        logger.info("Deleting an order with the order ID %d", self.id)
        db.session.delete(self)
        db.session.commit()
