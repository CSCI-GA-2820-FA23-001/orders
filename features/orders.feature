Feature: The orders service
    As a developer
    I need a RESTful catalog service
    So that I can keep track of all the orders

    Background:
        Given the following orders
            | Customer_ID | Creation_Time | Last_Updated_Time | Item_List | Status    | Total_Price |
            | 12345       | test          | test              | test      | PENDING   | 0           |
            | 12345       | test          | test              | test      | DELIVERED | 0           |
            | 23456       | test          | test              | test      | DELIVERED | 0           |
    

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

    Scenario: Update an Order
        When I visit the "Home Page"
        And I set the "Order" "Customer ID" to "23456"
        And I press the "List Order" button
        Then I should see the message "Success"
        And I should see "23456" in the "Order" "Customer ID" field
        And I should see "Delivered" in the "Order" "Status" dropdown
        When I change "Order" "Customer ID" to "34567"
        And I press the "Update Order" button
        Then I should see the message "Success"
        When I copy the "Order" "Order Id" field
        And I press the "Clear Order" button
        And I paste the "Order" "Order Id" field
        And I press the "Retrieve Order" button
        Then I should see the message "Success"
        And I should see "34567" in the "Order" "Customer ID" field
        When I press the "Clear Order" button
        And I press the "List Order" button
        Then I should see the message "Success"
        And I should see "34567" in the "Order" results
        And I should not see "23456" in the "Order" results

    Scenario: Retrieve an Order
        When I visit the "Home Page"
        And I set the "Order" "Customer_ID" to "1"
        And I select "Pending" in the "Order" "Status" dropdown
        And I press the "Create Order" button
        When I copy the "Order" "Order Id" field
        And I press the "Clear Order" button
        Then the "Order" "Order Id" field should be empty
        And the "Order" "Customer ID" field should be empty
        And the "Order" "Creation Time" field should be empty
        And the "Order" "Last Updated Time" field should be empty
        And the "Order" "Status" field should be empty
        And the "Order" "Total Price" field should be empty
        When I paste the "Order" "Order Id" field
        And I press the "Retrieve Order" button
        Then I should see the message "Success"
        And I should see "1" in the "Order" "Customer Id" field
        And I should see "Pending" in the "Order" "Status" dropdown
        And I should see "0" in the "Order" "Total Price" field

    Scenario: Create an Item
        When I visit the "Home Page"
        And I set the "Order" "Customer_ID" to "1"
        And I select "Pending" in the "Order" "Status" dropdown
        And I press the "Create Order" button
        Then I should see the message "Success"
        When I copy the "Order" "Order Id" field
        And I paste the "Item" "Order Id" field
        And I set the "Item" "Name" to "food"
        And I set the "Item" "Description" to "This is food"
        And I set the "Item" "Quantity" to "1"
        And I set the "Item" "Price" to "1"
        And I press the "Create Item" button
        Then I should see the message "Success"

    Scenario: List all items
        When I visit the "Home Page"
        And I set the "Order" "Customer_ID" to "1"
        And I select "Pending" in the "Order" "Status" dropdown
        And I press the "Create Order" button
        Then I should see the message "Success"
        When I copy the "Order" "Order Id" field
        And I paste the "Item" "Order Id" field
        And I set the "Item" "Name" to "food"
        And I set the "Item" "Description" to "This is food"
        And I set the "Item" "Quantity" to "1"
        And I set the "Item" "Price" to "1"
        And I press the "Create Item" button
        Then I should see the message "Success"
        When I copy the "Item" "Order Id" field
        And I press the "Clear Item" button
        # Then the "Item" "Order Id" field should be empty
        Then the "Item" "Item ID" field should be empty
        And the "Item" "Name" field should be empty
        And the "Item" "Description" field should be empty
        And the "Item" "Quantity" field should be empty
        And the "Item" "Price" field should be empty
        When I paste the "Order" "Order Id" field
        And I press the "List Items" button
        Then I should see the message "Success"
        And I should see "This is food" in the "Item" results
        And I should see "1" in the "Item" results
        And I should not see "CANCELED" in the "Item" results

    Scenario: Delete an Item
        When I visit the "Home Page"
        And I set the "Order" "Customer_ID" to "1"
        And I select "Pending" in the "Order" "Status" dropdown
        And I press the "Create Order" button
        Then I should see the message "Success"
        When I copy the "Order" "Order Id" field
        And I paste the "Item" "Order Id" field
        And I set the "Item" "Name" to "food"
        And I set the "Item" "Description" to "This is food"
        And I set the "Item" "Quantity" to "1"
        And I set the "Item" "Price" to "1"
        And I press the "Create Item" button
        Then I should see the message "Success"
        When I press the "Clear Order" button
        And I paste the "Order" "Order Id" field
        And I press the "Retrieve Order" button
        Then I should see the message "Success"
        And I should see "1.00" in the "Order" "Total price" field
        When I press the "Delete Item" button
        Then I should see the message "Success"
        When I press the "Retrieve Order" button
        Then I should see the message "Success"
        And I should see "0.00" in the "Order" "Total price" field

    Scenario: Update an Item
        When I visit the "Home Page"
        And I set the "Order" "Customer_ID" to "1"
        And I select "Pending" in the "Order" "Status" dropdown
        And I press the "Create Order" button
        Then I should see the message "Success"
        When I copy the "Order" "Order Id" field
        And I paste the "Item" "Order Id" field
        And I set the "Item" "Name" to "food"
        And I set the "Item" "Description" to "This is food"
        And I set the "Item" "Quantity" to "1"
        And I set the "Item" "Price" to "1"
        And I press the "Create Item" button
        Then I should see the message "Success"
        When I press the "Clear Order" button
        And I paste the "Order" "Order Id" field
        And I press the "Retrieve Order" button
        Then I should see the message "Success"
        And I should see "1.00" in the "Order" "Total price" field
        When I set the "Item" "Quantity" to "2"
        And I press the "Update Item" button
        Then I should see the message "Success"
        When I press the "Clear Order" button
        And I paste the "Order" "Order Id" field
        And I press the "Retrieve Order" button
        Then I should see the message "Success"
        And I should see "2.00" in the "Order" "Total price" field