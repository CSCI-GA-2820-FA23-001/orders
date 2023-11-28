# import os
import requests
from behave import given, when, then  # pylint: disable=no-name-in-module
import logging  # pylint: disable=unused-import
from selenium.webdriver.common.by import By  # pylint: disable=unused-import
from selenium.webdriver.support.ui import (
    Select,
    WebDriverWait,
)  # pylint: disable=unused-import
from selenium.webdriver.support import (
    expected_conditions,
)  # pylint: disable=unused-import

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204


@given("the server is started")
def step_impl(context):
    raise NotImplementedError("STEP: Given the server is started")


@when('I visit the "home page"')
def step_impl(context):
    raise NotImplementedError('STEP: When I visit the "home page"')


@then('I should see "Pet Demo REST API Service"')
def step_impl(context):
    raise NotImplementedError('STEP: Then I should see "Pet Demo REST API Service"')


@then('I should not see "404 Not Found"')
def step_impl(context):
    raise NotImplementedError('STEP: Then I not should see "404 Not Found"')


@given("the following pets")
def step_impl(context):
    """Delete all Pets and load new ones"""

    # List all of the pets and delete them one by one
    rest_endpoint = f"{context.base_url}/pets"
    context.resp = requests.get(rest_endpoint)
    assert context.resp.status_code == HTTP_200_OK
    for pet in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{pet['id']}")
        assert context.resp.status_code == HTTP_204_NO_CONTENT

    # load the database with new pets
    for row in context.table:
        payload = {
            "name": row["name"],
            "category": row["category"],
            "available": row["available"] in ["True", "true", "1"],
            "gender": row["gender"],
            "birthday": row["birthday"],
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        assert context.resp.status_code == HTTP_201_CREATED
