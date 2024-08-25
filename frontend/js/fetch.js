// Function to show and hide the loading indicator
function toggleLoading(show) {
    const loadingBar = document.getElementById('loading-bar');
    if (loadingBar) {
        if (show) {
            loadingBar.classList.add('show'); // Add class to show the spinner
        } else {
            loadingBar.classList.remove('show'); // Remove class to hide the spinner
        }
    }
}

// Function to fetch user details
async function fetchUserDetails(email) {
    toggleLoading(true); // Show loading indicator

    try {
        const response = await fetch(`https://llm-email-automation-back.onrender.com/fetch-details?email=${encodeURIComponent(email)}`, {
            method: 'GET',
        });

        if (!response.ok) {
            if (response.status === 404){
                throw new Error("User Not Found")
            }
            else{
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
    }

        return await response.json();
    } catch (error) {
        if (error.message ===  'User Not Found'){
            console.error("User Not Found")
            alert('User Not Registered')
        }
        else{
        console.error('Fetch request failed:', error);
        alert('Request failed. Please try again.');
        }
        throw error; // Re-throw the error for further handling
    } finally {
        toggleLoading(false); // Hide loading indicator
    }
}

// Event listener for the fetch details form
document.addEventListener('DOMContentLoaded', () => {
    const fetchDetailsForm = document.getElementById('fetch-details-form');

    if (fetchDetailsForm) {
        fetchDetailsForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const userEmail = fetchDetailsForm.querySelector('#email').value;
            try {
                const result = await fetchUserDetails(userEmail);
                const detailsResponse = document.getElementById('details-response');
                detailsResponse.innerHTML = `
                    <h3>User Details:</h3>
                    <p><strong>Name:</strong> ${result.name}</p>
                    <p><strong>Language:</strong> ${result.language}</p>
                    <p><strong>Difficulty:</strong> ${result.difficulty}</p>`;
            } catch (error) {
                console.error('Failed to fetch details:', error);
            }
        });
    } else {
        console.error('Form with ID "fetch-details-form" not found.');
    }
});
