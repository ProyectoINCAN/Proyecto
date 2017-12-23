//$(document).ready(function() {
$('#fecha_desde').datepicker({dateFormat: 'dd/mm/yy'});
$('#fecha_hasta').datepicker({dateFormat: 'dd/mm/yy'});

$('#cancelar').click(function () {
    console.log("llega a cancelar")
    var agenda_id = $("#agenda_id").val();
    var origen = $("#origen").val();

    console.log(agenda_id, origen);

    BootstrapDialog.show({
      title: 'Cancelación de agenda',
      message: 'Seleccione tipo de cancelación',
      draggable: true,
      buttons: [{
        label: 'Siguiente fecha',
        cssClass: 'btn-primary',
        icon: 'fa fa-step-forward',
        action: function (dialog) {
          dialog.close();
          var csrftoken = getCookie('csrftoken');
          console.log("token", csrftoken);
          $.ajax({
            type: "POST",
            //url:"{% url 'agendamientos:agenda_cancelar' agenda.id %}",
            url: "/agendamientos/agenda/" + agenda_id + "/" + origen + "/cancelar",
            data: {
              'tipo': 2,
              'csrfmiddlewaretoken': csrftoken
            },
            success: function (data) {
              console.log("llega al success");
              console.log("data", data);
              console.log("data", $.parseJSON(data)[0].pk, $.parseJSON(data)[1]);
              window.location = "/agendamientos/agenda/" + $.parseJSON(data)[0].pk + "/" + origen + "/";
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
        action: function (dialog) {
          dialog.close();
          var csrftoken = getCookie('csrftoken');
          $.ajax({
            type: "POST",
            url: "/agendamientos/agenda/" + agenda_id + "/" + origen + "/cancelar",
            data: {
              'tipo': 1,
              'csrfmiddlewaretoken': csrftoken
            },
            success: function (data) {
              console.log("llega al success");
              console.log("data", data);
              console.log("data", $.parseJSON(data)[0].pk);
              window.location = "/agendamientos/agenda/" + $.parseJSON(data)[0].pk + "/" + origen + "/";
            }
          });
          return false;
        }
      },]
    });

  }
);


$('#consultas').click(function () {
    var agenda_id = $("#agenda_id").val();
    var origen = $("#origen").val();

    console.log(agenda_id, origen);

    BootstrapDialog.show({
      title: 'Pasar agenda a Consultorio',
      message: '¿Está seguro de que desea pasar la agenda a consultorio?',
      draggable: true,
      buttons: [{
        label: 'No',
        //cssClass: 'btn-primary',
        icon: 'fa fa-times',
        action: function (dialog) {
          dialog.close();
          return false;
        }
      }, {
        label: 'Sí',
        //label: 'Cancelar',
        // no title as it is optional
        cssClass: 'btn-primary',
        icon: 'fa fa-check',
        action: function (dialog) {
          dialog.close();
          var csrftoken = getCookie('csrftoken');
          $.ajax({
            type: "POST",
            url: "/consultorios/consulta/create/" + agenda_id + "",
            data: {
              'origen': origen,
              'csrfmiddlewaretoken': csrftoken
            },
            success: function (data) {
              console.log("llega al success");
              console.log("data", data);
              window.location = data;
            }
          });
          return false;
        }
      },]
    });

  }
);

//}
//);

$("#buscar").click(function () {
  $.ajax({
      url: '/agendamientos/agenda_fecha/',
      data: {
        'fecha_desde': $('#fecha_desde'),
        'fecha_hasta': $('#fecha_hasta'),
        'especialidad': $('#especialidades').val()
      },
      success: function () {
        console.log('regreso')
      }
    }
  )
  return;
});


$("#medico_id").change(function () {
  var medico = $(this).val();

  $.ajax({
    url: '/consultorios/medico_especialidad/' + medico,
    data: {
      'medico': medico
    },
    dataType: 'json',
    success: function (data) {
      $("#id_especialidad").empty();
      $.each($.parseJSON(data), function (key, value) {
        html = "<option value=" + value['pk'] + ">" + value['fields'].nombre + "</option>";
        $("#id_especialidad").append(html);
        actualizarTurno(medico)

      });
    }
  });


});


var actualizarTurno = function (medico) {
  $.ajax({
    url: '/consultorios/medico_turno/' + medico,
    data: {
      'medico': medico
    },
    dataType: 'json',

    success: function (data) {
      var cantidad = 0;
      $("#id_turno").empty();
      $.each($.parseJSON(data), function (key, value) {
        console.log("Data", value);
        html = "<option value=" + value[0] + ">" + value[1] + "</option>";
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
//
$("#id_turno").change(function () {
  var medico = $("#medico_id").val();
  var turno = $("#id_turno").val();
  console.log("lilian")
  actualizarHorario(medico, turno)
})


var actualizarHorario = function (medico, turno) {
  $.ajax({
    url: '/consultorios/horario_medico/' + medico + '/' + turno,
    data: {
      'medico': medico,
      'turno': turno,
    },
    dataType: 'json',
    success: function (data) {
      $("#id_cantidad").empty();
      $.each($.parseJSON(data), function (key, value) {
        console.log("Data", value);
        console.log("data", key);
        $("#id_cantidad").val(value['fields'].cantidad);
      });

    }
  })
};

$(document).ready(function () {
  $('#create').click(function () {
    console.log("entro")
    $('#modalAgendaDetalle').modal('show');
  })
})


$("#limpiar").click(function () {
  console.log("prueba")
  $("#id_especialidad").val("");
  $("#id_medico").val("");
  $("#id_turno").val("");
  $("#buscar")
});

$("#limpiar_filtros").click(function () {
  console.log("prueba")
  var date = new Date();
  var primerDia = 01 + "/" + (date.getMonth() + 1) + "/" + date.getFullYear()
  var fechaActual = date.getDate() + "/" + (date.getMonth() + 1) + "/" + date.getFullYear()
  $("#fecha_desde").val(primerDia)
  $("#fecha_hasta").val(fechaActual)
  $("#id_especialidad").val("")
  $("#id_medico").val("");
  $("#id_estado").val("");
  $("#buscar")
});

