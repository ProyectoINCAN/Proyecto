   $("#tipo_doc").change(function () {
     var tipo_doc = $(this).val();
      if(tipo_doc=='NP' || tipo_doc=='NT' || tipo_doc=='NSC'){
            document.getElementById("id_nro_doc").disabled = true;
      }else{
            document.getElementById("id_nro_doc").disabled = false;
      }
  })


$("input[name='nro_doc']").focus(function(){
this.select();
});
// fix for CHROME
//$("input[name='nro_doc']").mouseup(function(e){
//e.preventDefault();
//});

