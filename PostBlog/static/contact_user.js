$(document).ready(function(){
   $("#contactForm").submit(function(e){
      	e.preventDefault();
      	var serializedData = $(this).serialize();
      	var MY_URL =  $(this).attr('action');
      	$.ajax({
      		type : 'POST',
      		url : MY_URL,
      		data : serializedData,
      		success : function(data){
      			$("#contactForm")[0].reset();
      			if (data) {
                              alert('Successfully Submitted');
                              console.log(data.status)
                              appendTocontacttable(data.data)
                           }
      		},
      		error : function(response){
      			console.log(response)
      		}
      	});
   });
});
  function appendTocontacttable(contact) {
             $("#contacttable > tbody:last-child").append(`
                    <tr id="contact-${contact.id}">
                        <td class="ContactName" name="name">${contact.name}</td>
                        <td class="ContactEmail" name="email">${contact.email}</td>
                        <td class="ContactMessage" name="message">${contact.message}</td>
                    </tr>
                `);
            }