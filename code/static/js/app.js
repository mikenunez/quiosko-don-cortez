// FUNTIONS
var totals = [[],[],[],[],[],[],[],[],[],[]];
function makethemath(u){
	camp = u;
	camp = camp.split("-");
	camp = camp[1];
	subtotal = 0.00;
	descuentos = 0.00;
	iva = 0.00;
	total = 0.00;
	prod_cant = parseInt($('#id_form-' + camp + '-cantidad').val(), 10);
	prod_p_u = parseFloat($('#id_form-' + camp + '-precio_uni').val()).toFixed(2);
	prod_iva = parseFloat($('#id_form-' + camp + '-iva').val());
	prod_iva = parseFloat(parseFloat(prod_iva)/100).toFixed(2);
	
	totals[camp][0] = parseFloat(prod_cant * prod_p_u).toFixed(2);
	totals[camp][1]	= parseFloat($('#id_form-' + camp + '-descuento').val()).toFixed(2);
	totals[camp][0] = parseFloat(totals[camp][0]) - parseFloat(totals[camp][1]);
	if (isNaN(prod_iva))
	{
		prod_iva = 0;
	}
	totals[camp][2]	= parseFloat(totals[camp][0]).toFixed(2) * parseFloat(prod_iva).toFixed(2);
	totals[camp][3]	= parseFloat(totals[camp][0]) + parseFloat(totals[camp][2]);
	if (!isNaN(totals[camp][3]))
	{
		$('#id_form-' + camp + '-subtotal').val(parseFloat(totals[camp][0]).toFixed(2));
		for (var i = 0; i < 10; i++)
		{
			if (!isNaN(totals[i][3]))
			{
				subtotal 	= parseFloat(subtotal) + parseFloat(totals[i][0]);
				descuentos 	= parseFloat(descuentos) + parseFloat(totals[i][1]);
				iva 		= parseFloat(iva) + parseFloat(totals[i][2]);
				total 		= parseFloat(total) + parseFloat(totals[i][3]);
			}
		}
		$("#totales-subtotal-sin-imp").html(parseFloat(subtotal).toFixed(2));
		$("#totales-subtotal-14").html(parseFloat(subtotal).toFixed(2));
		$("#totales-subtotal-0").html('0.00');
		$("#totales-descuentos").html(parseFloat(descuentos).toFixed(2));
		$("#totales-ice").html('0.00');
		$("#totales-iva-14").html(parseFloat(iva).toFixed(2));
		$("#id_iva").val(parseFloat(iva).toFixed(2));
		$("#totales-total").html(parseFloat(total).toFixed(2));
	}
}

$("#documento-form").keypress(
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

$("tr > td > select").change(function(){  
	var id =  $(this).attr('id')
	id_sel = id.split("-");
	if (id_sel[2]=='producto')
	{
		popu_price(id_sel[1],$(this).val());
	}
});

$("tr > td > input").on('input',function(){ 
	makethemath($(this).attr('id'));
});

$("tr > td > input").on('change',function(){ 
	makethemath($(this).attr('id'));
});

$("#btn-addForm").on('click',function(){ 
	addDetalle($("#id_form-TOTAL_FORMS").val(), function(){
		setTimeout(smartSelect(),200);
	});
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

function popu_price(id,v) {
	$.ajax({
		url: "/facturacion",
		method: "POST",
		data: { 
			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
			prod_pk: v },
		dataType: "json",
		})
		.done(function( data ) {
			$("#id_form-"+id+"-precio_uni").val(data.precio);
			$("#id_form-"+id+"-iva").val(data.iva);
			$("#id_form-"+id+"-iva_code").val(data.iva_code);
			makethemath("a-"+id);
		});
}
	
function smartSelect() {
	$('tbody > tr:last-child > td:nth-child(2) > select').selectpicker({
		"container": "body",
		"liveSearch":"true",
		"width":"100%"
	});
}

var getDrawDetalle = $("tbody>tr:last-child").clone(true);
function addDetalle(t, callback) {
	var total = t;
	var newDetalle = getDrawDetalle.clone(true);
	newDetalle.find(':input').each(function() {
		var name = $(this).prop('name').replace('-' + (total-1) + '-','-' + total + '-');
		var id = 'id_' + name;
		$(this).attr({'name': name, 'id': id});
	});
	newDetalle.find('label').each(function() {
		var newFor = $(this).prop('for').replace('-' + (total-1) + '-','-' + total + '-');
		$(this).attr('for', newFor);
	});
	newDetalle.find('select').each(function() {
		var name = $(this).prop('name').replace('-' + (total-1) + '-','-' + total + '-');
		var id = 'id_' + name;
		$(this).attr({'name': name, 'id': id}).val('');
	});
	total++;
	$('#id_form-TOTAL_FORMS').val(total);
	$("tbody").append(newDetalle);
	getDrawDetalle = newDetalle.clone(true);
	callback();
}

function makethemathAll(forms){
	for (var i = 0; i < forms; i++)
	{
		makethemath("a-"+i);
	}
}

$(document).on('ready',makethemathAll($('#id_form-TOTAL_FORMS').val()));
$(document).on('ready',smartSelect());