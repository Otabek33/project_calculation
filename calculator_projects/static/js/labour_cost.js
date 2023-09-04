let csrf_token = $('input[name="csrfmiddlewaretoken"]').val()

$("#labour_cost_for_project_calculation").on("click", function (e) {
    e.preventDefault();
    let btn = $(this);
    let form_data = {
        "id": $('input[name="activation_labour_cost"]').val(),
    }
    execute_status_of_labour_cost_update_post_request(url = btn.attr("data-href-template"), data = form_data)
})

function execute_status_of_labour_cost_update_post_request(url, data) {


    $.ajax({
        type: "POST",
        url: url,
        data: data,
        headers: {
            "X-CSRFToken": csrf_token

        },
        success: function (data) {

            $(".close").click()
            localStorage.setItem("msg", "Расчет активирован для проектов")
            window.location.reload();


        }

    })
}


$("#labour_cost_delete_modal").on("click", function (e) {
    e.preventDefault();
    var btn = $(this);
    let form_data = {
        "id": $('input[name="labour_cost_delete_name"]').val(),
    }
    execute_delete_labour_cost_post_request(url = btn.attr("data-href-template"), data = form_data)
})

function execute_delete_labour_cost_post_request(url, data) {


    $.ajax({
        type: "POST",
        url: url,
        data: data,
        headers: {
            "X-CSRFToken": csrf_token

        },
        success: function (data) {
            $(".close").click()
            localStorage.setItem("msg", "✅ Расчет успешно удален")
            window.location.reload();


        }

    })
}
