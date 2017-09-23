 $(document).ready(function() {
     var valor;
     $("#id_seguro_medico").change(function(){
         valor = $("#id_seguro_medico").val()
         if(valor == 0) {
             document.getElementById('otro_seguro').style.display = 'block';
         }else{
             document.getElementById('otro_seguro').style.display = 'none';
         }

     });
     $("#eventoForm").submit(function(e) {
         var url = this.action; // the script where you handle the form input.
         console.log(url)
         $.ajax({
             type: "POST",
             url: url,
             data: $("#eventoForm").serialize(), // serializes the form's elements.
             success: function(data, status) {
                 console.log('entro');
                 $('#eventoForm').html(data);

             },
             error: function(ajaxContext) {
                 console.log('ok');
                 alert(ajaxContext.responseText);
             },
             done: function (response) {
                 $('#modalSeguro').modal('hide');
                 $('#popup').modal('hide');
             }
         });
         e.preventDefault(); // avoid to execute the actual submit of the form.
     });

     //boton de eliminacion de seguro medico
     $('.btnDeleteSeguro').click(function () {
             var codigo_seguro = $(this).data('id');
                console.log(codigo_direccion)
                $("#paciente_seguro").val(codigo_seguro)
            });



 });