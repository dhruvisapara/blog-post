$(document).ready(function(){
   $("#contactForm").submit(function(e){
      	e.preventDefault();
      	var serializedData = $(this).serialize();
      	$.ajax({
      		type : 'POST',
      		url :  "{% url 'contact_submit' %}",
      		data : serializedData,
      		success : function(response){
      			$("#contactForm")[0].reset();
      		},
      		error : function(response){
      			console.log(response)
      		}
      	});
   });
});
