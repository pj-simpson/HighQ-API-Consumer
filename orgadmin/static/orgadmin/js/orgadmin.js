$("#hqOrgSearchForm").submit(function(event) {
    event.preventDefault();
    $('#orgResultTile').empty;
    var orgSearchInput = $('input[name="orgname"]').val().trim();
    var orgDomainInput = $('input[name="domainname"]').val().trim();
    var orgstatusInput = $('select[name="status"]').children("option:selected"). val();
    console.log(orgstatusInput);

    if (orgSearchInput &&! orgDomainInput) {
        // Create Ajax Call
        $.ajax( {type:"GET",
            url: decodeURI('ajax/org/'),
            data: {
                'orgname': orgSearchInput,
                'status': orgstatusInput,
            },
            dataType: 'json',

            success: function (search_result) {
                console.log(search_result)
                if (search_result.empty_check == true){
                    $('#hqOrgSearchForm').trigger("reset");
                    $("#orgResultTile").empty()

                    alert(search_result.message);
                }
                else {
                    appendToorgresultTile(search_result);
                }

             }
        });
      } else if (orgDomainInput &&! orgSearchInput){
        // Create Ajax Call
        $.ajax( {type:"GET",
            url: decodeURI('ajax/org/'),
            data: {
                'domainname': orgDomainInput,
                'status': orgstatusInput,
            },
            dataType: 'json',

            success: function (search_result) {
                console.log(search_result)
                if (search_result.empty_check == true){
                    $('#hqOrgSearchForm').trigger("reset");
                    $("#orgResultTile").empty()

                    alert(search_result.message);
                }
                else {
                    appendToorgresultTile(search_result);
                }

             }
        });
      } else if (orgSearchInput && orgDomainInput ){
        // Create Ajax Call
        $.ajax( {type:"GET",
            url: decodeURI('ajax/org/'),
            data: {
                'orgname': orgSearchInput || null,
                'domainname': orgDomainInput || null,
                'status': orgstatusInput,
            },
            dataType: 'json',

            success: function (search_result) {
                console.log(search_result)
                if (search_result.empty_check == true){
                    $('#hqOrgSearchForm').trigger("reset");
                    $("#orgResultTile").empty()

                    alert(search_result.message);
                }
                else {
                    appendToorgresultTile(search_result);
                }

             }
        });
      } else {
        alert("fall through");
    }
    $('#hqOrgSearchForm').trigger("reset");
});


function appendToorgresultTile(search_result) {
    $('#hqOrgSearchForm').trigger("reset");
    $("#orgResultTile").empty()

    $.each(search_result.organisation, function(key, value) {
                 $("#orgResultTile").append(`
                <div class="tile is-ancestor has-text-centered is-8">  
                    <div class="tile is-parent">
                        <article class="tile is-child box">
                            <p class="title">${value.name} </p>
                            <p>Creation Date: ${value.createddate}</p>
                            <p>Number of users: ${value.noofusers}</p>
                        </article>   
                    </div>
                </div>`);
    })
};

$("#hqOrgSubmitForm").submit(function(event) {
    event.preventDefault();
    var orgSearchInput = $('input[name="orgname"]').val().trim();
    var orgURLInput = $('input[name="url"]').val().trim();
    var orgstatusInput = $('select[name="status"]').children("option:selected"). val();
    var orgDomainInput = $('input[name="orgdomain"]').val().trim();
    console.log(orgDomainInput);

    if (orgSearchInput) {
        // Create Ajax Call
        $.ajax( {type:"GET",
            url: decodeURI('ajax/org/'),
            data: {
                'orgname': orgSearchInput,
                'orgurl': orgURLInput,
                'status': orgstatusInput,
                'orgdomain':orgDomainInput,
            },
            dataType: 'json',

            success: function (search_result) {
                $('#hqOrgSearchForm').trigger("reset");
                console.log(search_result)
                if (search_result.success == true) {
                    alert(search_result.message + search_result.name);
                } else {
                    appendToresultTile(search_result);
                }
            }
        });
      } else {
        alert("blah blah blah");
    }
    $('#hqOrgSearchForm').trigger("reset");
});