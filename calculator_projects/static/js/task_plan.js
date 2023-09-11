$(".edit-task-row").on("click", function (e) {
    e.preventDefault();
    let actionUrl = $(this).attr("href")
    $("#task-update-form").attr("action", actionUrl)
    $.ajax({
        type: "GET",
        url: actionUrl,
        success: function (data) {
            for (var key in data) {
                $("#task-update-form").find('[name="' + key + '"]').val(data[key]);
            }
        }
    })
    // Remove link row from DOM
    $("#taskUpdateModal").modal('show')
})
$("#task-update-form").on('submit', function (e) {
    e.preventDefault()
    let form = $(this);
    let actionUrl = form.attr('action') + '/';
    data = form.serialize()
    $.ajax({
        type: "PUT",
        url: actionUrl,
        data: form.serialize(),
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (data) {
            $("#taskAddModal").modal('hide')
            localStorage.setItem("msg", "Задача успешно обновлен")
            window.location.reload()
        },
        error: function (err) {
            console.log(err)
        }
    })
})
$(".delete-task-row").on("click", function (e) {
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
$("#task-add-form").on('submit', function (e) {
    e.preventDefault()
    let form = $(this);
    let actionUrl = form.attr('action');
    data = form.serialize()
    $.ajax({
        type: "POST",
        url: actionUrl,
        data: form.serialize(), // serializes the form's elements.
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (data) {
            localStorage.setItem("msg", "Задание успешно добавлено!")
            $("#stageModal").modal('hide')
            window.location.reload();
        },
        error: function (err) {
            console.log(err)
        }
    })

})
