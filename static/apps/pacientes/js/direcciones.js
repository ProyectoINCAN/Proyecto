   $( document ).ready(function() {
       $('#create').click(function(){
          $('#modalDireccion').modal('show');
       })
   })
    $("#id_nro_casa").attr("min", 1)
   $("#id_departamento").change(function () {
      console.log( $(this).val() );
      var departamento = $(this).val()
      console.log("departamento", departamento)

      $.ajax({
        url: '/principal/distrito/'+departamento,
        data: {
          'departamento': departamento
        },
        dataType: 'json',
        success: function (data) {
                console.log("data", data)
                console.log("data", data[4])
        console.log("data", data.length)
            $("#id_distrito").empty();
            $.each($.parseJSON(data), function( key, value ) {
              html = "<option value="+value['pk']+">"+value['fields'].nombre+"</option>";
              console.log('html', html)
              $("#id_distrito").append(html);

            });
        }
      });
   });

   $("#id_distrito").change(function () {
     var distrito = $(this).val()
     actualizarBarrio(distrito)

      console.log( $(this).val() );
  })

   var actualizarBarrio = function(distrito){
    $.ajax({
        url: '/principal/barrio/'+distrito,
        data: {
          'distrito': distrito
        },
        dataType: 'json',
        success: function(data){
            $("#id_barrio").empty();
            $.each($.parseJSON(data), function(key, value) {
               console.log("barrio", value)
               console.log("barrio", value[4])
               html = "<option value="+value['pk']+">"+value['fields'].nombre+"</option>";
               $("#id_barrio").append(html);

            });

        }
    })
  };

