Feature: The orders service
    As a developer
    I need a RESTful catalog service
    So that I can keep track of all the orders

Background:
    Given the following orders
        |Customer_ID | Creation_Time | Last_Updated_Time | Item_List | Status      | Total_Price |
        |12345       | test          | test              | test      | PENDING     | 0           |
        |12345       | test          | test              | test      | DELIVERED     | 0         |
        |23456       | test          | test              | test      | DELIVERED   | 0           |
#     Given the following items
#         | Item_ID | Order_ID | Item_Name | Item_Price | Description | Quantity |
#         | test    | test     | test      | test       | test        | test     |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Orders RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create an Order
    When I visit the "Home Page"
    And I set the "Order" "Customer_ID" to "1"
    And I select "Pending" in the "Order" "Status" dropdown

    And I press the "Create Order" button
    Then I should see the message "Success"

Scenario: Repeat an Order
    When I visit the "Home Page"
    And I set the "Order" "Customer_ID" to "1"
    And I select "Pending" in the "Order" "Status" dropdown
    And I press the "Create Order" button

    And I press the "Repeat Order" button
    Then I should see the message "Success"

Scenario: Cancel an Order
    When I visit the "Home Page"
    And I set the "Order" "Customer_ID" to "1"
    And I select "Pending" in the "Order" "Status" dropdown

    And I press the "Create Order" button
    And I press the "Cancel Order" button
    Then I should see the message "Success"
    Then I should see "Canceled" in the "Order" "Status" dropdown


Scenario: Delete an Order
    When I visit the "Home Page"
    And I set the "Order" "Customer_ID" to "1"
    And I select "Pending" in the "Order" "Status" dropdown

    And I press the "Create Order" button
    And I press the "Delete Order" button
    Then I should see the message "Success"

    # When I copy the "Id" field
    # And I press the "Clear" button
    # Then the "Id" field should be empty
    # And the "Name" field should be empty
    # And the "Category" field should be empty
    # When I paste the "Id" field
    # And I press the "Retrieve" button
    # Then I should see the message "Success"
    # And I should see "Happy" in the "Name" field
    # And I should see "Hippo" in the "Category" field
    # And I should see "False" in the "Available" dropdown
    # And I should see "Male" in the "Gender" dropdown
    # And I should see "2022-06-16" in the "Birthday" field

Scenario: List all orders
    When I visit the "Home Page"
    And I press the "Clear Order" button
    And I press the "List Order" button
    Then I should see the message "Success"
    And I should see "PENDING" in the "Order" results
    And I should see "DELIVERED" in the "Order" results
    And I should not see "CANCELED" in the "Order" results

Scenario: Search for Orders with customer_id 12345
    When I visit the "Home Page"
    And I press the "Clear Order" button
    And I set the "Order" "Customer Id" to "12345"
    And I press the "List Order" button
    Then I should see the message "Success"
    And I should see "12345" in the "Order" results
    And I should not see "23456" in the "Order" results

Scenario: Search for PENDING orders
    When I visit the "Home Page"
    And I select "Pending" in the "Order" "Status" dropdown
    And I press the "List Order" button
    Then I should see the message "Success"
    And I should see "PENDING" in the "Order" results
    And I should not see "DELIVERED" in the "Order" results

# Scenario: Update a Pet
#     When I visit the "Home Page"
#     And I set the "Name" to "fido"
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "fido" in the "Name" field
#     And I should see "dog" in the "Category" field
#     When I change "Name" to "Loki"
#     And I press the "Update" button
#     Then I should see the message "Success"
#     When I copy the "Id" field
#     And I press the "Clear" button
#     And I paste the "Id" field
#     And I press the "Retrieve" button
#     Then I should see the message "Success"
#     And I should see "Loki" in the "Name" field
#     When I press the "Clear" button
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "Loki" in the results
#     And I should not see "fido" in the results