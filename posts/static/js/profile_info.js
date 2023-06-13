// Add this code to handle the friend request button and the friends icon
window.onload = function() {
    fetch('{% url 'check_friendship' user.id %}')
        .then(response => response.json())
        .then(data => {
            let button = document.getElementById('friend-request-button');
            let icon = document.getElementById('friends-icon');
            if (data.is_friend) {
                icon.style.display = 'block';
                button.style.display = 'none';
            } else if (data.request_sent) {
                button.textContent = 'Friend request pending';
                button.disabled = true;
            } else {
                button.textContent = 'Send friend request';
                button.disabled = false;
            }
        });
};

function handleFriendRequest() {
    let button = document.getElementById('friend-request-button');
    button.textContent = 'Sending...';
    button.disabled = true;
    fetch('{% url 'send_friend_request' user.id %}', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                button.textContent = 'Friend request sent';
            } else {
                button.textContent = 'Error';
            }
        });
}





