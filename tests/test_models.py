"""
Test cases for YourResourceModel Model

"""
import os
import logging
import unittest
from service import app
from service.models import Order, Item, DataValidationError, db
from tests.factories import OrderFactory, ItemFactory





DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  YourResourceModel   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestOrder(unittest.TestCase):
    """Test Cases for YourOrder Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Order.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""
        db.session.query(Order).delete()  # clean up the last tests
        db.session.query(Item).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_an_order(self):
        """It should Create an Order and assert that it exists"""
        fake_order = OrderFactory()
        # pylint: disable=unexpected-keyword-arg
        order = Order(
            customer_id=fake_order.customer_id,
            creation_time=fake_order.creation_time,
            last_updated_time=fake_order.last_updated_time,
            status=fake_order.status,
            total_price=fake_order.total_price,
        )
        # print(repr(order))
        self.assertIsNotNone(order)
        self.assertEqual(order.id, None)
        self.assertEqual(order.customer_id, fake_order.customer_id)
        self.assertEqual(order.creation_time, fake_order.creation_time)
        self.assertEqual(order.last_updated_time, fake_order.last_updated_time)
        self.assertEqual(order.status, fake_order.status)
        self.assertAlmostEqual(order.total_price, fake_order.total_price)

    def test_add_an_order(self):
        """It should Create an Order and add it to the database"""
        orders = Order.all()
        self.assertEqual(orders, [])
        order = OrderFactory()
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)

        orders = Order.all()
        self.assertEqual(len(orders), 1)

    def test_read_order(self):
        """It should Read an Order"""
        order = OrderFactory()
        order.create()

        # Read it back
        found_order = Order.find(order.id)
        self.assertEqual(found_order.id, order.id)
        self.assertEqual(found_order.customer_id, order.customer_id)
        self.assertEqual(found_order.creation_time, order.creation_time)
        self.assertEqual(found_order.last_updated_time, order.last_updated_time)
        self.assertEqual(found_order.status, order.status)
        self.assertAlmostEqual(found_order.total_price, order.total_price)
        self.assertEqual(found_order.items, [])

    def test_update_order(self):
        """It should Update an Order"""
        order = OrderFactory(customer_id=1)
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        self.assertEqual(order.customer_id, 1)
        self.assertEqual(order.creation_time, order.last_updated_time)

        # Fetch it back
        order = Order.find(order.id)
        order.customer_id = 2
        order.update()

        # Fetch it back again, total_price would change and last_updated_time would be changed
        order = Order.find(order.id)
        self.assertEqual(order.customer_id, 2)
        self.assertNotEqual(order.creation_time, order.last_updated_time)

    def test_delete_an_order(self):
        """It should Delete an Order from the database"""
        orders = Order.all()
        self.assertEqual(orders, [])
        order = OrderFactory()
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1)
        order = orders[0]
        order.delete()
        orders = Order.all()
        self.assertEqual(len(orders), 0)

    def test_list_all_orders(self):
        """It should List all Orders in the database"""
        orders = Order.all()
        self.assertEqual(orders, [])
        for order in OrderFactory.create_batch(5):
            order.create()
        # Assert that there are not 5 orders in the database
        orders = Order.all()
        self.assertEqual(len(orders), 5)

    def test_find_by_customer_id(self):
        """It should Find all Orders by customer_id"""
        order = OrderFactory()
        order.create()

        # Fetch it back by name
        same_account = Order.find_by_customer_id(order.customer_id)[0]
        self.assertEqual(same_account.id, order.id)
        self.assertEqual(same_account.customer_id, order.customer_id)

    def test_find_by_status(self):
        """It should Find all Orders by status"""
        order = OrderFactory()
        order.create()

        # Fetch it back by status
        same_account = Order.find_by_status(order.status)[0]
        self.assertEqual(same_account.id, order.id)
        self.assertEqual(same_account.status, order.status)

    def test_find_by_date(self):
        """It should find all orders by date"""
        order = OrderFactory()
        order.create()

        # Fetch it back by status
        # date_string = order.creation_time
        # date_format = "%Y-%m-%dT%H:%M:%S.%f"
        # date_obj = datetime.strptime(date_string, date_format)
        same_account = Order.find_by_date(
            order.creation_time.date().strftime("%Y-%m-%d")
        )[0]
        self.assertEqual(same_account.id, order.id)
        self.assertEqual(same_account.creation_time.date(), order.creation_time.date())

    def test_serialize_an_order(self):
        """It should Serialize an Order"""
        order = OrderFactory()
        item = ItemFactory()
        order.items.append(item)
        serial_order = order.serialize()
        self.assertEqual(serial_order["id"], order.id)
        self.assertEqual(serial_order["customer_id"], order.customer_id)
        self.assertEqual(serial_order["creation_time"], order.creation_time.isoformat())
        self.assertEqual(
            serial_order["last_updated_time"], order.last_updated_time.isoformat()
        )
        self.assertEqual(serial_order["status"], order.status)
        self.assertAlmostEqual(serial_order["total_price"], order.total_price)
        self.assertEqual(len(serial_order["items"]), 1)
        items = serial_order["items"]
        self.assertEqual(items[0]["id"], item.id)
        self.assertEqual(items[0]["order_id"], item.order_id)
        self.assertEqual(items[0]["name"], item.name)
        self.assertAlmostEqual(items[0]["price"], item.price)
        self.assertEqual(items[0]["description"], item.description)
        self.assertEqual(items[0]["quantity"], item.quantity)

    def test_deserialize_an_order(self):
        """It should Deserialize an Order"""
        order = OrderFactory()
        order.items.append(ItemFactory())
        order.create()
        order = Order.find(order.id)
        serial_order = order.serialize()
        new_order = Order()
        new_order.deserialize(serial_order)
        self.assertEqual(new_order.customer_id, order.customer_id)
        self.assertEqual(new_order.status, order.status)
        self.assertAlmostEqual(new_order.total_price, order.total_price)

    def test_deserialize_order_with_key_error(self):
        """It should not Deserialize an Order with a KeyError"""
        order = Order()
        self.assertRaises(DataValidationError, order.deserialize, {})

    def test_deserialize_order_with_type_error(self):
        """It should not Deserialize an Order with a TypeError"""
        order = Order()
        self.assertRaises(DataValidationError, order.deserialize, [])

    def test_deserialize_item_key_error(self):
        """It should not Deserialize an Item with a KeyError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, {})

    def test_deserialize_item_type_error(self):
        """It should not Deserialize an Item with a TypeError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, [])

    def test_add_order_item(self):
        """It should Create an order with an item and add it to the database"""
        orders = Order.all()
        self.assertEqual(orders, [])
        order = OrderFactory()
        order.create()
        # print(order.total_price)

        # fake_item = ItemFactory()
        # pylint: disable=unexpected-keyword-arg
        item = Item(
            order_id=order.id,
            name="food",
            price=2.32,
            description="this is some food",
            quantity=2,
        )
        # order.items.append(item)
        item.create()
        # print(repr(item))

        order.update()

        # print(order.total_price)

        # order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1)
        # order = Order.find(order.id)
        self.assertEqual(len(order.items), 1)
        self.assertAlmostEqual(order.items[0].price, item.price)
        self.assertEqual(order.items[0].quantity, item.quantity)
        # print(order.total_price)
        self.assertAlmostEqual(order.total_price, item.price * item.quantity)

        new_order = Order.find(order.id)
        self.assertEqual(new_order.items[0].name, item.name)

        item2 = Item(
            order_id=order.id,
            name="food",
            price=4.44,
            description="this is some food",
            quantity=2,
        )
        order.items.append(item2)
        order.update()

        new_order = Order.find(order.id)
        self.assertEqual(len(new_order.items), 2)
        self.assertEqual(new_order.items[1].name, item2.name)
        self.assertAlmostEqual(
            order.total_price, item.price * item.quantity + item2.price * item2.quantity
        )

    def test_update_order_item(self):
        """It should Update an order's item"""
        orders = Order.all()
        self.assertEqual(orders, [])

        order = OrderFactory()
        item = ItemFactory(order=order)
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        self.assertEqual(order.creation_time, order.last_updated_time)
        self.assertAlmostEqual(order.total_price, item.price * item.quantity)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

        # Fetch it back
        order = Order.find(order.id)
        old_item = order.items[0]
        # print("%r", old_item)
        self.assertEqual(old_item.name, item.name)
        # Change the city
        old_item.name = "drink"
        old_item.update()
        # order.update()

        # Fetch it back again
        order = Order.find(order.id)

        item = order.items[0]
        self.assertEqual(item.name, "drink")
        item.quantity = 0
        order.update()

        order = Order.find(order.id)
        self.assertNotEqual(order.creation_time, order.last_updated_time)
        self.assertAlmostEqual(order.total_price, 0)

    def test_delete_order_item(self):
        """It should Delete an order's item"""
        orders = Order.all()
        self.assertEqual(orders, [])

        order = OrderFactory()
        item = ItemFactory(order=order)
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

        # Fetch it back
        order = Order.find(order.id)
        item = order.items[0]
        item.delete()
        order.update()

        # Fetch it back again
        order = Order.find(order.id)
        self.assertEqual(len(order.items), 0)

    def test_list_all_order_items(self):
        """It should List all items in the database"""
        orders = Order.all()
        self.assertEqual(orders, [])

        order = OrderFactory()
        order.create()

        self.assertEqual(order.items, [])
        for item in ItemFactory.create_batch(5):
            item.create()
            order.items.append(item)
            order.update()
        # Assert that there are not 5 items in the database
        items = Item.all()
        self.assertEqual(len(items), 5)
        self.assertEqual(len(order.items), 5)

    def test_copy_an_order(self):
        """It should make a duplicate of an order and save to the database"""

        orders = Order.all()
        self.assertEqual(orders, [])

        order = OrderFactory()
        order.create()

        self.assertEqual(order.items, [])
        for item in ItemFactory.create_batch(5):
            item.create()
            order.items.append(item)
            order.update()
        # Assert that there are not 5 items in the database
        items = Item.all()
        self.assertEqual(len(items), 5)
        self.assertEqual(len(order.items), 5)

        new_order = order.copy()
        self.assertNotEqual(order.id, new_order.id)
        self.assertEqual(order.customer_id, new_order.customer_id)
        self.assertEqual(order.status, new_order.status)
        self.assertEqual(len(order.items), len(new_order.items))

        def test_item_is_copy(item_x, item_y):
            self.assertNotEqual(item_x.id, item_y.id)
            self.assertEqual(new_order.id, item_y.order_id)
            self.assertEqual(item_x.name, item_y.name)
            self.assertAlmostEqual(item_x.price, item_y.price)
            self.assertEqual(item_x.description, item_y.description)
            self.assertEqual(item_x.quantity, item_y.quantity)

        for i, item1 in enumerate(order.items):
            item2 = new_order.items[i]
            test_item_is_copy(item1, item2)
