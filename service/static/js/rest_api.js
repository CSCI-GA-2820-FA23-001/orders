$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_order_form_data(res) {
        $("#order_order_id").val(res.id);
        $("#order_customer_id").val(res.customer_id);
        $("#order_creation_time").val(res.creation_time);
        $("#order_last_updated_time").val(res.last_updated_time);
        $("#order_status").val(res.status.toUpperCase());
        $("#order_total_price").val(res.total_price);
    }

    /// Clears all form fields
    function clear_order_form_data() {
        $("#order_id").val("");
        $("#order_customer_id").val("");
        $("#order_creation_time").val("");
        $("#order_last_updated_time").val("");
        $("#order_status").val("");
        $("#order_total_price").val("");
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
            url: "/orders",
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


//     // ****************************************
//     // Update a Pet
//     // ****************************************

//     $("#update-btn").click(function () {

//         let pet_id = $("#pet_id").val();
//         let name = $("#pet_name").val();
//         let category = $("#pet_category").val();
//         let available = $("#pet_available").val() == "true";
//         let gender = $("#pet_gender").val();
//         let birthday = $("#pet_birthday").val();

//         let data = {
//             "name": name,
//             "category": category,
//             "available": available,
//             "gender": gender,
//             "birthday": birthday
//         };

//         $("#flash_message").empty();

//         let ajax = $.ajax({
//                 type: "PUT",
//                 url: `/pets/${pet_id}`,
//                 contentType: "application/json",
//                 data: JSON.stringify(data)
//             })

//         ajax.done(function(res){
//             update_form_data(res)
//             flash_message("Success")
//         });

//         ajax.fail(function(res){
//             flash_message(res.responseJSON.message)
//         });

//     });

//     // ****************************************
//     // Retrieve a Pet
//     // ****************************************

//     $("#retrieve-btn").click(function () {

//         let pet_id = $("#pet_id").val();

//         $("#flash_message").empty();

//         let ajax = $.ajax({
//             type: "GET",
//             url: `/pets/${pet_id}`,
//             contentType: "application/json",
//             data: ''
//         })

//         ajax.done(function(res){
//             //alert(res.toSource())
//             update_form_data(res)
//             flash_message("Success")
//         });

//         ajax.fail(function(res){
//             clear_form_data()
//             flash_message(res.responseJSON.message)
//         });

//     });

    // ****************************************
    // Cancel an Order
    // ****************************************

    $("#cancel-order-btn").click(function () {

        let order_id = $("#order_order_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: "/orders/" + order_id + "/cancel",
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

//     // ****************************************
//     // Delete a Pet
//     // ****************************************

//     $("#delete-btn").click(function () {

//         let pet_id = $("#pet_id").val();

//         $("#flash_message").empty();

//         let ajax = $.ajax({
//             type: "DELETE",
//             url: `/pets/${pet_id}`,
//             contentType: "application/json",
//             data: '',
//         })

//         ajax.done(function(res){
//             clear_form_data()
//             flash_message("Pet has been Deleted!")
//         });

//         ajax.fail(function(res){
//             flash_message("Server error!")
//         });
//     });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-order-btn").click(function () {
        $("#order_id").val("");
        $("#flash_message").empty();
        clear_order_form_data()
    });

//     // ****************************************
//     // Search for a Pet
//     // ****************************************

//     $("#search-btn").click(function () {

//         let name = $("#pet_name").val();
//         let category = $("#pet_category").val();
//         let available = $("#pet_available").val() == "true";

//         let queryString = ""

//         if (name) {
//             queryString += 'name=' + name
//         }
//         if (category) {
//             if (queryString.length > 0) {
//                 queryString += '&category=' + category
//             } else {
//                 queryString += 'category=' + category
//             }
//         }
//         if (available) {
//             if (queryString.length > 0) {
//                 queryString += '&available=' + available
//             } else {
//                 queryString += 'available=' + available
//             }
//         }

//         $("#flash_message").empty();

//         let ajax = $.ajax({
//             type: "GET",
//             url: `/pets?${queryString}`,
//             contentType: "application/json",
//             data: ''
//         })

//         ajax.done(function(res){
//             //alert(res.toSource())
//             $("#search_results").empty();
//             let table = '<table class="table table-striped" cellpadding="10">'
//             table += '<thead><tr>'
//             table += '<th class="col-md-2">ID</th>'
//             table += '<th class="col-md-2">Name</th>'
//             table += '<th class="col-md-2">Category</th>'
//             table += '<th class="col-md-2">Available</th>'
//             table += '<th class="col-md-2">Gender</th>'
//             table += '<th class="col-md-2">Birthday</th>'
//             table += '</tr></thead><tbody>'
//             let firstPet = "";
//             for(let i = 0; i < res.length; i++) {
//                 let pet = res[i];
//                 table +=  `<tr id="row_${i}"><td>${pet.id}</td><td>${pet.name}</td><td>${pet.category}</td><td>${pet.available}</td><td>${pet.gender}</td><td>${pet.birthday}</td></tr>`;
//                 if (i == 0) {
//                     firstPet = pet;
//                 }
//             }
//             table += '</tbody></table>';
//             $("#search_results").append(table);

//             // copy the first result to the form
//             if (firstPet != "") {
//                 update_form_data(firstPet)
//             }

//             flash_message("Success")
//         });

//         ajax.fail(function(res){
//             flash_message(res.responseJSON.message)
//         });

//     });

})
