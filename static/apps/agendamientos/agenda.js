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