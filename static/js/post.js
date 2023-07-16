function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function likeButtonHandler() {
    const postId = this.dataset.id;
    this.disabled = true;  // disable button
    const postDiv = this.closest('.post'); // get the closest parent div with class 'post'
    fetch(`/like/${postId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        this.textContent = data.isLiked ? 'Unlike' : 'Like';
        this.disabled = false;  // enable button
        if (data.isLiked) {
            postDiv.style.display = 'none'; // hide the post if it is liked
        }
    });
}

document.querySelectorAll('.like-button:not(.event-bound)').forEach(button => {
    button.classList.add('event-bound');
    button.addEventListener('click', likeButtonHandler);  // Add the event listener
});







