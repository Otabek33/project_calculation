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

    if (self_total_price) {
        changed_margin_amount = parseFloat(self_total_price) - parseFloat(project_total_price_by_stage_and_task.text())
        td_changed_margin_amount.text(changed_margin_amount.formatMoney(2, ' ', ',') + " сўм")
        changed_tax_amount = parseFloat(self_total_price) * 0.01
        project_tax_update_part.text(changed_tax_amount.formatMoney(2, ' ', ',') + " сўм")

        changeTotalPriceOfProjectWithAdditionalCost(parseFloat(self_total_price))
        updatingPercentageAfterChangingSelfTotalPrice(changed_margin_amount, parseFloat(self_total_price))
    }
    project_total_price_hidden.text(parseFloat(self_total_price))

}

function calculateTotalPriceWithMargin() {

    let changed_margin_amount = $("#changed_margin")
    let total_price_of_project = $("#total_price_of_project")
    let project_tax_update_part = $("#project_tax_update_part")

    let project_total_price_hidden = $("#project-total-price-hidden")
    let project_total_price_hidden_after_change = $("#project-total-price-hidden-after-change")


    let margin = document.getElementById("margin_percentage").value
    let project_total_price_by_stage_and_task = document.getElementById("project_total_price_by_stage_and_task");
    let project_tax_amount = document.getElementById("project_tax_amount");
    let parsed_total_price = parseFloat(project_total_price_by_stage_and_task.innerText.replace(/,/g, '.'));
    let parsed_tax_amount = parseFloat(project_tax_amount.innerText.replace(/,/g, '.'));
    let margin_after_changed_percent = Number(margin) / 100 * parsed_total_price
    changed_margin_amount.text((margin_after_changed_percent.formatMoney(2, ' ', ',')) + " сўм")
    let changed_total_price_of_project = (parsed_total_price - parsed_tax_amount + margin_after_changed_percent) * 100 / 99

    total_price_of_project.val(changed_total_price_of_project.formatMoney(2, ' ', ',') + " сўм")
    let changed_tax = changed_total_price_of_project - (parsed_total_price - parsed_tax_amount + margin_after_changed_percent)

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
//     let project_additional_cost = $("#project-additional-cost")
// + parseFloat(project_additional_cost.text())
    let changed_amount_of_project_with_additional_cost = changed_total_price_of_project

    total_price_with_additional_cost.text(changed_amount_of_project_with_additional_cost)
    total_price_of_project_in_footer_part.text(changed_amount_of_project_with_additional_cost.formatMoney(2, ' ', ',') + " сўм")
    total_price_with_additional_cost_update_part.text(changed_amount_of_project_with_additional_cost.formatMoney(2, ' ', ',') + " сўм")

}
$("#additional-cost-form-modal").on('submit', function (e) {
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
        success: function () {
            window.location.reload()
        },
        error: function (err) {
            console.log(err)
        }
    })

})