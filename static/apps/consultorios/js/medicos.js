   console.log("entro", $('#id_tipo_doc').val())

   $(function(){
       if ($('#id_tipo_doc').val()==null || $('#id_tipo_doc').val()==''){
          console.log("entro")
          $("#id_tipo_doc").val("CI");
          $("#editar").hide()
          console.log("hola",  $("#id_tipo_doc").val("CI"))
               setDisabled(false)
       }else{
          setDisabled(true)
       }

       var table= $('#dataTables-horarios').DataTable({
         responsive: true,
         searching: false,
         ordering: false,
         lengthChange: false,
         "language": {
             "lengthMenu": "Mostrar _MENU_   registros",
             "zeroRecords": "No existen registros",
             "info": "Mostrando la página _PAGE_ de _PAGES_",
             "infoEmpty": "No hay registros disponibles",
             "infoFiltered": " ",
             "sSearch": "Buscar:",
             "paginate": {
                 "previous": "Anterior",
                 "next": "Siguiente"
             }

         }
     });

   }
   )

   function setDisabled (disabled){
        $('#id_especialidad').removeAttr('tabindex');
   $('#id_tipo_doc').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
   $('#id_nacionalidad').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
   $('#id_lugar_nacimiento').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
   $('#id_sexo').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
   $('#id_etnia').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
   $('#id_estado_civil').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
   $('#id_etnia').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
   $('#id_especialidad').select2({ placeholder:"Seleccione una opción", allowClear: true,disabled:disabled});
   $('#select2-tipo_doc-container').prop('tabindex', 1);
   $('#id_nro_doc').prop('tabindex', 2);
   $('#id_nombres').prop('tabindex', 3);
   $('#id_apellidos').prop('tabindex', 4);
   $('#id_nro_registro_profesional').prop('tabindex', 5);
   $('#select2-id_sexo-container').prop('tabindex', 6);
   $('#select2-id_nacionalidad-container').prop('tabindex', 7);
   $('#id_fecha_nacimiento').prop('tabindex', 8);
   $('#select2-id_lugar_nacimiento-container').prop('tabindex', 9);
   $('#select2-id_estado_civil-container').prop('tabindex', 10);
   $('#id_direccion').prop('tabindex', 11);
   $('#id_telefono').prop('tabindex', 12);
   $('#id_email').prop('tabindex', 13);
   $('#select2-id_especialidad-container').prop('tabindex', 14);
   $("#id_nro_doc").prop('disabled', disabled);
   $("#id_nombres").prop('disabled', disabled);
   $("#id_apellidos").prop('disabled', disabled);
   $("#id_direccion").prop('disabled', disabled);
   $("#id_email").prop('disabled', disabled);
   $("#id_telefono").prop('disabled', disabled);
   $("#id_nro_registro_profesional").prop('disabled', disabled);
   $("#id_fecha_nacimiento").prop('disabled', disabled);
   $("#id_habilitado").prop('disabled', disabled);
   $("#guardar").prop('disabled', disabled);

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
