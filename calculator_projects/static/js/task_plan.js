
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
