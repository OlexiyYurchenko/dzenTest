$(document).ready(function(){


	function display_form_errors(errors, $form) {
		for (var k in errors) {
			if (k=='captcha'){
				$form.find('[name=captcha_1]').after('<div class="error">' + errors[k] + '</div>');
			}
			$form.find('[name=' + k + ']').after('<div class="error">' + errors[k] + '</div>');
		}
	}

	$('.submit').click(function(event){ 
		event.preventDefault();

		var $form = $(this).parents("form");
		formData = new FormData($form.get(0));

		$.ajax({ 
			url: '/', 
			type: 'POST',
			contentType: false,
			processData: false,
			data: formData, 
			dataType: "json",
			success: function(data) { 
				$form.find('.error').remove();
				if ( data.result == 'success') {
					$(location).attr('href','/');
				}
				else if (data['result'] == 'error') {
                    display_form_errors(data['response'], $form);
                }
			}, 
			error: function(errorThrown){ 
				$form.find('.generic-error').text('Unexpected error, contact support');
			} 
		});  
	}); 

	$('.js-btn_preview').click(function(event){ 
		event.preventDefault();

		var $form = $(this).parents("form");
		formData = new FormData($form.get(0));

		$.ajax({ 

			url: '/preview/', 
			type: 'POST',
			contentType: false,
			processData: false,
			data: formData, 
			dataType: "json",
			success: function(data) { 
				$form.find('.error').remove();
				if ( data.result == 'success') {
					// $(location).attr('href','/');
					console.log(data)
				}
				else if (data['result'] == 'error') {
                    display_form_errors(data['response'], $form);
                }
			}, 
			error: function(errorThrown){ 
				$form.find('.generic-error').text('Unexpected error, contact support');
			} 
		});  
	}); 

	$('.comment__footer-link').click(function(event){ 
		event.preventDefault();
		$('.comment-form-holder.form-reply').fadeOut();
		var parent = $(this).data("parent");
		$(".form-reply[data-open='" + parent + "']").fadeIn(); 

		
	}); 

	$(".iframe").colorbox({iframe:true, width:"380px", height:"320px" });
	

	$('.js-captcha-refresh').click(function (e) {
		e.preventDefault();
		var $form = $(this).parents("form");
		$.getJSON("/captcha/refresh/", function (result) {
			$form.find('.captcha').attr('src', result['image_url']);
			$form.find('#id_captcha_0').val(result['key'])
		});
	});

	$('body').on('click', '.sort-btn', function(e){
		e.preventDefault();
		$('.sort').toggleClass('open');
	});

	$("body").click(function (e) {
		if (!$(e.target).closest($(".sort")).length) {
			$('.sort').removeClass('open');
		}
	});
});

