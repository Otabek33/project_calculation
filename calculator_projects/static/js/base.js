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
