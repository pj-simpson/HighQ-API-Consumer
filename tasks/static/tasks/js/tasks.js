$("#id_site").change(function(event) {
    var siteId = $(this).children("option:selected").val();
    if (siteId) {
        // Create Ajax Call
        $.ajax( {type:"GET",
            url: decodeURI('ajax/task_list/'),
            data: {
                'siteid': siteId,
            },
            dataType: 'json',
            success: function (result) {

                console.log(result)
                $('#id_task_list').empty();

                $.each(result.list,function(key, value) {
                    $("#id_task_list").append(`<option value="${value.listid}">${value.listname}</option>`);

                });


            }
        });
      } else {
        alert("Error With Tasks JQuery");
    }
});