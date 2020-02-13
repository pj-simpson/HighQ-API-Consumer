$("#hqUserSearchForm").submit(function(event) {
    event.preventDefault();
    $("#resultheader").empty()
    $("#sitenameLoop").empty()
    console.log("form submitted!")
    var emailInput = $('input[name="email"]').val().trim();
    if (emailInput) {
        // Create Ajax Call
        $.ajax( {type:"GET",
            url: decodeURI('ajax/user/'),
            data: {
                'email': emailInput,
            },
            dataType: 'json',
            success: function (search_result) {
                if (search_result.success == true) {
                    appendTop(search_result)
                }
                else {
                    alert(search_result.summary)
                }



            }
        });
      } else {
        alert("email value must have a valid value.");
    }
    $('#hqUserSearchForm').trigger("reset");
});

function appendTop(search_result) {
    $('#hqUserSearchForm').trigger("reset")
    $("#resultheader").append(`<div class="card events-card">
                    <header class="card-header">
                        <h3 class="card-header-title" id="resultheader_h">
                            <strong>${search_result.firstname} ${search_result.lastname}</strong> | Added to the instance: ${search_result.createddate} | Last Login: ${search_result.lastlogindate}
                        </h3>
                    </header>
                    <div class="card-content">
                        <table class="table is-bordered" id="sitenameLoop">
                        </table>
                    </div>
                <footer class="card-footer"/>
                </div>
    `);
    $.each(search_result.sites.site, function(key, value) {
    $("#sitenameLoop").append(`  
        <tr id="site-${value.id}">
         <td id="site-${value.id}">${value.sitename}</td>
         <td id="site-${value.id}" align="center">
            <button class="button is-small is-danger is-outlined" id="remove_from_site" onClick="removeUser(${search_result.userid},${value.id})">
                <span>Remove</span>
                <span class="icon is-small">
                    <i class="fas fa-times"></i>
                </span>
            </button>
          </td>
         <td id="site-${value.id}" align="center">
            <button class="button is-small is-primary is-outlined" id="reset_password" onClick="resetUserPassword(${search_result.userid},${value.id})">
                <span>Re-Invite To Site</span>
                <span class="icon is-small">
                    <i class="fa fa-address-card"></i>
                </span>
            </button>
           </td>      
        </tr>     

    `);
});

};

function removeUser(user_id, site_id) {
    var action = confirm("Are you sure you want to remove this user from the site?");

    if (action != false){
        $.ajax({
            type:'GET',
            url: decodeURI('ajax/remove/'),
            data:{
                'user_id':user_id,
                'site_id':site_id
            },
            dataType:'json',
            success: function(result) {
                if (result.apistatuscode !== "200")  {
                    alert(result.apistatuscode +':' + result.message);

                }
                else {
                    $("#site-"+site_id).remove();

                }


            }
        });
    }
};

function resetUserPassword(user_id, site_id) {
        $.ajax({
            type:'GET',
            url: decodeURI('ajax/reset/'),
            data:{
                'user_id':user_id,
                'site_id':site_id
            },
            dataType:'json',
            success: function(result) {
                alert(result.apistatuscode +':' + result.message);
            }
        });
};







