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


     $('#dataTables-example tfoot th').each(function () {
         var title = $(this).text();
         $(this).html('<input type="text" placeholder="Ingresar ' + title + '" />');
     });
     // DataTable
     var otable = $('#dataTables-example').DataTable();

     // Apply the search
     otable.columns().every(function () {

         var that = this;
         $('input', this.footer()).on('keyup change', function () {
             if (that.search() !== this.value) {
                 that
                     .search(this.value)
                     .draw();
             }
         });
     });

 });