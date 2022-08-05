(function ($) {
    $.each(['show', 'hide'], function (i, ev) {
        let el = $.fn[ev];
        $.fn[ev] = function () {
            this.trigger(ev);
            return el.apply(this, arguments);
        };
    });
})(jQuery);
$(':input').focus(function () {
    let center = $(window).height() / 2;
    let top = $(this).offset().top;
    if (top > center) {
        $(window).scrollTop(top - center);
    }
})
$(".formfield").on("show", function () {
    let div = $(this);
    setTimeout(function () {
        let input = div.find(":input").first();
        input.trigger('focus');
    }, 50);
})
$("#CRS_A0 :input").change((e) => {
    let marriage_status = $(e.target).val();
    console.log(marriage_status)
    if (marriage_status) {
        hide_after("#CRS_A0");
        $("#CRS_A1").show();
    } else {
        hide_after("#CRS_A0");
    }
})
$("#CRS_A1 :input").change((e) => {
    let age_group = $(e.target).val();
    if (age_group < 0) {
        hide_after("#CRS_A1");
        end();
    } else if (age_group >= 0) {
        $("#CRS_A2").show();
        let crs_submit = $("#CRS_Submit");
        if (crs_submit.is(":visible")) {
            crs_submit.hide();
        }
    } else {
        hide_after("#CRS_A1");
    }
})
$("#CRS_A2 :input").change((e) => {
    let education_lv = $(e.target).val();
    if (education_lv === "") {
        hide_after("#CRS_A2");
    } else {
        $("#CRS_A2_1").show();
    }
})
$("#CRS_A2_1 :input").change((e) => {
    let education_canadian = $(e.target).val();
    if (education_canadian) {
        $("#CRS_A3").show();
    } else {
        hide_after("#CRS_A2_1")
    }
})
$("#CRS_A3 :input").change((e) => {
    let valid_first_language = $(e.target).val()
    if (valid_first_language === "False") {
        hide_after("#CRS_A3");
        end();
    } else {
        $("#CRS_A3_1").show()
        let crs_submit = $("#CRS_Submit");
        if (crs_submit.is(":visible")) {
            crs_submit.hide();
        }
    }
})
$("#CRS_A3_1 :input").change((e) => {
    $("#CRS_A3_1").find("optgroup")
    let first_language_test = $(e.target).val()
    let first_language_listening = $("#CRS_A3_2_L .form-control")
    let first_language_speaking = $("#CRS_A3_2_S .form-control")
    let first_language_reading = $("#CRS_A3_2_R .form-control")
    let first_language_writing = $("#CRS_A3_2_W .form-control")
    if (first_language_test) {
        first_language_listening.val("").trigger("change")
        first_language_speaking.val("").trigger("change")
        first_language_reading.val("").trigger("change")
        first_language_writing.val("").trigger("change")

        if (first_language_test === "0") {
            first_language_listening.attr("max", 12).attr("step", 1)
            first_language_speaking.attr("max", 12).attr("step", 1)
            first_language_reading.attr("max", 12).attr("step", 1)
            first_language_writing.attr("max", 12).attr("step", 1)
        } else if (first_language_test === "1") {
            first_language_listening.attr("max", 9).attr("step", 0.5)
            first_language_speaking.attr("max", 9).attr("step", 0.5)
            first_language_reading.attr("max", 9).attr("step", 0.5)
            first_language_writing.attr("max", 9).attr("step", 0.5)
        } else if (first_language_test === "2") {
            first_language_listening.attr("max", 300).attr("step", 1)
            first_language_speaking.attr("max", 450).attr("step", 1)
            first_language_reading.attr("max", 360).attr("step", 1)
            first_language_writing.attr("max", 450).attr("step", 1)
        } else if (first_language_test === "3") {
            first_language_listening.attr("max", 699).attr("step", 1)
            first_language_speaking.attr("max", 20).attr("step", 1)
            first_language_reading.attr("max", 699).attr("step", 1)
            first_language_writing.attr("max", 20).attr("step", 1)
        }

        $("#CRS_A3_2").show()
    } else {
        hide_after("#CRS_A3_1");
    }
})
$(".language1 input").change(() => {
    let first_language_listening = $("#CRS_A3_2_L .form-control").val()
    let first_language_speaking = $("#CRS_A3_2_S .form-control").val()
    let first_language_reading = $("#CRS_A3_2_R .form-control").val()
    let first_language_writing = $("#CRS_A3_2_W .form-control").val()

    if (first_language_listening &&
        first_language_speaking &&
        first_language_reading &&
        first_language_writing
    ) {
        $("#CRS_A4").show()
    } else if (
        first_language_listening === "" ||
        first_language_speaking === "" ||
        first_language_reading === "" ||
        first_language_writing === ""
    ) {
        hide_after("#CRS_A3_2");
    }
})
$("#CRS_A4 :input").change((e) => {
    let valid_second_language = $(e.target).val()
    if (valid_second_language === "False") {
        hide_after("#CRS_A4");
        $("#CRS_A5").show()
    } else if (valid_second_language === "True") {
        hide_after("#CRS_A4_1");
        let first_language = $("#CRS_A3_1 .form-control")
        let second_language = $("#CRS_A4_1 .form-control")
        let options = first_language.find("option")
        let values = $.map(options, function (option) {
            return option.value;
        });
        second_language.empty();

        if (jQuery.inArray(first_language.val(), ["0", "1"]) !== -1) {
            second_language.append(new Option("---------", ""));
            second_language.append(new Option(first_language.find("option[value=2]").text(), values[3]));
            second_language.append(new Option(first_language.find("option[value=3]").text(), values[4]));
        } else {
            second_language.append(new Option("---------", ""));
            second_language.append(new Option(first_language.find("option[value=0]").text(), values[1]));
            second_language.append(new Option(first_language.find("option[value=1]").text(), values[2]));
        }
        $("#CRS_A4_1").show()
        setTimeout(function () {
            $("#CRS_A4_1 .form-control").trigger('focus')
        }, 50)

    } else {
        hide_after("#CRS_A4");
    }
})
$("#CRS_A4_1 :input").change((e) => {
    let second_language_test = $(e.target).val()
    let second_language_listening = $("#CRS_A4_2_L .form-control")
    let second_language_speaking = $("#CRS_A4_2_S .form-control")
    let second_language_reading = $("#CRS_A4_2_R .form-control")
    let second_language_writing = $("#CRS_A4_2_W .form-control")
    if (second_language_test) {
        second_language_listening.val("").trigger("change")
        second_language_speaking.val("").trigger("change")
        second_language_reading.val("").trigger("change")
        second_language_writing.val("").trigger("change")

        if (second_language_test === "0") {
            second_language_listening.attr("max", 12).attr("step", 1)
            second_language_speaking.attr("max", 12).attr("step", 1)
            second_language_reading.attr("max", 12).attr("step", 1)
            second_language_writing.attr("max", 12).attr("step", 1)
        } else if (second_language_test === "1") {
            second_language_listening.attr("max", 9).attr("step", 0.5)
            second_language_speaking.attr("max", 9).attr("step", 0.5)
            second_language_reading.attr("max", 9).attr("step", 0.5)
            second_language_writing.attr("max", 9).attr("step", 0.5)
        } else if (second_language_test === "2") {
            second_language_listening.attr("max", 300).attr("step", 1)
            second_language_speaking.attr("max", 450).attr("step", 1)
            second_language_reading.attr("max", 360).attr("step", 1)
            second_language_writing.attr("max", 450).attr("step", 1)
        } else if (second_language_test === "3") {
            second_language_listening.attr("max", 699).attr("step", 1)
            second_language_speaking.attr("max", 20).attr("step", 1)
            second_language_reading.attr("max", 699).attr("step", 1)
            second_language_writing.attr("max", 20).attr("step", 1)
        }

        $("#CRS_A4_2").show()
    } else {
        hide_after("#CRS_A4_1")
    }
})
$(".language2 input").change(() => {
    let second_language_listening = $("#CRS_A4_2_L .form-control").val()
    let second_language_speaking = $("#CRS_A4_2_S .form-control").val()
    let second_language_reading = $("#CRS_A4_2_R .form-control").val()
    let second_language_writing = $("#CRS_A4_2_W .form-control").val()

    if (second_language_listening &&
        second_language_speaking &&
        second_language_reading &&
        second_language_writing
    ) {
        $("#CRS_A5").show()
    } else if (
        second_language_listening === "" ||
        second_language_speaking === "" ||
        second_language_reading === "" ||
        second_language_writing === ""
    ) {
        hide_after("#CRS_A4_2");
    }
})
$("#CRS_A5 :input").change((e) => {
    let work_experience = $(e.target).val();

    if (work_experience === "0") {
        hide_after("#CRS_A5");
        end();
    } else if (jQuery.inArray(work_experience, ["1", "2", "3", "4", "5"]) !== -1) {
        $("#CRS_A5_1").show()
        let crs_submit = $("#CRS_Submit");
        if (crs_submit.is(":visible")) {
            crs_submit.hide();
        }
    } else {
        hide_after("#CRS_A5");
    }
})
$("#CRS_A5_1 :input").change((e) => {
    let noc = $(e.target).val();
    if (noc) {
        $("#CRS_A6").show()
    } else {
        hide_after("#CRS_A5_1");
    }
})
$("#CRS_A6 :input").change((e) => {
    let work_experience = $(e.target).val();
    let marriage_status = $("#CRS_A0 :input").val();
    console.log(jQuery.inArray(marriage_status, ["1", "2", "3"]) !== -1)

    if (work_experience === "0") {
        hide_after("#CRS_A6");
        end();
    } else if (jQuery.inArray(work_experience, ["1", "2", "3", "4", "5"]) !== -1) {
        if (jQuery.inArray(marriage_status, ["1", "2", "3"]) !== -1) {
            $("#CRS_B").show()
            $("#CRS_B1").show()
        } else {
            $("#CRS_C").show()
            $("#CRS_C1").show()
        }

        let crs_submit = $("#CRS_Submit");
        if (crs_submit.is(":visible")) {
            crs_submit.hide();
        }
    } else {
        hide_after("#CRS_A6");
    }
})
$("#CRS_B1 :input").change((e) => {
    let partner_education_lv = $(e.target).val()
    if (partner_education_lv) {
        $("#CRS_B2").show()
    } else {
        hide_after("#CRS_B1");
    }
})
$("#CRS_B2 :input").change((e) => {
    let valid_partner_language = $(e.target).val()
    if (valid_partner_language === "True") {
        $("#CRS_B2_1").show()
    } else if (valid_partner_language === "False") {
        hide_after("#CRS_B2")
        $("#CRS_B3").show()
    } else {
        hide_after("#CRS_B2")
    }
})
$("#CRS_B2_1 :input").change((e) => {
    let partner_language_test = $(e.target).val()
    let partner_language_listening = $("#CRS_B2_2_L .form-control")
    let partner_language_speaking = $("#CRS_B2_2_S .form-control")
    let partner_language_reading = $("#CRS_B2_2_R .form-control")
    let partner_language_writing = $("#CRS_B2_2_W .form-control")

    if (partner_language_test) {
        partner_language_listening.val("").trigger("change")
        partner_language_speaking.val("").trigger("change")
        partner_language_reading.val("").trigger("change")
        partner_language_writing.val("").trigger("change")

        if (partner_language_test === "0") {
            partner_language_listening.attr("max", 12).attr("step", 1)
            partner_language_speaking.attr("max", 12).attr("step", 1)
            partner_language_reading.attr("max", 12).attr("step", 1)
            partner_language_writing.attr("max", 12).attr("step", 1)
        } else if (partner_language_test === "1") {
            partner_language_listening.attr("max", 9).attr("step", 0.5)
            partner_language_speaking.attr("max", 9).attr("step", 0.5)
            partner_language_reading.attr("max", 9).attr("step", 0.5)
            partner_language_writing.attr("max", 9).attr("step", 0.5)
        } else if (partner_language_test === "2") {
            partner_language_listening.attr("max", 300).attr("step", 1)
            partner_language_speaking.attr("max", 450).attr("step", 1)
            partner_language_reading.attr("max", 360).attr("step", 1)
            partner_language_writing.attr("max", 450).attr("step", 1)
        } else if (partner_language_test === "3") {
            partner_language_listening.attr("max", 699).attr("step", 1)
            partner_language_speaking.attr("max", 20).attr("step", 1)
            partner_language_reading.attr("max", 699).attr("step", 1)
            partner_language_writing.attr("max", 20).attr("step", 1)
        }

        $("#CRS_B2_2").show()
    } else {
        hide_after("#CRS_B2_1")
    }
})
$(".language3 input").change(() => {
    let partner_language_listening = $("#CRS_B2_2_L .form-control").val()
    let partner_language_speaking = $("#CRS_B2_2_S .form-control").val()
    let partner_language_reading = $("#CRS_B2_2_R .form-control").val()
    let partner_language_writing = $("#CRS_B2_2_W .form-control").val()

    if (partner_language_listening &&
        partner_language_speaking &&
        partner_language_reading &&
        partner_language_writing
    ) {
        $("#CRS_B3").show()
    } else if (
        partner_language_listening === "" ||
        partner_language_speaking === "" ||
        partner_language_reading === "" ||
        partner_language_writing === ""
    ) {
        hide_after("#CRS_B2_2")
    }
})
$("#CRS_B3 :input").change((e) => {
    let partner_work_experience = $(e.target).val()
    if (partner_work_experience) {
        $("#CRS_C").show()
        $("#CRS_C1").show()
    } else {
        hide_after("#CRS_B3")
    }
})
$("#CRS_C1 :input").change((e) => {
    let valid_certificate = $(e.target).val()
    if (valid_certificate) {
        $("#CRS_C2").show()
    } else {
        hide_after("#CRS_C1")
    }
})
$("#CRS_C2 :input").change((e) => {
    let valid_job_offer = $(e.target).val()
    if (valid_job_offer) {
        $("#CRS_C3").show()
    } else {
        hide_after("#CRS_C2")
    }
})
$("#CRS_C3 :input").change((e) => {
    let valid_nomination = $(e.target).val()
    if (valid_nomination) {
        $("#CRS_C4").show()
    } else {
        hide_after("#CRS_C3")
    }
})
$("#CRS_C4 :input").change((e) => {
    let valid_relatives_citizen = $(e.target).val()
    if (valid_relatives_citizen) {
        end()
    } else {
        hide_after("#CRS_C4")
    }
})