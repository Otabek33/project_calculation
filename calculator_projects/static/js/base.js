$("#confirm-delete-project-button").on("click", function (e) {
    e.preventDefault();

    var btn = $(this);

    let form_data = {
        "id": $('input[name="delete_project"]').val(),

    }

    execute_project_delete_post_request(url = btn.attr("data-href-template"), data = form_data)

})

function execute_project_delete_post_request(url, data) {

    $.ajax({
        type: "POST",
        url: url,
        data: data,
        headers: {
            "X-CSRFToken": csrf_token

        },
        success: function (data) {
            $(".close").click()
            localStorage.setItem("msg", "Проект успешно удален")
            window.location.reload();


        }


    })
}


$("#reject-project").on("click", function (e) {
    e.preventDefault();

    var btn = $(this);

    let form_data = {
        "id": $('input[name="reject_project_plan"]').val(),

    }
    execute_project_reject_post_request(url = btn.attr("data-href-template"), data = form_data)

})

function execute_project_reject_post_request(url, data) {

    $.ajax({
        type: "POST",
        url: url,
        data: data,
        headers: {
            "X-CSRFToken": csrf_token

        },
        success: function (data) {
            $(".close").click()
            localStorage.setItem("msg", "Проект успешно отклонен")
            window.location.reload();


        }


    })
}


$("#confirm-project").on("click", function (e) {
    e.preventDefault();

    var btn = $(this);

    let form_data = {
        "id": $('input[name="confirm_project"]').val(),

    }
    execute_project_confirm_post_request(url = btn.attr("data-href-template"), data = form_data)

})

function execute_project_confirm_post_request(url, data) {

    $.ajax({
        type: "POST",
        url: url,
        data: data,
        headers: {
            "X-CSRFToken": csrf_token

        },
        success: function (data) {
            $(".close").click()
            localStorage.setItem("msg", "Проект успешно подтвержден")
            window.location.reload();


        }


    })
}

$(".project_fact_task_update").on("click", function (e) {
    e.preventDefault();


    var btn = $(this);
    id = btn.attr("data-store-id")
    let form_data = {
        "worker": $('select[id="worker_' + id + '"]').val(),
        "task_status": $('select[name="task_fact_status_' + id + '"]').val(),
        "daterange": $('input[name="daterange_' + id + '"]').val(),
        "id": id,

    }
    console.log(btn.attr("data-href-template"))
    execute_plan_fact_task_fact_update(url = btn.attr("data-href-template"), data = form_data)

})

$("#task_fact_add_modal").on('submit', function (e) {
    e.preventDefault()
    let form = $(this);
    let actionUrl = form.attr('action');
    let form_data = {
        "name": $('textarea[name="task_fact_add_name"]').val(),
        "project": $('input[name="project_fact"]').val(),
        "date": $('input[name="daterange_task_fact"]').val(),
        "stage": $('select[name="task_fact_add_stage"]').val(),
        "status": $('select[name="task_fact_add_status"]').val(),
    }

    console.log(form_data, actionUrl)
    $.ajax({
        method: "POST",
        url: actionUrl,
        data: form_data,
        dataType: 'json',
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (data) {
            localStorage.setItem("msg", data.msg)
            window.location.reload()


        },
        error: function (response) {
            var error_message = response["responseJSON"]["error"];
            toast_show("error", error_message)
        }
    })

})


$("#additional_cost_fact_add_modal").on('submit', function (e) {
    e.preventDefault()
    let form = $(this);
    let actionUrl = form.attr('action');
    let form_data = {
        "comment": $('textarea[name="additional_cost_fact_comment"]').val(),
        "amount": $('input[name="additional_cost_fact_amount"]').val(),
        "type": $('select[name="additional_cost_fact_type"]').val(),
        "project": $('input[name="project_fact"]').val(),
    }


    $.ajax({
        method: "POST",
        url: actionUrl,
        data: form_data,
        dataType: 'json',
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (data) {
            localStorage.setItem("msg", data.msg)
            window.location.reload()

        },
        error: function (response) {
            var error_message = response["responseJSON"]["error"];
            toast_show("error", error_message)
        }
    })

})


$("#item-delete-additional-cost-fact").on('submit', function (e) {
    e.preventDefault()
    let form = $(this);
    let actionUrl = form.attr('action');
    let form_data = {
        "additional_cost": $('input[name="delete_additional_cost_fact"]').val(),
    }


    $.ajax({
        method: "POST",
        url: actionUrl,
        data: form_data,
        dataType: 'json',
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (data) {
            localStorage.setItem("msg", data.msg)
            window.location.reload()

        },
        error: function (response) {
            var error_message = response["responseJSON"]["error"];
            toast_show("error", error_message)
        }
    })

})

function execute_plan_fact_task_fact_update(url, data) {
    console.log(url, data)

    $.ajax({
        type: "POST",
        url: url,
        data: data,
        headers: {
            "X-CSRFToken": csrf_token

        },
        success: function (data) {
            $(".close").click()
            localStorage.setItem("msg", "Задача успешно обновлен")
            window.location.reload();


        },
        error: function (response) {
            var error_message = response["responseJSON"]["error"];
            toast_show("error", error_message)
        }


    })
}

$(".additional_cost_fact_edit_row").on("click", function (e) {
    e.preventDefault();
    let actionUrl = $(this).attr("href")

    let id = $(this).attr("data-id")


    $.ajax({
        type: "GET",
        url: actionUrl,
        data: {"id": id},
        success: function (data) {
            for (var key in data.data) {
                $("#additional_cost_fact_edit_modal").find('[name="' + key + '"]').val(data.data[key]);
            }
        }
    })
    $("#additional_cost_fact_edit_modal").attr("action", actionUrl)
    $("#editAdditionalCostFact").modal('show')
})


$("#additional_cost_fact_edit_modal").on('submit', function (e) {
    e.preventDefault()
    let form = $(this);
    let actionUrl = form.attr('action');
    let form_data = {
        "comment": $('textarea[name="comment"]').val(),
        "amount": $('input[name="amount"]').val(),
        "type": $('select[name="cost_type"]').val(),
        "project": $('input[name="project_fact"]').val(),
        "id": $('input[name="id"]').val(),
    }
    console.log(actionUrl, form_data)


    $.ajax({
        method: "POST",
        url: actionUrl,
        data: form_data,
        dataType: 'json',
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (data) {
            localStorage.setItem("msg", data.msg)
            window.location.reload()

        },
        error: function (response) {
            var error_message = response["responseJSON"]["error"];
            toast_show("error", error_message)
        }
    })

})

function toast_show(alert_type, message) {
    if (alert_type === "error") {
        toastr_danger_top_right(message)
    } else if (alert_type === "success") {
        toastr_success_top_right(message)
    }


}
