
var modal;

function abrir_modal(url, titulo)
{
    modal = $('#popup_pacientes').dialog(
    {
        title: titulo,
        modal: true,
        width: 650,
        height: 500,
        resizable: false
    }).dialog('open').load(url)
}

function cerrar_modal()
{
    modal.dialog("close");
}

