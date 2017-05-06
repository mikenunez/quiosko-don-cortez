$("form").keypress(
    function(event){
     if (event.which == '13') {
        event.preventDefault();
      }
});


$("#id_ruc").keypress(
    function(event){
     if (event.which == '13') {
        popu_client($(this).val());
      }
});


function popu_client(v) {
	$.ajax({
		url: "/facturacion",
		method: "POST",
		data: { 
			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
			cli_val: v },
		dataType: "json",
		})
		.done(function( data ) {
			$("#id_firstname").val(data.nombre);
			$("#id_lastname").val(data.apellido);
			$("#id_phone").val(data.phone);
			$("#id_email").val(data.email);
		});
}