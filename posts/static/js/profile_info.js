var modal = document.getElementById('myModal');

document.getElementById('editBtn').addEventListener('click', function (event) {
    event.preventDefault();
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            document.querySelector('#myModal #modal-body').innerHTML = data.form;
            modal.style.display = 'block'; // I've also replaced document.getElementById('myModal') with modal here

            // The form now exists, so attach the event listener to it
            var form = document.querySelector('#myModal form');
            form.addEventListener('submit', function(event) {
                console.log('Form submitted');
                event.preventDefault();

                var formData = new FormData(form);
                console.log(formData);

                var request = new XMLHttpRequest();
                request.open('POST', '/profile/edit', true);
                request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                request.setRequestHeader('X-CSRFToken', form.querySelector('[name=csrfmiddlewaretoken]').value);

                request.onload = function() {
                    if (this.status == 200) {
                        // Form was processed successfully, hide the modal and reload the page
                        modal.style.display = 'none'; // This is where you got the error before
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
        }
    };
    httpRequest.open('GET', '/profile/edit', true);
    httpRequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    httpRequest.send();
});




