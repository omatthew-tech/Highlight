// Get the modal
var modal = document.getElementById('myModal');

// Get the <span> element that closes the modal
var span = document.getElementsByClassName('close')[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = 'none';
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = 'none';
  }
}

// Get the form and add an event listener for form submission
var form = document.querySelector('#myModal form');
form.addEventListener('submit', function(event) {
    console.log('Form submitted');
  event.preventDefault();
  
  var formData = new FormData(form);
  console.log(formData);  // Add this line

  var request = new XMLHttpRequest();
  request.open('POST', '/profile/edit', true);
  request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  request.setRequestHeader('X-CSRFToken', form.querySelector('[name=csrfmiddlewaretoken]').value);

  request.onload = function() {
    if (this.status == 200) {
      // Form was processed successfully, hide the modal and reload the page
      modal.style.display = 'none';
      location.reload();
    } else {
      // Error processing form, display an error message
      console.error('Form processing error:', this.responseText);
    }
  };

  request.onerror = function() {
    // There was a connection error of some sort
    console.error('Connection error');
  };

  request.send(formData);
});




