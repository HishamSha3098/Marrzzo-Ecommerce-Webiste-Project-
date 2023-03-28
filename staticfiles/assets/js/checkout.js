
	$(document).ready(function () {

		$('#paywithrazorpay').click(function (){
		
			var orderid = $('.order-number').attr('orderid');
		console.log(orderid);
			$.ajax({
				url: '/order/proceed-to-pay/',
				data :{ 'orderid': orderid},
				dataType: 'json',
				
				success: function(data) {
				console.log(data);
				var fname = data.values.fname;
				var email = data.values.email;
				var address =data.values.address;
				var city =data.values.city;
				var state = data.values.state;
				var country = data.values.country;
				var pincode = data.values.pin_code;
				var phone = data.values.phone;
				var amount = data.values.amount;
				var ordernumber = data.values.order_id;
				var token = $("[name='csrfmiddlewaretoken']").val();
		
				  // etc.
				  // Your code to process the retrieved values
			console.log(fname)
			if (fname=="" || email == "" || address == "" || city == ""||state=="" || country =="" || pincode =="" || phone == "" || amount == "" || ordernumber == "" ) {
				console.log("im in if")
				 swal.fire("alert!","All fields are mandatory","error")
				return false;
			}
			else{
				console.log("im in else")
			 	var options = {
					"key": "rzp_test_wDSZWwmcRov4vw", // Enter the Key ID generated from the Dashboard
					"amount": amount*100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
					"currency": "INR",
					"name": "Marrazzo", //your business name
					"description": "Thank you for purchasing with us",
					"image": "static/assets/images/singlelogo.png",
					// "order_id": ordernumber, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
					"handler": function (response){
						// swal.fire("Your Payment id is",response.razorpay_payment_id,"success");
						// alert(response.razorpay_order_id);
						// alert(response.razorpay_signature)
						data ={
							
						"payment_mode": "Paid by Razorpay",
						"payment_id" :response.razorpay_payment_id,
						"order_id" : ordernumber,
						"amount" : amount,
						csrfmiddlewaretoken: token
		
						}
						console.log("im before ajax")
						$.ajax({
							method : "POST",
							url :"/order/place-order/",
							data : data,
							success : function(responseb){
						console.log("im inside ajax")

							swal.fire("Congratulations",responseb.status,"success").then((value)=> {
		
								window.location.href="/order/invoice/" + ordernumber + "/";
		
													  
														
								 }
											   
								);
							
		
								
							}
		
		
						});
		
						console.log("im after ajax")
		
					},
					
					"prefill": {
						"name": fname, //your customer's name
						"email": email,
						"contact": phone
					},
					// "notes": {
					//     "address": "Razorpay Corporate Office"
					// },
					"theme": {
						"color": "#3399cc"
					}
				};
				var rzp1 = new Razorpay(options);
				
				rzp1.open();
				}}
				
				})
		
			
		
				
		
			   
			
		
			
		
		
			})
			
		});
		
		
		
