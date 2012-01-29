/* Form validation and submission stuff. */

function init_form() {
  $('.submit').click(handle_form_submit);

  // Reinit everything just to be sure whenever the modal is shown.
  $('#modal-from-dom').bind('show', function() {
    init_form();
  });
  $('.dismiss').click(function() {
    $('#modal-from-dom').modal('hide');
  });
  
  $('#submit_pre').show();
  $('#submit_success_yes').hide();
  $('#submit_success_no').hide();
  $('#submit_error').hide();
}

function handle_form_submit() {
  var name = $('input#name').val();
  var email = $('input#email').val();
  var guests = $('select#guests').val();

  if (!validate_form(name, email, guests)) {
    return false;
  }
  
  // Wrap it all up and submit it.
  var formData = 'name=' + name + '&email=' + email + '&guests=' + guests;
  $.ajax({
    type: "POST",
    url: "/rsvp",
    data: formData,
    success: function() {
      $('#submit_pre').hide();
      $('#submit_error').hide();

      if ($('select#guests').val() == "0") {
        $('#submit_success_yes').hide();
        $('#submit_success_no').show();
      } else {
        $('#submit_success_yes').show();
        $('#submit_success_no').hide();
      }
    },
    error: function() {
      $('#submit_pre').hide();
      $('#submit_success_yes').hide();
      $('#submit_success_no').hide();
      $('#submit_error').show();
    },
  });
}

function validate_form(name, email, guests) {
  $('*').removeClass('error');
  
  var success = true;
  if (name == "") {
    $('input#name').addClass('error');
    $('input#name').parents('.clearfix').addClass('error');
    success = false;
  }
  
  if (email == "") {
    $('input#email').addClass('error');
    $('input#email').parents('.clearfix').addClass('error');
    success = false;
  }
  
  return success;
}