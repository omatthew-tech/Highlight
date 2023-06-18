// When the page loads, attach an event listener to the friend request button
window.onload = function() {
    const usernameElement = document.querySelector('.username');
    if (usernameElement) {
        const username = usernameElement.innerText;
        const button = document.getElementById('friend-request-button-' + username);
        if (button) {
            button.addEventListener('click', () => {
                handleFriendRequest(username);
            });
        }
    }
};



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrftoken = getCookie('csrftoken');

function handleFriendRequest(username) {
    let button = document.getElementById('friend-request-button-' + username);

    // disable the button and change the text while the request is being sent
    button.disabled = true;
    button.innerText = 'Sending...';

    // Send the POST request
    fetch(`/send_friend_request/${username}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // handle the response
        if (data.status === 'Friend request sent.' || data.status === 'Friend request already sent.') {
            button.innerText = 'Friend request sent';
            button.disabled = true;
        } else {
            button.innerText = 'Error';
            button.disabled = false;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        button.innerText = 'Error';
        button.disabled = false;
    });
}



function handleFriendRequest(username) {
    let button = document.getElementById('friend-request-button-' + username);

    // disable the button and change the text while the request is being sent
    button.disabled = true;
    button.innerText = 'Sending...';

    // Send the POST request
    fetch(`/send_friend_request/${username}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // handle the response
        if (data.status === 'Friend request sent.' || data.status === 'Friend request already sent.') {
            button.innerText = 'Pending';
            button.disabled = true;
        } else {
            button.innerText = 'Send Friend Request';
            button.disabled = false;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        button.innerText = 'Send Friend Request';
        button.disabled = false;
    });
}

function handleFriendRequestResponse(requestId, action) {
    // Send the POST request
    fetch(`/respond_friend_request/${requestId}/${action}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // handle the response
        if (data.success) {
            let requestElement = document.getElementById('friend-request-' + requestId);
            requestElement.remove();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}














