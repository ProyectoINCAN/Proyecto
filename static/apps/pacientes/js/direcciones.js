   $( document ).ready(function() {
       $('#create').click(function(){
          $('#modalDireccion').modal('show');
       })
   })

   $("#id_departamento").change(function () {
      console.log( $(this).val() );
      var departamento = $(this).val()
      console.log("departamento", departamento)

//      $.ajax({
//        url: '/principal/distrito/'+departamento,
//        data: {
//          'departamento': departamento
//        },
//        dataType: 'json',
//        success: function (data) {
//
//          if (data.distrito) {
//            console.log('data', data.distrito)
//          }
//        }
//      });
    $.ajax({url: '/principal/distrito/'+departamento, type: 'GET',
    success:function(result){
        console.log("entro")
    }
    });
   });