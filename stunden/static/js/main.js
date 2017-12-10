$(document).ready(function() {

    // Pagination
    function pagination() {
        stundenaufzeichnung = $("#stundenaufzeichnung");
        $(".pages").on("click", function(event){
            var href = $(this).attr("href");
            stundenaufzeichnung.fadeTo("fast", 0.1, function() {
                stundenaufzeichnung.load(href + " #stundenaufzeichnung > *", function () {
                    stundenaufzeichnung.fadeTo("slow", 1);
                    pagination();
                });
            })
            event.preventDefault();
        });
    }
    pagination();

    // Checkboxes toogle all auf der Rechnungsseite
    $(":checkbox#toggle-all").css("visibility", "visible");
    $(":checkbox#toggle-all").click(function() {
        var checkedStatus = this.checked;
        $(":checkbox.toggle-me").each(function() {
            $(this).prop("checked", checkedStatus);
        });
    });

    // Datepicker
    $("#id_datum").datepicker({
        dateFormat: "dd.mm.yy",
        showOtherMonths: true,
        selectOtherMonths: true
        },
        $.datepicker.regional["de"]
    );

    // Timepicker Startzeit
    $('#id_startzeit').clockpicker({
        autoclose: true
    });

    // Timepicker Endzeit
    $('#id_endzeit').clockpicker({
        autoclose: true
    });

    // Rechnung Firma-Checkbox-Auswahl Stundensatz Eintrag
    $("#id_firma").change(function() {
        if(document.location.pathname == "/rechnung/") {
            selected_firma_id = $(this).val();
            if (selected_firma_id) {
                request_url = "/get_firma_stundensatz/" + selected_firma_id + "/";
                $.ajax({
                    url: request_url,
                    success: function(data) {
                        var firma_stundensatz = data["firma_stundensatz"]
                        if (firma_stundensatz) {
                            $("#id_rechnungs_stundenlohn").val(firma_stundensatz).effect("highlight");
                        } else {
                            $("#id_rechnungs_stundenlohn").val("").effect("highlight", {color: "red"});
                        }
                    }
                })
            }
        }
    });

});
