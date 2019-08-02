//*****************************************************************************
    //Fill select with states/provinces
    $(document).ready(function () {
        get_steps_by_stage();
        let stage_number = $('#community-stage').val();
        $('#community-step').attr("max", String(steps_by_stage[stage_number]));
        if ($.isEmptyObject(community)) {
            $.when(
              getProvinces()
            ).then(
              console.log("Community data: blank; provinces obtained from Database.")
            );
        } else {
            $('#state-select').append(new Option(community.state));
            $('#city-select').append(new Option(community.city));
            $('#community-select').append(new Option(community.town));
            console.log("Select dropdowns filled by community address");
        }
        $('#community-name').val("");
        $('#town-id').val("");
        $('#community-stage').val("");
        $('#community-step').val("");
        $('#create_community').attr('disabled', 'disabled');
        let getUrl = window.location;
        let baseUrl = getUrl.protocol + "//" + getUrl.host;
        $.when(
          $.get(baseUrl + "/api/resilience/stages_count")
              .done(function (data) {
                  $('#community-stage').attr("max", String(data.Stages_count));
                  console.log(JSON.stringify(data));
              })
        ).then(
          console.log("Got stages count from Database.")
        );

    });

//*****************************************************************************
    //get number of maximum steps for a given stage
    var steps_by_stage = {};
    function get_steps_by_stage(){
        let getUrl = window.location;
        let baseUrl = getUrl.protocol + "//" + getUrl.host;
        $.get(baseUrl + "/api/resilience/steps_count_by_stage/")
            .done(function (data) {
                steps_by_stage = data.Steps_count_by_stage;
                console.log("Steps by stage: "+JSON.stringify(steps_by_stage));
            });
    };


//*****************************************************************************
  //Get the maximun number of steps a stage can have
    $('#community-stage').change(function () {
        let stage_number = $('#community-stage').val();
        if (steps_by_stage === undefined) {
            get_steps_by_stage();
        }
        $('#community-step').attr("max", String(steps_by_stage[stage_number]));
        console.log("Steps by stage: "+JSON.stringify(steps_by_stage));
    });

//******************************************************************************
    //Get states (provincias) and fill the respective dropdown select with them
    function getProvinces() {
        let getUrl = window.location;
        let baseUrl = getUrl.protocol + "//" + getUrl.host;
        $.get(baseUrl + "/api/towns/provinces")
            .done(function (data) {
                if (data != null) {
                    $('#state-select').append(new Option("Provincia:", "", true, true));
                    data.forEach(function (element) {
                        $('#state-select').append(new Option(element));
                    });
                    console.log("Provinces: "+JSON.stringify(data));
                }else{
                  console.log("Error in database: not provinces found.");
                }
            });
    }

//*****************************************************************************
    // Reload web page, erasing obtained data
    $('#reload').click(function () {
        var getUrl = window.location;
        var baseUrl = getUrl.protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[1];
        window.location.href = baseUrl;
        console.log("Reloading page.");
    });

//*****************************************************************************
    //Change page to create a community with its resilience details
    $('#create_community').click(async function () {
        let town = $('#community-select').val();
        let city = $('#city-select').val();
        let state = $('#state-select').val();
        let getUrl = window.location;
        let baseUrl = getUrl.protocol + "//" + getUrl.host;
        let communities_url = baseUrl + "/api/communities/";
        let percentages_url = "/api/resilience/accomplished_percentages/";
        let stage = $('#community-stage').val();
        let step = $('#community-step').val();
        let community_percentages_url = percentages_url.concat(
            stage,
            "/",
            step
        );
        console.log("%'s URL: "+community_percentages_url);
        let community_url = communities_url.concat(state, "/", city, "/", town);
        let current_badge_url = baseUrl + "/api/resilience/badge/" + stage + "/" + step;
        console.log("Badges URL: "+current_badge_url);
        let current_badge = {};
        let POST_OBJECT = {};
        POST_OBJECT.RESILIENCIA = {};
        POST_OBJECT.RESILIENCIA.RESILIENCIA = {};
        POST_OBJECT.RESILIENCIA.RESILIENCIA.badges = [];
        POST_OBJECT.RESILIENCIA.RESILIENCIA.stage = Number(stage);
        POST_OBJECT.RESILIENCIA.RESILIENCIA.step = Number(step);
        console.log("POST Object (init): "+JSON.stringify(POST_OBJECT));
        $.when(
            $.get(community_url, function (data) {
                POST_OBJECT.RESILIENCIA.RESILIENCIA.badges = data.RESILIENCIA.badges;
                console.log("POST Object (with badges): "+JSON.stringify(POST_OBJECT));
            }),
            $.get(community_percentages_url, function (data) {
                POST_OBJECT.RESILIENCIA.RESILIENCIA.resilience_stage_level = data.Stage;
                POST_OBJECT.RESILIENCIA.RESILIENCIA.resilience_total_level = data.Total;
                console.log("POST Object (with stage & step levels): "+JSON.stringify(POST_OBJECT));
            })
        ).then(function () {
                $.when(
                  $.get(current_badge_url, function (data) {
                      let this_badge = data;
                      let date = new Date();
                      let badge_date = String(date.getFullYear()) + '-' + String(Number(date.getMonth()) + 1) + '-' + date.getDate();
                      this_badge.date = badge_date;
                      POST_OBJECT.RESILIENCIA.RESILIENCIA.badges.push(this_badge);
                      console.log("POST Object (with new badge): "+JSON.stringify(POST_OBJECT));
                  })
                ).then(function(){
                  console.log(JSON.stringify(POST_OBJECT));
                    $.ajaxSetup({
                        headers: {
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        }
                    });
                    $.post(community_url, JSON.stringify(POST_OBJECT), function (data, status) {
                        alert("Data: " + data + "\nStatus: " + status);
                    });
                })
            }
        )
    });

