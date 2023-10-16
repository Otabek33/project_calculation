const csrftoken = $("[name=csrfmiddlewaretoken]").val();
$("#stage-form-modal").on('submit', function (e) {
    e.preventDefault()
    let form = $(this);
    let actionUrl = form.attr('action');
    data = form.serialize()
    $.ajax({
        type: "POST",
        url: actionUrl,
        data: form.serialize(), // serializes the form's elements.
        success: function () {
            $(".close").click()
            localStorage.setItem("msg", "Этап успешно добавлен")
            window.location.reload();
        },
        error: function (response) {
            var error_message = response["responseJSON"]["error"];
            toast_show("error", error_message)
        }
    })
})


$(".delete-stagePlan-row").on("click", function (e) {
    e.preventDefault();
    let actionUrl = $(this).attr("href")
    $.ajax({
        type: "DELETE",
        url: actionUrl,
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function () {
            localStorage.setItem("msg", "Успешно удален")
            window.location.reload();
        },
        error: function (err) {
            toastMixin.fire({
                title: err
            })
        }
    })
})

$(".edit-row").on("click", function (e) {
    e.preventDefault();
    let actionUrl = $(this).attr("href")
    $("#stage-update-form").attr("action", actionUrl)
    $.ajax({
        type: "GET",
        url: actionUrl,
        success: function (data) {
            for (var key in data) {
                $("#stage-update-form").find('[name="' + key + '"]').val(data[key]);
            }
        }
    })
    // Remove link row from DOM
    $("#stageUpdateModal").modal('show')
})


$("#stage-update-form").on('submit', function (e) {
    e.preventDefault()
    let form = $(this);
    let actionUrl = form.attr('action') + "/";
    data = form.serialize()
    $.ajax({
        type: "PUT",
        url: actionUrl,
        data: form.serialize(), // serializes the form's elements.
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (data) {
            localStorage.setItem("msg", "Этап успешно обновлен")
            window.location.reload();
        },
        error: function (response) {
            var error_message = response["responseJSON"]["error"];
            toast_show("error", error_message)
        }
    })
})
