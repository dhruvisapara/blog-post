        $("form#updateBlog").submit(function() {
        var IdInput = $('input[name="formId"]').val();
        var TitleInput = $('input[name="formTitle"]').val();
        var DescriptionInput = $('input[name="formDescription"]').val();
        var HighlightsInput = $('input[name="formHighlights"]').val();
        var Pub_dateInput = $('input[name="formPub_date"]').val();
        var MY_URL =  $(this).attr('action');
        if (TitleInput && DescriptionInput && HighlightsInput && Pub_dateInput) {
            $.ajax({
                url: MY_URL,
                data: {
                    'id': IdInput,
                    'title': TitleInput,
                    'description': DescriptionInput,
                    'highlights': HighlightsInput,
                    'pub_date':Pub_dateInput
                },
                dataType: 'json',
                success: function (data) {
                    if (data) {
                      updateToBlogTabel(data);
                    }
                }
            });
           } else {
            alert("All fields must have a valid value.");
        }

        $('form#updateBlog').trigger("reset");
        $('#myModal').modal('hide');
        return false;
            });
        function editBlog(id) {
          if (id) {
            tr_id = "#blog-" + id;
            title = $(tr_id).find(".blogTitle").text();
            description = $(tr_id).find(".blogDescription").text();
            highlight = $(tr_id).find(".blogHighlights").text();
            pub_date = $(tr_id).find(".blogPub_date").text();
            $('#form-id').val(id);
            $('#form-title').val(title);
            $('#form-description').val(description);
            $('#form-highlights').val(highlight);
            $('#form-pub_date').data(pub_date);
          }
        }
        function updateToBlogTabel(blog){
            $("#container2 #blog-" + blog.id).children(".blogData").each(function() {
                var attr = $(this).attr("name");
                if (attr == "title") {
                  $(this).text(blog.title);
                } else if (attr == "description") {
                  $(this).text(blog.description);
                }else if (attr == "pub_date") {
                  $(this).text(blog.pub_date);
                }
                 else {
                  $(this).text(blog.highlights);
                }
              });
        }
         function deleteBlog(id) {
          var action = confirm("Are you sure you want to delete this user?");
          var MY_URL = $('#delete_url').text();
          if (action != false) {
            $.ajax({
                url:MY_URL,
                data: {
                    'id': id,
                },
                dataType: 'json',
                success: function (data) {
                    if (data.deleted) {
                      $("#container2 #blog-" + id).remove();
                      alert("Successfully deleted.")
                    }
                }
            });
          }
        }