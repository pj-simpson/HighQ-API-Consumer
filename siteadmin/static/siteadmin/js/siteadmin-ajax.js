$("#hqSiteSearchForm").submit(function(event) {
    event.preventDefault();
    var siteSearchInput = $('input[name="sitename"]').val().trim();
    if (siteSearchInput) {
        // Create Ajax Call
        $.ajax( {type:"GET",
            url: decodeURI('ajax/site/'),
            data: {
                'sitename': siteSearchInput,
            },
            dataType: 'json',
            success: function (search_result) {
            if (search_result.empty_check == true) {
                $("#hqSiteSearchForm").trigger("reset");
                $("#siteResultTile").empty();
                alert(search_result.message);
            }
            else {
                appendTositeresultTile(search_result);

            }
             }
        });
      } else {
        alert("email value must have a valid value.");
    }
    $("#hqSiteSearchForm").trigger("reset");
});



function appendTositeresultTile(search_result) {
    $("#siteResultTile").empty();
    $.each(search_result.site, function(key, value) {
                 $("#siteResultTile").append(`
                <div class="tile is-ancestor has-text-centered is-6">  
                    <div class="tile is-parent">
                        <article class="tile is-child box">
                            <p class="title">${value.sitename} </p>
                            <p class="subtitle"><button class="button is-small is-link is-light" id="showModal" data-modalid="${value.id}">Details</button></p>                                
                        </article>   
                    </div>
                </div>
                
                <div id="modal-site${value.id}" class="modal">
                  <div class="modal-background"></div>
                  <div class="modal-card">
                    <header class="modal-card-head">
                      <p class="modal-card-title">${value.sitename}</p>
                      <button id="closeModal" class="modal-close is-large" aria-label="close" data-modalid="${value.id}"></button>
                    </header>
                    <section class="modal-card-body">
                      <ul>
                      <li>Created on: ${value.createddate} by <a href="mailto:${value.siteowner.email}">${value.siteowner.firstname} ${value.siteowner.lastname}</a></li>
                      <li>Current Status: ${value.status}</li>
                      <li>Current Size: ${value.size} of which ${value.percentage_deleted} % is deleted files</li>
                      
                      </ul>
                    </section>
                    <footer class="modal-card-foot">
                    <form id="hqSiteMessage${value.id}" action="">
                            <div class="field">
                                <p class="control">
                                    <input class="input" type="text" name="email_message" maxlength="200" required="" id="emailMessage_${value.id}"/>
                                </p>
                            </div>
                        <input class="input" type="hidden" name="user_id" maxlength="200" required=""  value="${value.siteowner.userid}"/>
                        <input class="input" type="hidden" name="site_id" maxlength="200" required=""  value="${value.id}"/>
                        <div class="field">
                                <p class="control">
                                    <button class="button is-primary" onClick="sendMessage(document.getElementById('emailMessage_${value.id}').value,${value.siteowner.userid},${value.id})">Email Site Owner</button>
                                </p>
                            </div>
                    </form>



                        
                    </footer>
                  </div>
                </div>`);
    });
};

//show Modal

$("#siteResultTile").on("click","#showModal",function(event){
        var modalId = event.originalEvent.toElement.dataset.modalid;
        $("#modal-site" + modalId).addClass("is-active");

});

//hide Modal

$("#siteResultTile").on("click","#closeModal",function(event){
        var modalId = event.originalEvent.toElement.dataset.modalid;
        $("#modal-site" + modalId).removeClass("is-active");

});



function sendMessage(emailMessage,userId,siteId) {
     $("#hqSiteMessage"+siteId).trigger("reset")

        $.ajax({
                type: "GET",
                url: decodeURI('ajax/message/'),
                data: {
                    'email_message': emailMessage,
                    'user_id': userId,
                    'site_id': siteId,
                },
                dataType: 'json',
                success: function (message_result) {
                    if (message_result.apistatuscode) {
                        alert(message_result.apistatuscode +':' + message_result.message);
                    }
                    else {
                         alert(message_result.message);
                    }
                    $('#hqSiteMessage').trigger("reset");
                    $(".modal.is-active").removeClass("is-active");

                }

            }
        )

}














