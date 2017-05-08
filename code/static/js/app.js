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


$("tr > td > input").on('input',
	function(){
		camp = $(this).attr('id');
		camp = camp.split("-");
		camp = camp[1];
		subtotal = 0.00;
		descuentos = 0.00;
		producto_cantidad = parseFloat($('#id_form-' + camp + '-cantidad').val()).toFixed(2);
		producto_precio_unitario = parseFloat($('#id_form-' + camp + '-precio_uni').val()).toFixed(2);
		producto_descuento = parseFloat($('#id_form-' + camp + '-descuento').val()).toFixed(2);
		producto_precio_total = parseFloat((producto_cantidad * producto_precio_unitario) - producto_descuento).toFixed(2);
		if (producto_precio_total)
		{
			$('#id_form-' + camp + '-precio_total').val(producto_precio_total);
			for (var i = 0; i < 10; i++) 
			{
				if ($('#id_form-' + i + '-precio_total').val())
				{
					subtotal = parseFloat(subtotal) + parseFloat($('#id_form-' + i + '-precio_total').val());
					descuentos = parseFloat(descuentos) + parseFloat($('#id_form-' + i + '-descuento').val());
					console.log(i);
				}
			}
			$("#totales-subtotal-sin-imp").html(parseFloat(subtotal).toFixed(2));
			$("#totales-subtotal-14").html(parseFloat(subtotal).toFixed(2));
			$("#totales-subtotal-0").html('0.00');
			$("#totales-descuentos").html(parseFloat(descuentos).toFixed(2));
			$("#totales-ice").html('0.00');
			$("#totales-iva-14").html(parseFloat(subtotal * 0.14).toFixed(2));
			$("#totales-total").html(parseFloat((subtotal - descuentos) + (subtotal * 0.14)).toFixed(2));
		}
	}
);


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