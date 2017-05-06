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


/*$("#cli_upd").click(
    function(){
        $.ajax({
		url: "/facturacion",
		method: "POST",
		data: { 
			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
			client_type: 'update',
			client_ruc: $("#id_ruc").val(),
			client_firstname: $("#id_firstname").val(),
			client_lastname: $("#id_lastname").val(),
			client_phone: $("#id_phone").val(),
			client_email: $("#id_email").val(),
			},
		// dataType: "json",
		})
		.done(function( data ) {
			console.log(data);
		});
});*/


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