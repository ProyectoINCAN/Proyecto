
var modal;

function abrir_modal(url)
{
     $('#popup').load(url, function()
     {
            $(this).modal('show');
     });
        return false;
}

function cerrar_modal()
{
    $('#popup').modal('hide');
        return false;
}

function reloadPaginaConsultaPaciente(id_detalle, id_tab)
{
    window.location = "/consultorios/consulta/detalle/"+id_detalle+"/?ir_a_tab="+id_tab;
}

