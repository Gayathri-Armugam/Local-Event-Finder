// You can add extra JavaScript for advanced functionality or animations
// Example for handling modal logic (optional)

function viewEventDetails(eventId) {
    // Open a modal or redirect to the event detail page.
    window.location.href = `/events/${eventId}/`;  // Redirect to event detail page
}

function removeFromInterested(eventId) {
    fetch(`/remove-interested/${eventId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Assuming you're using CSRF tokens
        },
        body: JSON.stringify({ event_id: eventId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove event card from DOM or refresh the list
            document.querySelector(`#event-${eventId}`).remove();
        } else {
            alert('An error occurred while removing the event.');
        }
    });
}

// Helper function to get CSRF token (if using Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
