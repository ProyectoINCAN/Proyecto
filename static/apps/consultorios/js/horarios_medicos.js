   console.log("entro", $('#id_tipo_doc').val())

   $(function(){
       if ($('#id_medico').val()==null || $('#id_medico').val()==''){
          $("#editar").hide()
          console.log("hola",  $("#id_tipo_doc").val("CI"))
               setDisabled(false)
       }else{
          setDisabled(true)
       }
   }
   )

   function setDisabled (disabled){
   $('#id_medico').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
   $('#id_cod_departamento').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
   $('#id_dia_semana').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
   $('#id_turno').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
   $('#select2-id_medico-container').prop('tabindex', 1)
   $('#select2-id_cod_departamento-container').prop('tabindex', 2);
   $('#select2-id_dia_semana-container').prop('tabindex', 3);
   $('#select2-id_turno-container').prop('tabindex', 4);
   $('#id_hora_inicio').prop('tabindex', 5);
   $('#id_hora_fin').prop('tabindex', 6);
   $("#id_cantidad").prop('tabindex', 8);
   $("#id_habilitado").prop('tabindex', 9);
   $("#id_cantidad").prop('disabled', disabled)
   $("#id_hora_fin").prop('disabled', disabled)
   $("#id_hora_inicio").prop('disabled', disabled)
   $("#id_habilitado").prop('disabled', disabled);

   }

  $("#editar").click(function(){
      setDisabled(false);
      $('#select2-id_medico-container').focus();
      console.log($(this).prop("tabindex"));
      $("input,span>span>span>span").keyup(function() {
        var currentTabIndex = parseInt($(this).attr("tabindex") );
        console.log("entro", currentTabIndex)
      });
  });

  $("#id_turno").change(function(){

    var turno = $('#id_turno').val();
    var inicio, fin = '00:00'

    if (turno == "M") {
        inicio = '07:00'
        fin = '12:00'
    } else if (turno == "T") {
        inicio = '12:00'
        fin = '17:00'
    } else {
        inicio = '17:00'
        fin = '22:00'
    }

    $('#id_hora_inicio').val(inicio);
    $('#id_hora_fin').val(fin);

  })
