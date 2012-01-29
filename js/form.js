/* Form validation and submission stuff. */

function init_form() {
  $('#button').click(handle_form_submit);
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
      alert("yay!");
    },
    error: function() {
      alert("boo");
    },
  });
}

function validate_form(name, email, guests) {
  $('*').removeClass('error'); // Remove all error classes

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