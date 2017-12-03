$('button').click(function(e) {
    e.preventDefault();
    console.log("handle click event...");
    //var paciente = $("#paciente_id").val();
    var paciente = $(this).val();
    var consulta = $("#consulta_id").val();
    console.log("paciente", paciente, "consulta", consulta);
    var url = "/consultorios/consulta/"+consulta+"/detalles/agregar/";
    var data = {
      'consulta_id': consulta,
      'paciente_id': paciente,
      'csrfmiddlewaretoken': getCookie('csrftoken')

    };
    $.post(
      url,
      data,
      function(data){
        console.log("llega al success...");
        if (data.success) {
            window.location="/consultorios/consulta/"+consulta+"/detalles/";
        }
      }
    );
  });