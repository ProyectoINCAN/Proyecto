   $( document ).ready(function() {
       $('#create').click(function(){
          $('#modalDireccion').modal('show');
       })
   })

   $("#id_departamento").change(function () {
      console.log( $(this).val() );
      var departamento = $(this).val()
      console.log("departamento", departamento)

      $.ajax({
        url: '/comunes/distrito/'+departamento,
        data: {
          'departamento': departamento
        },
        dataType: 'json',
        success: function (data) {
                console.log("data", data)
                console.log("data", data[4])
        console.log("data", data.length)
//        success: function(data){
            $("#id_distrito").empty();
            $.each($.parseJSON(data), function( key, value ) {

              console.log('hola', key);
              console.log('data', value);
              console.log('hola', value["fields"].nombre);
              console.log('hola', value["model"]);
              html = "<option value="+value['pk']+">"+value['fields'].nombre+"</option>";
              console.log('html', html)
              $("#id_distrito").append(html);

            });

        }
      });
   });

