            $(document).ready(function() {
                $("form#addUser").on('submit', function() {
                    var nameInput = $('input[name="name"]').val();
                    var addressInput = $('input[name="address"]').val();
                    var ageInput = $('input[name="age"]').val();
                    var formdata = $(this).serialize()
                    if (nameInput && addressInput && ageInput) {
                        // Create Ajax Call
                        $.ajax({
                            url: 'create/',
                            data: formdata,
                            dataType: 'json',
                            success: function(data) {
                                if (data.user) {
                                    alert('Successfully Submitted');
                                    appendToUsrTable(data.user);
                                }
                            }
                        });
                    } else {
                        alert("All fields must have a valid value.");
                    }
                });
            });

            function appendToUsrTable(user) {
                $("#userTable > tbody:last-child").append(`
                    <tr id="user-${user.id}">
                        <td class="userName" name="name">${user.name}</td>
                        <td class="userAddress" name="address">${user.address}</td>
                        <td class="userAge" name="age">${user.age}</td>
                        <td align="center">
                            <button class="btn btn-success form-control" onClick="editUser(${user.id})" data-toggle="modal" data-target="#myModal")">EDIT</button>
                        </td>

                        <td align="center">
                            <button class="btn btn-danger form-control" onClick="deleteUser(${user.id})">DELETE</button>
                        </td>
                    </tr>
                `);
            }
            $("form#updateUser").submit(function() {
                var idInput = $('input[name="formId"]').val();
                var nameInput = $('input[name="formName"]').val();
                var addressInput = $('input[name="formAddress"]').val();
                var ageInput = $('input[name="formAge"]').val();

                if (nameInput && addressInput && ageInput) {
                    $.ajax({
                        url: 'update/',
                        data: {
                            'id': idInput,
                            'name': nameInput,
                            'address': addressInput,
                            'age': ageInput
                        },
                        dataType: 'json',
                        success: function(data) {
                            if (data.user) {
                                updateToUserTabel(data.user);
                            }
                        }
                    });
                } else {
                    alert("All fields must have a valid value.");
                }
//                $('form#updateUser').trigger("reset");
                $('#myModal').modal('hide');
                return false;
            });

            function editUser(id) {
                if (id) {
                    tr_id = "#user-" + id;
                    name = $(tr_id).find(".userName").text();
                    address = $(tr_id).find(".userAddress").text();
                    age = $(tr_id).find(".userAge").text();
                    $('#form-id').val(id);
                    $('#form-name').val(name);
                    $('#form-address').val(address);
                    $('#form-age').val(age);
                }
            }

            function updateToUserTabel(user) {
                $("#userTable #user-" + user.id).children(".userData").each(function() {

                    var attr = $(this).attr("name");
                    if (attr == "name") {
                        $(this).text(user.name);
                    } else if (attr == "address") {
                        $(this).text(user.address);
                    } else {
                        $(this).text(user.age);
                    }
                });
            }

            function deleteUser(id) {
                var action = confirm("Are you sure you want to delete this user?");
                if (action != false) {
                    $.ajax({
                        url: 'delete/',
                        data: {
                            'id': id,
                        },
                        dataType: 'json',
                        success: function(data) {
                            if (data.deleted) {
                                $("#userTable #user-" + id).remove();
                            }
                        }
                    });
                }
            }