$('#id_ajax_upload_form').submit(function(e){
        e.preventDefault();
        var token = '{{csrf_token}}';
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();

        var MY_URL =  $(this).attr('action');
        var method =  $(this).attr('method');
        var formData = new FormData(this);
         $(document).ready(function(){
        $.ajax({
            headers: { "X-CSRFToken": csrftoken },
            url: MY_URL,
            type: method,
            data: formData,
           success: function (response) {
                $('.error').remove();
                console.log(response)
                if(response.error){
                  alert(response.error)
                }
                else{
                    alert(response.message)
                    window.location = ""
                }
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });
    });