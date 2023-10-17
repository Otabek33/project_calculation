Number.prototype.formatMoney = function (decPlaces, thouSeparator, decSeparator) {
    var n = this,
        decPlaces = isNaN(decPlaces = Math.abs(decPlaces)) ? 2 : decPlaces,
        decSeparator = decSeparator == undefined ? "." : decSeparator,
        thouSeparator = thouSeparator == undefined ? "," : thouSeparator,
        sign = n < 0 ? "-" : "",
        i = parseInt(n = Math.abs(+n || 0).toFixed(decPlaces)) + "",
        j = (j = i.length) > 3 ? j % 3 : 0;
    return sign + (j ? i.substr(0, j) + thouSeparator : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + thouSeparator) + (decPlaces ? decSeparator + Math.abs(n - i).toFixed(decPlaces).slice(2) : "");
};

function selfWriteTotalPriceOfProject() {
    let self_total_price = document.getElementById("total_price_of_project").value
    let project_total_price_hidden = $("#project-total-price-hidden")
    let td_changed_margin_amount = $("#changed_margin")
    let project_tax_update_part = $("#project_tax_update_part")
    let project_total_price_by_stage_and_task = $("#project_total_price_by_stage_and_task")

    const regex_number = self_total_price.replace(/,/g, '.').replaceAll(/\s/g, '');
    if (regex_number) {
        changed_margin_amount = parseFloat(regex_number) - parseFloat(project_total_price_by_stage_and_task.text())
        td_changed_margin_amount.text(changed_margin_amount.formatMoney(2, ' ', ',') + " сўм")
        changed_tax_amount = parseFloat(regex_number) * 0.01
        project_tax_update_part.text(changed_tax_amount.formatMoney(2, ' ', ',') + " сўм")
        changeTotalPriceOfProjectWithAdditionalCost(parseFloat(regex_number))
        updatingPercentageAfterChangingSelfTotalPrice(changed_margin_amount, parseFloat(regex_number))
    }
    project_total_price_hidden.text(parseFloat(regex_number))

}

function calculateTotalPriceWithMargin() {

    let changed_margin_amount = $("#changed_margin")
    let total_price_of_project = $("#total_price_of_project")
    let project_tax_update_part = $("#project_tax_update_part")

    let project_total_price_hidden = $("#project-total-price-hidden")
    let margin = document.getElementById("margin_percentage").value
    let project_total_price_by_stage_and_task = document.getElementById("project_total_price_by_stage_and_task");
    let cost_price_of_project_amount = document.getElementById("cost_price_of_project_amount");
    let salary_cost_of_project_amount = document.getElementById("salary_cost_of_project_amount");
    let period_expenses_of_project_amount = document.getElementById("period_expenses_of_project_amount");

    let parsed_total_price = parseFloat(project_total_price_by_stage_and_task.innerText.replace(/,/g, '.'));
    let parsed_cost = parseFloat(cost_price_of_project_amount.innerText.replace(/,/g, '.'));
    let parsed_salary = parseFloat(salary_cost_of_project_amount.innerText.replace(/,/g, '.'));
    let parsed_expenses = parseFloat(period_expenses_of_project_amount.innerText.replace(/,/g, '.'));
    let margin_after_changed_percent = Number(margin) / 100 * parsed_total_price
    changed_margin_amount.text((margin_after_changed_percent.formatMoney(2, ' ', ',')) + " сўм")

    let changed_total_price_of_project = (parsed_cost + parsed_salary + parsed_expenses + margin_after_changed_percent) / 0.99


    total_price_of_project.val(changed_total_price_of_project.formatMoney(2, ' ', ','))
    let changed_tax = changed_total_price_of_project * 0.01

    project_tax_update_part.text(changed_tax.formatMoney(2, ' ', ',') + " сўм")
    project_total_price_hidden.text(changed_total_price_of_project)

    changeTotalPriceOfProjectWithAdditionalCost(changed_total_price_of_project)
    updatingPercentageAfterChangingMargin(changed_total_price_of_project)

}

function updatingPercentageAfterChangingMargin(changed_total_price_of_project) {
    let cost_price_of_project = $("#cost_price_of_project_percent")
    let salary_cost_of_project_percent = $("#salary_cost_of_project_percent")
    let period_expenses_of_project_percent = $("#period_expenses_of_project_percent")
    let cost_price_of_project_amount = parseFloat(document.getElementById("cost_price_of_project_amount").innerText.replace(/,/g, '.'));
    let salary_cost_of_project_amount = parseFloat(document.getElementById("salary_cost_of_project_amount").innerText.replace(/,/g, '.'));
    let period_expenses_of_project_amount = parseFloat(document.getElementById("period_expenses_of_project_amount").innerText.replace(/,/g, '.'));

    cost_price_of_project.text((cost_price_of_project_amount / changed_total_price_of_project * 100).formatMoney(2, ' ', ',') + " %")
    salary_cost_of_project_percent.text((salary_cost_of_project_amount / changed_total_price_of_project * 100).formatMoney(2, ' ', ',') + " %")
    period_expenses_of_project_percent.text((period_expenses_of_project_amount / changed_total_price_of_project * 100).formatMoney(2, ' ', ',') + " %")
}

