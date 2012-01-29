/* Form validation and submission stuff. */

function init_form() {
  // Reset the form whenever the modal is shown.
  $('#modal-from-dom').bind('show', function() {
    reset_form();
  });
  $('#modal-from-dom').bind('shown', function() {
    $('input#name').focus();
  });

  $('.submit').click(handle_form_submit);
  $('.dismiss').click(function() {
    $('#modal-from-dom').modal('hide');
  });
}

function reset_form() {
  $('.footer-section').hide();
  $('#submit_pre').show();
  $('.disable-on-submit').removeAttr('disabled');
}

function handle_form_submit() {
  var name = $('input#name').val();
  var email = $('input#email').val();
  var which = $('select#which').val();
  var guests = $('select#guests').val();
  if (which == "no") {
    guests = "0";
  }

  if (!validate_form(name, email, guests)) {
    return false;
  }
  
  $('.disable-on-submit').attr('disabled', 'disabled');
  
  // Wrap it all up and submit it.
  var formData = 'name=' + name + '&email=' + email
      + '&which=' + which + '&guests=' + guests;
  $.ajax({
    type: "POST",
    url: "/rsvp",
    data: formData,
    success: function() {
      $('.footer-section').hide();
      if (guests == "0") {
        $('#submit_success_no').show();
      } else {
        $('#submit_success_yes').show();
      }
    },
    error: function() {
      $('.footer-section').hide();
      $('#submit_error').show();
      $('.disable-on-submit').removeAttr('disabled');
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