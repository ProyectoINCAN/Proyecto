   $(function(){
       if ($('#id_nombre').val()==null || $('#id_nombre').val()==''){
          console.log("entro")
          $('#editar').hide();
          setDisabled(false);
       }else{
          setDisabled(true);
       }
   }
   )

   function setDisabled (disabled){
       $('#id_tipificacion').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
       $('#id_forma_farmaceutica').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
       $('#id_nombre').prop('tabindex', 1);
       $('#select2-id_tipificacion-container').prop('tabindex', 2);
       $('#select2-id_forma_farmaceutica-container').prop('tabindex', 3);
       $('#id_nro_lote').prop('tabindex',4);
       $('#id_cantidad').prop('tabindex', 5);
       $('#id_fabricado').prop('tabindex', 6);
       $('#id_vencimiento').prop('tabindex', 7);
       $('#id_habilitado').prop('tabindex', 8);
       $("#id_nombre").prop('disabled', disabled);
       $("#id_nro_lote").prop('disabled', disabled);
       $("#id_cantidad").prop('disabled', disabled);
       $("#id_fabricado").prop('disabled', disabled);
       $("#id_vencimiento").prop('disabled', disabled);
       $("#id_habilitado").prop('disabled', disabled);
   }

  $("#editar").click(function(){
      setDisabled(false);
      $('#select2-id_tipo_doc-container').focus();
      console.log($(this).prop("tabindex"));
  $("input,span>span>span>span").keyup(function() {
  var currentTabIndex = parseInt($(this).attr("tabindex") );
    console.log("entro", currentTabIndex)

});
  })
