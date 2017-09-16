/**
 * Created by isasiluispy on 11/3/16.
 */

$(function () {
  // $('body').on('show.bs.modal', '#modal-borrar', function () {
  $('#modal-borrar').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var url = button.data('url');
    var nombre = button.data('nombre');
    var modal = $(this);
    var form_delete = $('#form-delete').attr('action', url);

    var titulo = button.data('titulo');
    if (titulo) {
      modal.find('.modal-title').text(titulo);
    }
    else {
      modal.find('.modal-title').text('Borrar ' + nombre);
    }
    modal.find('.modal-body').html('<p>¿ Está seguro ?</p>');

    var desc = button.data('desc_boton');
    if (desc) {
      $('#boton-enviar').html(desc);
    } else {
      $('#boton-enviar').html('Borrar');
    }

  });
});
