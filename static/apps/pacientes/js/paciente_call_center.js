   console.log("entro", $('#id_tipo_doc').val())

   $(function(){
       if ($('#id_tipo_doc').val()==null || $('#id_tipo_doc').val()==''){
          $("#id_tipo_doc").val("CI");
               setDisabled(false)
       }else{
          setDisabled(true)
       }

   }
   )

   function setDisabled (disabled){
   $('#id_tipo_doc').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
           $('#id_nacionalidad').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
           $('#id_lugar_nacimiento').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
           $('#id_distrito').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
           $('#id_sexo').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
           $('#id_estado_civil').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
           $('#id_tipo').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
           $('#id_etnia').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
           $('#select2-id_tipo_doc-container').prop('tabindex', 1);
           $('#id_nro_doc').prop('tabindex', 2);
           $('#id_nombres').prop('tabindex', 3);
           $('#id_apellidos').prop('tabindex', 4);
           $('#id_fecha_nacimiento').prop('tabindex', 5);
           $('#select2-id_nacionalidad-container').prop('tabindex', 6);
           $('#select2-id_lugar_nacimiento-container').prop('tabindex', 7);
           $('#select2-id_distrito-container').prop('tabindex', 8);
           $('#select2-id_sexo-container').prop('tabindex', 9);
           $('#select2-id_estado_civil-container').prop('tabindex', 10);
           $('#select2-id_tipo-container').prop('tabindex', 11);
           $('#id_numero').prop('tabindex', 12);
           $('#select2-id_etnia-container').prop('tabindex', 13);
           $("#id_nro_doc").prop('disabled', disabled);
           $("#id_nombres").prop('disabled', disabled);
           $("#id_apellidos").prop('disabled', disabled);
           $("#id_fecha_nacimiento").prop('disabled', disabled);
           $("#id_numero").prop('disabled', disabled);

   }


   $("#id_tipo_doc").change(function () {
     var tipo_doc = $(this).val();
     console.log("entro", tipo_doc)
      if(tipo_doc=='NP' || tipo_doc=='NT' || tipo_doc=='NSC'){
            document.getElementById("id_nro_doc").disabled = true;
      }else{
            document.getElementById("id_nro_doc").disabled = false;
      }
  }),

  $("#editar").click(function(){
      setDisabled(false);
      $('#select2-id_tipo_doc-container').focus();
      console.log($(this).prop("tabindex"));
  $("input,span>span>span>span").keyup(function() {
  var currentTabIndex = parseInt($(this).attr("tabindex") );
    console.log("entro", currentTabIndex)

});
  })
