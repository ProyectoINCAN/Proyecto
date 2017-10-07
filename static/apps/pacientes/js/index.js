 $(document).ready(function() {


     //$('#dataTables-example tfoot tr ').appendTo('#dataTables-example thead');

     $("#limpiar").click(function () {
                 $("#id_paciente").val('');
                 $("#paciente_label").val('');

     });
            var id_paciente;
     $(".paciente_label").autocomplete({
         source: "/pacientes/autocomplete_nombres/",
         minLength : 1,
         select: function (event, ui) {
             id_paciente = ui.item.id;
             $("#id_paciente").val(id_paciente);
             $("#paciente_label").val(ui.item.label);

         }

     });
} );
