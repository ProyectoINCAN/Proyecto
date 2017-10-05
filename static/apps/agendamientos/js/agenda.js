$(document).ready(function() {
        $('#cancelar').click(function() {
            BootstrapDialog.show({
            title: 'Cancelación de agenda',
            message: 'Seleccione tipo de cancelación',
            draggable: true,
            buttons: [{
                label: 'Siguiente fecha',
                cssClass: 'btn-primary',
                icon: 'fa fa-step-forward',
                  action: function(dialog){
                    dialog.close();
                    var csrftoken = getCookie('csrftoken');
                    console.log("token", csrftoken);
                    $.ajax({
                         type:"POST",
                         url:"{% url 'agendamientos:agenda_cancelar' agenda.id %}",
                         data: {
                                'tipo': 2,
                                'csrfmiddlewaretoken': csrftoken
                                },
                         success: function(data){
                            console.log("llega al success");
                            console.log("data", data );
                            console.log("data", $.parseJSON(data)[0].pk );
                            window.location="/agendamientos/agenda/"+$.parseJSON(data)[0].pk;
                         }
                    });
                    return false;
                }
            }, {
                label: 'Última fecha',
                //label: 'Cancelar',
                // no title as it is optional
                cssClass: 'btn-primary',
                icon: 'fa fa-fast-forward',
                action: function(dialog){
                    dialog.close();
                    var csrftoken = getCookie('csrftoken');
                    $.ajax({
                         type:"POST",
                         url:"{% url 'agendamientos:agenda_cancelar' agenda.id %}",
                         data: {
                                'tipo': 1,
                                'csrfmiddlewaretoken': csrftoken
                                },
                         success: function(data){
                            console.log("llega al success");
                            console.log("data", data );
                            console.log("data", $.parseJSON(data)[0].pk );
                            window.location="/agendamientos/agenda/"+$.parseJSON(data)[0].pk;
                         }
                    });
                    return false;
                }
            }, ]
        });

        }
    );

});

   $("#medico_id").change(function () {
      var medico = $(this).val()
      $.ajax({
        url: '/consultorios/medico_especialidad/'+medico,
        data: {
          'medico': medico
        },
        dataType: 'json',
        success: function (data) {
            $("#id_especialidad").empty();
            $.each($.parseJSON(data), function( key, value ) {
              html = "<option value="+value['pk']+">"+value['fields'].nombre+"</option>";
              $("#id_especialidad").append(html);
              actualizarTurno(medico)

            });
        }
      });
   });


   var actualizarTurno = function(medico){
        $.ajax({
            url: '/consultorios/medico_turno/'+medico,
            data: {
              'medico': medico
            },
            dataType: 'json',

            success: function(data){
                var cantidad =0;
                $("#id_turno").empty();
                $.each($.parseJSON(data), function(key, value) {
                   console.log("Data", value);
                   html = "<option value="+value[0]+">"+value[1]+"</option>";
                   $("#id_turno").append(html);
                   cantidad = value[3];
//                   $("#id_cantidad").val(value[3]).disabled = true;
                });
//                $("#id_cantidad").val(cantidad).disabled = true;

                var turno = $("#id_turno").val();
                actualizarHorario(medico, turno);


            }
        })
      };


      var actualizarHorario = function(medico, turno){
//        var csrftoken = getCookie('csrftoken');
        $.ajax({
//            type:'POST',
            url: '/consultorios/horario_medico/',

            data: {
              'medico': medico,
              'turno':turno,
//              'csrfmiddlewaretoken':csrftoken,
            },
            dataType: 'json',
            success: function(data){
                $("#id_cantidad").empty();
                $.each($.parseJSON(data), function(key, value) {
                   console.log("Data", value);
                   console.log("data", key);
                   html = "<option value="+value[0]+">"+value[1]+"</option>";
//                   $("#id_cantidad").append(html);
//                   var turno = $("#id_turno").val()
//                   actualizarHorario(medico, turno)
//                   $("#id_cantidad").val(value[3]).disabled = true;
                });

            }
        })
      };
