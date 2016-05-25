$("#departamento").change(function() {
  var dep_id = $(this).find(":selected").val();
  //alert(dep_id);
  var request = $.ajax({
        type: 'GET',
        url: '/getProvincias/' + dep_id ,
    });
    request.done(function(data){

        $("#provincia").empty();
        $("#ciudad").empty();



        $("#provincia").append(
          $("<option></option>").attr(
            "value", "").text("--seleccionar--")
        );

        $("#ciudad").append(
          $("<option></option>").attr(
            "value", "").text("")
        );

        $('#ciudad').prop('disabled', 'disabled');

        for (var i = 0; i < data.regions.length; i++) {
            //alert(data.regions[i].Nombre)
            $("#provincia").append(
                $("<option></option>").attr(
                    "value", data.regions[i].Id).text(data.regions[i].Nombre)
            );
        }

    });
});

$("#provincia").change(function() {
  var prov_id = $(this).find(":selected").val();
  var request = $.ajax({
        type: 'GET',
        url: '/getCiudades/' + prov_id ,
    });
    request.done(function(data){

        $("#ciudad").empty();
        $('#ciudad').prop('disabled', false);
        for (var i = 0; i < data.regions.length; i++) {
            $("#ciudad").append(
                $("<option></option>").attr(
                    "value", data.regions[i].Id).text(data.regions[i].Nombre)
            );
        }
    });
});