function updatingPercentageAfterChangingSelfTotalPrice(changed_margin_amount, self_total_price) {
    let margin_percentage = $("#margin_percentage")
    let cost_price_of_project = $("#cost_price_of_project_percent")
    let salary_cost_of_project_percent = $("#salary_cost_of_project_percent")
    let period_expenses_of_project_percent = $("#period_expenses_of_project_percent")
    let cost_price_of_project_amount = parseFloat(document.getElementById("cost_price_of_project_amount").innerText.replace(/,/g, '.'));
    let salary_cost_of_project_amount = parseFloat(document.getElementById("salary_cost_of_project_amount").innerText.replace(/,/g, '.'));
    let period_expenses_of_project_amount = parseFloat(document.getElementById("period_expenses_of_project_amount").innerText.replace(/,/g, '.'));

    margin_percentage.val((changed_margin_amount / self_total_price * 100).formatMoney(2, ' ', ','))
    cost_price_of_project.text((cost_price_of_project_amount / self_total_price * 100).formatMoney(2, ' ', ',') + " %")
    salary_cost_of_project_percent.text((salary_cost_of_project_amount / self_total_price * 100).formatMoney(2, ' ', ',') + " %")
    period_expenses_of_project_percent.text((period_expenses_of_project_amount / self_total_price * 100).formatMoney(2, ' ', ',') + " %")
}


function changeTotalPriceOfProjectWithAdditionalCost(changed_total_price_of_project) {
    let total_price_with_additional_cost = $("#total-price-with-additional-cost")
    let total_price_of_project_in_footer_part = $("#total_price_of_project_in_footer_part")

    let total_price_with_additional_cost_update_part = $("#total-price-with-additional-cost-update-part")
    let project_additional_cost = $("#project-additional-cost")
    let changed_amount_of_project_with_additional_cost = changed_total_price_of_project + parseFloat(project_additional_cost.text())

    total_price_with_additional_cost.text(changed_amount_of_project_with_additional_cost)
    total_price_of_project_in_footer_part.text(changed_amount_of_project_with_additional_cost.formatMoney(2, ' ', ',') + " сўм")
    total_price_with_additional_cost_update_part.text(changed_amount_of_project_with_additional_cost.formatMoney(2, ' ', ',') + " сўм")

}

let amount = document.getElementById('additional_cost_amount');


$("#additional-cost-form-modal").on('submit', function (e) {
    e.preventDefault()
    let form = $(this);
    let amount = document.getElementById('additional_cost_amount').value;
    let actionUrl = form.attr('action');
    const regex_number = amount.replace(/,/g, '.').replaceAll(/\s/g, '');
    document.getElementById("additional_cost_amount").value = parseFloat(regex_number);
    $.ajax({
        type: "POST",
        url: actionUrl,
        data: form.serialize(), // serializes the form's elements.
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function () {
            localStorage.setItem("msg", "Дополнительный расход успешно добавлен")
            window.location.reload();
        },
        error: function (err) {
            console.log(err)
        }
    })

})

$(".additional-cost-edit-row").on("click", function (e) {
    e.preventDefault();
    let actionUrl = $(this).attr("href")

    let amount = $(this).attr("data-store-id")

    $("#additional-cost-update-form-modal").attr("action", actionUrl)
    $.ajax({
        type: "GET",
        url: actionUrl,
        success: function (data) {
            for (var key in data) {
                $("#additional-cost-update-form-modal").find('[name="' + key + '"]').val(data[key]);
            }
            $("#amount-update-hidden").val(amount)
        }
    })

    $("#additional-cost-update-modal").modal('show')
})


$("#additional-cost-update-form-modal").on('submit', function (e) {
    e.preventDefault()
    let form = $(this);
    let actionUrl = form.attr('action');
    let amount = document.getElementById('additional_cost_amount_update').value;
    const regex_number = amount.replace(/,/g, '.').replaceAll(/\s/g, '');
    document.getElementById("additional_cost_amount_update").value = parseFloat(regex_number);
    $.ajax({
        type: "PUT",
        url: actionUrl,
        data: form.serialize(),
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (data) {
            localStorage.setItem("msg", "Дополнительный расход успешно обновлен")
            window.location.reload();
        },
        error: function (err) {
            console.log(err)
        }
    })
})

$(".additional-cost-delete-row").on("click", function (e) {
    e.preventDefault();
    let actionUrl = $(this).attr("href")
    let amount = $(this).attr("data-store-id")

    $.ajax({
        type: "DELETE",
        url: actionUrl,
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function () {
            localStorage.setItem("msg", "Дополнительный расход успешно удален")
            window.location.reload();
        },
        error: function (err) {
            toastMixin.fire({
                title: err
            })
        }
    })
})


$(".sending_button").on("click", function (e) {
    var btn = $(this);

    let total_price_of_project = document.getElementById('total_price_of_project').value
    let project_tax_update_part = document.getElementById('project_tax_update_part')
    let changed_margin = document.getElementById('changed_margin')

    document.getElementById('margin_for_backend').setAttribute('value', changed_margin.innerText)
    document.getElementById('tax_for_backend').setAttribute('value', project_tax_update_part.innerText)
    document.getElementById('total_price_with_margin_for_backend').setAttribute('value', total_price_of_project)

});
