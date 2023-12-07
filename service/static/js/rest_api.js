$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the Order form with data from the response
    function update_order_form_data(res) {
        $("#order_order_id").val(res.id);
        $("#order_customer_id").val(res.customer_id);
        $("#order_creation_time").val(res.creation_time);
        $("#order_last_updated_time").val(res.last_updated_time);
        $("#order_status").val(res.status.toUpperCase());
        $("#order_total_price").val(res.total_price);
    }

    // Clears all Order form fields
    function clear_order_form_data() {
        $("#order_order_id").val("");
        $("#order_customer_id").val("");
        $("#order_creation_time").val("");
        $("#order_last_updated_time").val("");
        $("#order_status").val("");
        $("#order_total_price").val("");
    }

    // Updates the Item form with data from the response
    function update_item_form_data(res) {
        $("#item_item_id").val(res.id);
        $("#item_order_id").val(res.order_id);
        $("#item_name").val(res.name);
        $("#item_description").val(res.description);
        $("#item_quantity").val(res.quantity);
        $("#item_price").val(res.price);
    }

    // Clears all Item form fields
    function clear_item_form_data() {
        $("#item_item_id").val("");
        $("#item_order_id").val("");
        $("#item_name").val("");
        $("#item_description").val("");
        $("#item_quantity").val("");
        $("#item_price").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Order
    // ****************************************

    $("#create-order-btn").click(function () {

        let customer_id = $("#order_customer_id").val();
        let status = $("#order_status").val();
        

        let data = {
            "customer_id": customer_id,
            "status": status,
            "items": [],
            "total_price": 0
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/api/orders",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_order_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update an Order
    // ****************************************

    $("#update-order-btn").click(function () {

        let order_id = $("#order_order_id").val();
        let customer_id = $("#order_customer_id").val();
        let status = $("#order_status").val();
        let total_price = $("#order_total_price").val();

        let data = {
            "customer_id": customer_id,
            "status": status,
            "total_price": total_price
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/api/orders/${order_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_order_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an Order
    // ****************************************

    $("#retrieve-order-btn").click(function () {

        let order_id = $("#order_order_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/orders/${order_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_order_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_order_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Cancel an Order
    // ****************************************

    $("#cancel-order-btn").click(function () {

        let order_id = $("#order_order_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/api/orders/${order_id}/cancel`,
            contentType: "application/json"
        });

        ajax.done(function(res){
            update_order_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Delete an Order
    // ****************************************

    $("#delete-order-btn").click(function () {

        let order_id = $("#order_order_id").val();

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "DELETE",
            url: `/api/orders/${order_id}`,
            contentType: "application/json"
        });

        ajax.done(function(res){
            clear_order_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Repeat an Order
    // ****************************************

    $("#repeat-order-btn").click(function () {

        let order_id = $("#order_order_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: `/api/orders/${order_id}/repeat`,
            contentType: "application/json"
        });

        ajax.done(function(res){
            update_order_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-order-btn").click(function () {
        $("#flash_message").empty();
        clear_order_form_data()
    });

    $("#clear-item-btn").click(function () {
        $("#flash_message").empty();
        clear_item_form_data()
    });

    // ****************************************
    // List Orders
    // ****************************************

    $("#list-order-btn").click(function () {

        let customer_id = $("#order_customer_id").val();
        let creation_time = $("#order_creation_time").val();
        let status = $("#order_status").val();

        let queryString = ""

        if (customer_id) {
            queryString += 'customer_id=' + customer_id
        }
        if (creation_time) {
            if (queryString.length > 0) {
                queryString += '&date=' + creation_time
            } else {
                queryString += 'date=' + creation_time
            }
        }
        if (status) {
            if (queryString.length > 0) {
                queryString += '&status=' + status
            } else {
                queryString += 'status=' + status
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/orders?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#order_search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-4">CUSTOMER ID</th>'
            table += '<th class="col-md-4">CREATION TIME</th>'
            table += '<th class="col-md-3">LAST UPDATED TIME</th>'
            table += '<th class="col-md-3">STATUS</th>'
            table += '<th class="col-md-3">TOTAL PRICE</th>'
            table += '</tr></thead><tbody>'
            let firstOrder = "";
            for(let i = 0; i < res.length; i++) {
                let order = res[i];
                table +=  `<tr id="row_${i}"><td>${order.id}</td><td>${order.customer_id}</td><td>${order.creation_time}</td><td>${order.last_updated_time}</td><td>${order.status}</td><td>${order.total_price}</td></tr>`;
                if (i == 0) {
                    firstOrder = order;
                }
            }
            table += '</tbody></table>';
            $("#order_search_results").append(table);

            // copy the first result to the form
            if (firstOrder != "") {
                update_order_form_data(firstOrder)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Create an Item
    // ****************************************

    $("#create-item-btn").click(function () {

        let order_id = $("#item_order_id").val();
        let name = $("#item_name").val();
        let description = $("#item_description").val();
        let quantity = $("#item_quantity").val();
        let price = $("#item_price").val();
        

        let data = {
            "order_id": order_id,
            "name": name,
            "description": description,
            "quantity": quantity,
            "price": price
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: `/api/orders/${order_id}/items`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_item_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

      // ****************************************
    // List Items
    // ****************************************

    $("#list-item-btn").click(function () {

        let order_id = $("#item_order_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/orders/${order_id}/items`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#item_search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-4">ITEM ID</th>'
            table += '<th class="col-md-3">NAME</th>'
            table += '<th class="col-md-3">DESCRIPTION</th>'
            table += '<th class="col-md-3">QUANTITY</th>'
            table += '<th class="col-md-3">PRICE</th>'
            table += '</tr></thead><tbody>'
            let firstItem = "";
            for(let i = 0; i < res.length; i++) {
                let item = res[i];
                table +=  `<tr id="row_${i}"><td>${item.id}</td><td>${item.name}</td><td>${item.description}</td><td>${item.quantity}</td><td>${item.price}</td></tr>`;
                if (i == 0) {
                    firstItem = item;
                }
            }
            table += '</tbody></table>';
            $("#item_search_results").append(table);

            // copy the first result to the form
            if (firstItem != "") {
                update_item_form_data(firstItem)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    

    });

    // ****************************************
    // Delete an Item
    // ****************************************

    $("#delete-item-btn").click(function () {

        let item_id = $("#item_item_id").val();
        let order_id = $("#item_order_id").val();

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "DELETE",
            url: `/api/orders/${order_id}/items/${item_id}`,
            contentType: "application/json"
        });

        ajax.done(function(res){
            clear_item_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Update an Item
    // ****************************************

    $("#update-item-btn").click(function () {
        
        let item_id = $("#item_item_id").val();
        let order_id = $("#item_order_id").val();
        let name = $("#item_name").val();
        let description = $("#item_description").val();
        let quantity = $("#item_quantity").val();
        let price = $("#item_price").val();

        let data = {
            "order_id": order_id,
            "name": name,
            "description": description,
            "quantity": quantity,
            "price": price
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/api/orders/${order_id}/items/${item_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_item_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    // Retrieve an Item
    // ****************************************

    $("#retrieve-item-btn").click(function () {

        let item_id = $("#item_item_id").val();
        let order_id = $("#item_order_id").val();

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "GET",
            url: `/api/orders/${order_id}/items/${item_id}`,
            contentType: "application/json"
        });

        ajax.done(function(res){
            update_item_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

})
