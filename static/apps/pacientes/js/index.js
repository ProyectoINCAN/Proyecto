 $(document).ready(function() {

    $('#dataTables-example').DataTable({
        responsive: true,
         "language": {
            "lengthMenu": "Mostrar _MENU_   registros",
            "zeroRecords": "No existen registros",
            "info": "Mostrando la página page _PAGE_ de _PAGES_",
            "infoEmpty": "No hay registros disponibles",
            "infoFiltered": " ",
             "paginate": {
                  "previous": "Anterior",
                 "next": "Siguiente"
                }

        }
    });
     //elimamos el search que se encontraba en el extremo derecho
     document.getElementById('dataTables-example_filter').style.display = 'none';



     $('#dataTables-example tfoot th').each( function () {
         var title = $(this).text();
         $(this).html( '<input type="text" placeholder="Ingresar '+title+'" />' );
     } );
     // DataTable
     var otable = $('#dataTables-example').DataTable();

     // Apply the search
     otable.columns().every( function () {

         var that = this;
         $( 'input', this.footer() ).on( 'keyup change', function () {
             if ( that.search() !== this.value ) {
                 that
                     .search( this.value )
                     .draw();
             }
         } );
     } );

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