//******************************************************************************
    //Search community data when Search button is pressed
    $('#search').click(function () {
        let town = $('#community-select').val();
        let city = $('#city-select').val();
        let state = $('#state-select').val();
        let getUrl = window.location;
        let baseUrl = getUrl.protocol + "//" + getUrl.host;
        let communities_url = baseUrl + "/api/communities/";
        let community_url = communities_url.concat(state, "/", city, "/", town);
        console.log("Community URL: "+community_url);
        if (state.length > 0 && city.length > 0 && town.length > 0) {
            $.get(community_url, function (data) {
                console.log(JSON.stringify(data));
                if (data != null) {
                    console.log("Community data: "+JSON.stringify(data));
                    let community_name = data.PUEBLO;
                    $('#community-name').val(community_name);
                    $('#town-id').val(data.POBLAC_ID);
                    $('#create_community').removeAttr('disabled');
                    $('#community-stage').val(data.RESILIENCIA.stage);
                    $('#community-step').val(data.RESILIENCIA.step);
                    $('#total-progress').html(data.RESILIENCIA.resilience_total_level+"%");
                    let total_progress_width = "width:"+ data.RESILIENCIA.resilience_total_level + "%";
                    $('#total-progress-bar').attr({
                        "style":total_progress_width,
                        "aria-valuenow":String(data.RESILIENCIA.resilience_total_level)
                    });
                    $('#stage-progress').html(data.RESILIENCIA.resilience_stage_level+"%");
                    let stage_progress_width = "width:"+ data.RESILIENCIA.resilience_stage_level + "%";
                    $('#stage-progress-bar').attr({
                        "style":stage_progress_width,
                        "aria-valuenow":String(data.RESILIENCIA.resilience_stage_level)
                    });
                    let badges_number = data.RESILIENCIA.badges.length;
                    let getUrl = window.location;
                    let baseUrl = getUrl.protocol + "//" + getUrl.host;
                    $.get(baseUrl + "/api/resilience/steps_count").done(function (data) {
                        let total_steps = String(data.Steps_count);
                        $('#step-progress').html(badges_number+"/"+total_steps);
                        $('#step-progress-bar').attr({
                            "style":total_progress_width,
                            "aria-valuemax":total_steps,
                            "aria-valuenow":String(badges_number)
                            });
                    });
                    $('#community_id').val(data.RESILIENCIA['_id']);
                    $('#community_rev').val(data.RESILIENCIA['_rev']);
                    $.get(baseUrl + "/api/resilience/badge/"
                        + $('#community-stage').val()
                        + "/"
                        + $('#community-step').val())
                        .done(function (data) {
                            $('#current_badge').val(data.description);
                            $('#current_badge_type').val(data.type);
                        });
                } else {
                    $('#community-name').val('Community not found');
                }
            });
        } else if (state == "Provincia:" || city == "Cantón:" || town == "Poblado:") {
            $('#state-name').empty();
            $('#city-name').empty();
            $('#town-name').empty();
            $('#town-id').empty();
        }
        $('#create_community').removeAttr('disabled');
    });

//******************************************************************************
    //Get cities (canton) when state (provincia) changes
    $('#state-select').change(function () {
        $('#community-select').empty();
        $('#city-select').empty();
        let getUrl = window.location;
        let baseUrl = getUrl.protocol + "//" + getUrl.host;
        $.get(baseUrl + "/api/towns/" + $('#state-select option:selected').val())
            .done(function (data) {
                if (data != null) {
                    console.log("Cities data: "+data);
                    $('#city-select').append(new Option("Cantón:", "", true, true));
                    data.forEach(function (element) {
                        $('#city-select').append(new Option(element));
                    });
                }else{
                  console.log("Error in database, cities not found");
                }
            })
    });


//******************************************************************************
    //Get town (pueblo) when city changes
    $('#city-select').change(function () {
        $('#community-select').empty();
        let getUrl = window.location;
        let baseUrl = getUrl.protocol + "//" + getUrl.host;
        $.get(baseUrl + "/api/towns/"
            + $('#state-select option:selected').val()
            + '/'
            + $('#city-select option:selected').val())
            .done(function (data) {
                if (data != null) {
                    console.log("Communities: "+data);
                    $('#community-select').append(new Option("Poblado:", "", true, true));
                    data.forEach(function (element) {
                        $('#community-select').append(new Option(element));
                    });
                }else{
                  console.log("Database error: communities not found.");
                }
            })
    });
