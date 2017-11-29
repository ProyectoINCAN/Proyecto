   console.log($("#id_nacionalidad").val())
 console.log("entro")
   $("#id_tipo_doc").change(function () {
       console.log("entro")
   }

           $("input[name='tipo_doc']").focus(function(){
        console.log("entro")
this.select();
});
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
                $("#id_lugar_nacimiento").empty();
                $.each($.parseJSON(data), function(key, value) {
                   console.log("Data", value)
                   console.log("data", value[4])
                   html = "<option value="+value[4]+">"+value[1]+" - "+value[5]+"</option>";
                   $("#id_lugar_nacimiento").append(html);

                });

            }
        })
      };
