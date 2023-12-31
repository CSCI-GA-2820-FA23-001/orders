# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""

from datetime import datetime
import factory
from factory.fuzzy import (
    FuzzyChoice,
    FuzzyInteger,
    FuzzyFloat,
    FuzzyText,
)
from service.models import Order, Item


class FuzzyDecimal(factory.fuzzy.BaseFuzzyAttribute):
    """
    Generate random Decimal values
    """

    def __init__(self, low, high, precision):
        super().__init__()
        self.low = low
        self.high = high
        self.precision = precision

    def fuzz(self):
        value = FuzzyFloat(self.low, self.high).fuzz()
        return round(value, self.precision)


class OrderFactory(factory.Factory):
    """Creates fake Orders"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Persistent class"""

        model = Order

    id = factory.Sequence(lambda n: n)
    customer_id = FuzzyInteger(0, 100)
    creation_time = datetime.now()
    last_updated_time = datetime.now()
    total_price = 0.0
    status = FuzzyChoice(
        choices=["shipped", "cancelled", "finished", "delivered", "submitted"]
    )
    # the many side of relationships can be a little wonky in factory boy:
    # https://factoryboy.readthedocs.io/en/latest/recipes.html#simple-many-to-many-relationship

    @factory.post_generation
    def items(
        self, create, extracted, **kwargs
    ):  # pylint: disable=method-hidden, unused-argument
        """Creates the item list"""
        if not create:
            return

        if extracted:
            self.items = extracted


class ItemFactory(factory.Factory):
    """Creates fake Items"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Persistent class"""

        model = Item

    id = factory.Sequence(lambda n: n)
    order_id = None
    name = FuzzyChoice(choices=["food", "furniture", "tool"])
    price = FuzzyDecimal(0.01, 100.00, 2)
    description = FuzzyText("This is a ", 30)
    quantity = FuzzyInteger(1, 10)
    order = factory.SubFactory(OrderFactory)
