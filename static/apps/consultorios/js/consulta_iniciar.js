$( document ).ready(function() {
    var centesimas = 0;
    var segundos = 0;
    var minutos = 0;
    var horas = 0;
    function inicio () {
      control = setInterval(cronometro,10);
      document.getElementById("inicio").disabled = true;
      document.getElementById("parar").disabled = false;
      document.getElementById("continuar").disabled = true;
      document.getElementById("reinicio").disabled = false;
    }
    function parar () {
      clearInterval(control);
      document.getElementById("parar").disabled = true;
      document.getElementById("continuar").disabled = false;
    }
    function reinicio () {
      clearInterval(control);
      centesimas = 0;
      segundos = 0;
      minutos = 0;
      horas = 0;
      Centesimas.innerHTML = ":00";
      Segundos.innerHTML = ":00";
      Minutos.innerHTML = ":00";
      Horas.innerHTML = "00";
      document.getElementById("inicio").disabled = false;
      document.getElementById("parar").disabled = true;
      document.getElementById("continuar").disabled = true;
      document.getElementById("reinicio").disabled = true;
    }
    function cronometro () {
      if (centesimas < 99) {
        centesimas++;
        if (centesimas < 10) { centesimas = "0"+centesimas }
        Centesimas.innerHTML = ":"+centesimas;
      }
      if (centesimas == 99) {
        centesimas = -1;
      }
      if (centesimas == 0) {
        segundos ++;
        if (segundos < 10) { segundos = "0"+segundos }
        Segundos.innerHTML = ":"+segundos;
      }
      if (segundos == 59) {
        segundos = -1;
      }
      if ( (centesimas == 0)&&(segundos == 0) ) {
        minutos++;
        if (minutos < 10) { minutos = "0"+minutos }
        Minutos.innerHTML = ":"+minutos;
      }
      if (minutos == 59) {
        minutos = -1;
      }
      if ( (centesimas == 0)&&(segundos == 0)&&(minutos == 0) ) {
        horas ++;
        if (horas < 10) { horas = "0"+horas }
        Horas.innerHTML = horas;
      }
    }
    });

    $(function(){
        setTimeout(function() {
            console.log("timeout");
        }, 100 ); // <-- tiempo en milisegundos, 1000 =  1 sec
        var toTab = $("#ir_a_tab").val();
        console.log("toTab : ", toTab);
        $(toTab).click();
        /*window.history.replaceState({}, "", "/"+window.location.href.substring(window.location.href.lastIndexOf('/') + 1).split("?")[0]);*/
        window.history.replaceState(null, null, window.location.pathname.split("?")[0]);
    })

$('#finalizar').click(function() {
    var $this = this;
    var detalle_id = $("#detalle_id").val();

    console.log(detalle_id);

    BootstrapDialog.show({
    title: 'Finalizar consulta',
    message: '¿Desea finalizar la consulta? Este proceso es irreversible.',
    draggable: true,
    buttons: [{
        label: 'Finalizar',
        cssClass: 'btn-primary',
        icon: 'fa fa-check',
        action: function(dialog){
            dialog.close();
            var csrftoken = getCookie('csrftoken');
            console.log("token", csrftoken);
            $.ajax({
                 type:"POST",
                 url:"/consultorios/consulta/detalle/finalizar/",
                 data: {
                        'consulta_det_id': detalle_id,
                        'csrfmiddlewaretoken': csrftoken
                        },
                 success: function(data){
                    console.log("llega al success");
                    console.log("data", data );
                    window.location="/consultorios/consulta/detalle/"+detalle_id+"/resumen/";
                 }
            });
            return false;
        }
    }, {
        label: 'Cancelar',
        // no title as it is optional
        cssClass: 'btn-default',
        icon: 'fa fa-times',
        action: function(dialog){
            dialog.close();
            return false;
        }
    },
    ]
    });

    }

);


$('#cancelar').click(function() {
    var $this = this;
    var detalle_id = $("#detalle_id").val();

    console.log(detalle_id);

    BootstrapDialog.show({
    type: BootstrapDialog.TYPE_DANGER,
    title: 'Cancelar consulta',
    message: '¿Desea cancelar la consulta?',
    draggable: true,
    buttons: [{
        label: 'Sí',
        cssClass: 'btn-danger',
        icon: 'fa fa-check',
        action: function(dialog){
            dialog.close();
            var csrftoken = getCookie('csrftoken');
            console.log("token", csrftoken);
            $.ajax({
                 type:"POST",
                 url:"/consultorios/consulta/detalle/cancelar/",
                 data: {
                        'consulta_det_id': detalle_id,
                        'csrfmiddlewaretoken': csrftoken
                        },
                 success: function(data){
                    console.log("llega al success");
                    console.log("data", data );
                    window.location="/consultorios/consulta/detalle/"+detalle_id+"/resumen/";
                 }
            });
            return false;
        }
    }, {
        label: 'No',
        // no title as it is optional
        cssClass: 'btn-default',
        icon: 'fa fa-times',
        action: function(dialog){
            dialog.close();
            return false;
        }
    }, {
        label: 'Volver a pendientes',
        // no title as it is optional
        cssClass: 'btn-default',
        icon: 'fa fa-reply',
        action: function(dialog){
            dialog.close();
            var csrftoken = getCookie('csrftoken');
            var consulta_id = $('#consulta_id').val();
            console.log("token", csrftoken);
            $.ajax({
                 type:"POST",
                 url:"/consultorios/consulta/detalle/volver/",
                 data: {
                        'consulta_det_id': detalle_id,
                        'csrfmiddlewaretoken': csrftoken
                        },
                 success: function(data){
                    console.log("llega al success de volver");
                    window.location="/consultorios/consulta/"+consulta_id+"/detalles/";
                 }
            });
            return false;
        }
    },
    ]
    });

    }

);

