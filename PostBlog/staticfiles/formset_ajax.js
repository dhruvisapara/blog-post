 $(document).ready(function() {
     var csrftoken = $("[name=csrfmiddlewaretoken]").val();
     let data = $('form#mainform').serialize();
     var url = $(this).attr('action');

     $.ajax({
         url: url,
         type: "POST",
         data: data,
         headers: {
             "X-CSRFToken": csrftoken
         },
         success: function(response) {
             console.log("88888")
         },
         error: function(response) {
             console.log(response)
         }
     });

 });