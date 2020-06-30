$(document).ready(function() {
    $('#example_buy_table').DataTable();
    $('#example_sell_table').DataTable();
    $('#example_transaction_table').DataTable();
    $("#order_form").submit(function(){
        // alert("Hello");
        var stock_code = $(".stock_code").val()
        var quantity = $(".quantity").val()
        var customer = $(".customer_id").val()
        var status = false
        if(stock_code.length!=6)
        {
            $(".stock_code_error").html("Stock Code Value Should be 6 Charecters")
            $(".stock_code").addClass("border_danger")
            status = false
        }
        else
        {
            $(".stock_code_error").html("")
            $(".stock_code").removeClass("border_danger") 
            status = true
            if(quantity<0)
            {
                $(".quantity_error").html("Quantity Value Should be Greater than 0")
                $(".quantity").addClass("border_danger")
                status = false
            }
            else
            {
                $(".quantity_error").html("")
                $(".quantity").removeClass("border_danger") 
                status = true
                if(isNaN(customer))
                {
                    $(".customer_id_error").html("Customer ID should be Integer")
                    $(".customer_id").addClass("border_danger")
                    status = false
                }
                else
                {
                    $(".customer_id_error").html("")
                    $(".scustomer_id").removeClass("border_danger") 
                    status = true
                }  
            }
        }
        


        if(status == true)
        {
            $.ajax({
                url:"http://localhost:5000/",
                method:"POST",
                data:$("#order_form").serialize(),
                success:function(data){
                    window.location.href="http://localhost:5000/"
                }
            })
        }
        
    })
    $("#transaction_form").submit(function(){
        // alert("Hello");
        var stock_code = $(".stock_code").val()
        var quantity = $(".quantity").val()
        var customer = $(".customer_id").val()
        var status = false
        if(stock_code.length!=6)
        {
            $(".stock_code_error").html("Stock Code Value Should be 6 Charecters")
            $(".stock_code").addClass("border_danger")
            status = false
        }
        else
        {
            $(".stock_code_error").html("")
            $(".stock_code").removeClass("border_danger") 
            status = true
            if(quantity<0)
            {
                $(".quantity_error").html("Quantity Value Should be Greater than 0")
                $(".quantity").addClass("border_danger")
                status = false
            }
            else
            {
                $(".quantity_error").html("")
                $(".quantity").removeClass("border_danger") 
                status = true
                if(isNaN(customer))
                {
                    $(".customer_id_error").html("Customer ID should be Integer")
                    $(".customer_id").addClass("border_danger")
                    status = false
                }
                else
                {
                    $(".customer_id_error").html("")
                    $(".scustomer_id").removeClass("border_danger") 
                    status = true
                }  
            }
        }
        


        if(status == true)
        {
            $.ajax({
                url:"http://localhost:5000/",
                method:"POST",
                data:$("#transaction_form").serialize(),
                success:function(data){
                    window.location.href="http://localhost:5000/"
                }
            })
        }
        
    })
} );