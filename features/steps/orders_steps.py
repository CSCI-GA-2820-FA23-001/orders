######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
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
######################################################################

"""
Orders Steps

Steps file for Recommendation.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given  # pylint: disable=no-name-in-module

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204


@given("the following orders")
def step_impl(context):
    """Delete all Recommendations and load new ones"""

    # List all of the orders and delete them one by one
    rest_endpoint = f"{context.base_url}/orders"
    context.resp = requests.get(rest_endpoint)
    assert context.resp.status_code == HTTP_200_OK
    for rec in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{rec['id']}")
        assert context.resp.status_code == HTTP_204_NO_CONTENT

    # load the database with new recommendations
    for row in context.table:
        payload = {
            "customer_id": int(row["Customer_ID"]),
            "status": row["Status"],
            "items": [],
            "total_price": 0
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        print(context.resp.status_code)
        assert context.resp.status_code == HTTP_201_CREATED
