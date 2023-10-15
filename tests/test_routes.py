"""
Order and Item API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from service import app
from service.models import db, init_db, Order, Item
from service.common import status  # HTTP Status Codes
from tests.factories import OrderFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/orders"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestOrderItemServer(TestCase):
    """Order and Item Server Tests"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        self.client = app.test_client()
        db.session.query(Order).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def _create_orders(self, count):
        """Factory method to create pets in bulk"""
        orders = []
        for _ in range(count):
            test_order = OrderFactory()
            response = self.client.post(BASE_URL, json=test_order.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test pet",
            )
            new_order = response.get_json()
            test_order.id = new_order["id"]
            orders.append(test_order)
        return orders

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_order_list(self):
        """It should Get a list of Accounts"""
        self._create_orders(5)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_read_order(self):
        """It should get the order detail by sending the id"""

        order = self._create_orders(1)[0]
        resp = self.client.get(
            f"{BASE_URL}/{order.id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["customer_id"], order.customer_id)
        # self.assertEqual(data["creation_time"], order.creation_time)
        # self.assertEqual(data["last_updated_time"], order.last_updated_time)

    def test_read_order_not_found(self):
        """It should not Read an Order that is not found"""
        resp = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_order(self):
        """It should Create a new Order"""
        order = OrderFactory()
        resp = self.client.post(
            BASE_URL, json=order.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_order = resp.get_json()
        print(new_order)
        self.assertEqual(
            new_order["customer_id"],
            order.customer_id,
            "Customer Id does not match",
        )
        self.assertEqual(
            new_order["total_price"], order.total_price, "Total price does not match"
        )
        self.assertEqual(new_order["items"], order.items, "Items don't not match")
        # self.assertEqual(
        #     new_order["creation_time"],
        #     str(order.creation_time),
        #     "Creation time does not match",
        # )
        # self.assertEqual(
        #     new_order["last_updated_time"],
        #     str(order.last_updated_time),
        #     "Last updated time does not match",
        # )

        # Check that the location header was correct by getting it
        resp = self.client.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_order = resp.get_json()

        self.assertEqual(
            new_order["customer_id"], order.customer_id, "Customer Id does not match"
        )
        self.assertEqual(
            new_order["total_price"], order.total_price, "Total price does not match"
        )
        self.assertEqual(new_order["items"], order.items, "Items don't not match")
        # self.assertEqual(
        #     new_order["creation_time"],
        #     str(order.creation_time),
        #     "Creation time does not match",
        # )
        # self.assertEqual(
        #     new_order["last_updated_time"],
        #     str(order.last_updated_time),
        #     "Last updated time does not match",
        # )
