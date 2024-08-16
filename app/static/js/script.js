document.addEventListener('DOMContentLoaded', function () {
    const eventForm = document.getElementById('createEventForm');
    const recommendedVenues = document.getElementById('recommendedVenues');

    // Event listener for form submission
    eventForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent form submission

        // Fetch recommended venues based on form data
        fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                eventName: eventForm.eventName.value,
                location: eventForm.location.value,
                date: eventForm.date.value,
                spaceCapacity: eventForm.spaceCapacity.value,
                budget: eventForm.budget.value,
                description: eventForm.description.value
            })
        })
        .then(response => response.json())
        .then(recommendedVenues => {
            // Clear previous recommendations
            recommendedVenues.innerHTML = '';

            // Display recommended venues
            recommendedVenues.forEach(venue => {
                const venueItem = document.createElement('li');
                venueItem.innerHTML = `
                    <h3>${venue['Venue Name']}</h3>
                    <p>Location: ${venue['Location']}</p>
                    <p>Rating: ${venue['Rating']}</p>
                    <p>Overview: ${venue['Overview']}</p>
                `;
                recommendedVenues.appendChild(venueItem);
            });

            // Show recommended venues section
            document.getElementById('recommendedVenuesSection').style.display = 'block';
        })
        .catch(error => console.error('Error fetching recommended venues:', error));
    });

    // Function to submit booking form
    function submitBooking() {
        const bookingForm = document.getElementById('createEventForm');
        bookingForm.action = '/book'; // Set action to book route
        bookingForm.submit();
    }
});

