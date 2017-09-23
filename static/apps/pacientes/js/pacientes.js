   console.log($("#id_nacionalidad").val())
   var nacionalidad = $("#id_nacionalidad").val()
        $.ajax({
        url: '/principal/nacionalidad/'+nacionalidad,
        data: {
          'nacionalidad': nacionalidad
        },
        dataType: 'json',
        success: function(data){
            $.each($.parseJSON(data), function( key, value ) {
              var pais = value["fields"].pais;
              actualizarDepartamento(pais);
            });
        }
      });

      var actualizarDepartamento = function(pais){
        $.ajax({
            url: '/principal/departamento/'+pais,
            data: {
              'pais': pais
            },
            dataType: 'json',
            success: function(data){
                var departamento = []
                $.each($.parseJSON(data), function(key, value) {
                    departamento.push(value['pk']);
                });
                console.log("depa", departamento)
                actualizarDistrito(departamento)

            }
        })
      };

      var actualizarDistrito = function(departamento){
        console.log("depart", departamento)
        $.ajax({
            url: '/principal/distrito/'+departamento,
            data: {
              'departamento': departamento
            },
            dataType: 'json',
            success: function(data){
                var departamento = []
                $.each($.parseJSON(data), function(key, value) {
                                console.log("depa", key)
//                   / departamento.push(value['pk']);
                });


            }
        })
      };

   $("#id_lugar_nacimiento").change(function () {
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