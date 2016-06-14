$(document).ready(function() {

    // process the form
    $('form').submit(function(event) {

        $('.form-group').removeClass('has-warning'); // remove the error class
        $('.alert').remove(); // remove the error text

        // get the form data
        // there are many ways to get this data using jQuery (you can use the class or id also)
        var formData = $( "form" ).serialize();

        // process the form
        $.ajax({
            type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
            url         : '/form', // the url where we want to POST
            data        : formData, // our data object
            dataType    : 'json', // what type of data do we expect back from the server
            encode      : true
        })
            // using the done promise callback
            .done(function(data) {
                // log data to the console so we can see
                console.log(data);

                // ALL GOOD! just show the success message!
                $('form').append('<div class="alert alert-success">' + data.message + '</div>');
            })

            // using the fail promise callback
            .fail(function(xhr) {
                // get the json encoded response
                data = xhr.responseJSON

                // log data to the console so we can see
                console.log(data);

                // show any errors
                $.each(data.errors, function(field, message){
                    $('#'+field+'-group').addClass('has-warning'); // add the error class to show red input
                    $('#'+field+'-group div').append('<div class="alert alert-warning" role="alert">' + message + '</div>'); // add the actual error message under our input
                })
            });

        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
    });

});