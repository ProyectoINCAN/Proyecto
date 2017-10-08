 $(document).ready(function() {
     $('#dataTables-example').DataTable({
         responsive: true,
         "language": {
             "lengthMenu": "Mostrar _MENU_   registros",
             "zeroRecords": "No existen registros",
             "info": "Mostrando la página page _PAGE_ de _PAGES_",
             "infoEmpty": "No hay registros disponibles",
             "infoFiltered": " ",
             "sSearch": "Buscar:",
             "paginate": {
                 "previous": "Anterior",
                 "next": "Siguiente"
             }

         }
     });
     //elimamos el search que se encontraba en el extremo derecho
     //document.getElementById('dataTables-example_filter').style.display = 'none';





 });