console.log("Navbar.js loaded");

document.querySelector('#search-input').addEventListener('input', function() {

    const query = this.value;
    const resultsDiv = document.querySelector('#search-results');
    resultsDiv.innerHTML = '';

    if (!query) {
        resultsDiv.style.display = 'none';
        return;
    }

    resultsDiv.style.display = 'block';

    fetch(`/search/?query=${encodeURIComponent(query)}`)
    .then(response => {
        console.log("Fetch response received", response);
        return response.json();
    })
    .then(data => {
        console.log("Data received", data);

        data.forEach(user => {
            const userDiv = document.createElement('div');
            userDiv.className = 'search-results';

            // Make the whole div a clickable link
            userDiv.addEventListener('click', function() {
                window.location.href = `/profile/${user.username}`;
            });

            const userDetailDiv = document.createElement('div');
            userDetailDiv.className = 'user-detail-container';

            const profileImage = document.createElement('img');
            profileImage.src = user.profile__image;
            profileImage.alt = `${user.first_name} ${user.last_name}`;
            profileImage.className = 'profile-avatar';
            userDetailDiv.appendChild(profileImage);

            const userNameDiv = document.createElement('div');
            userNameDiv.className = 'username-container';

            const userLink = document.createElement('a');
            userLink.href = `/profile/${user.username}`;
            const name = document.createTextNode(`${user.first_name} ${user.last_name}`);
            userLink.appendChild(name);
            userNameDiv.appendChild(userLink);

            const username = document.createElement('p');
            username.textContent = `@${user.username}`;
            userNameDiv.appendChild(username);

            userDiv.appendChild(userDetailDiv);
            userDiv.appendChild(userNameDiv);

            resultsDiv.appendChild(userDiv);
        });
    });
});




