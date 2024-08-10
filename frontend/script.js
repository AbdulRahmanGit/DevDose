async function registerUser(data) {
    try {
        const response = await fetch('https://llm-email-automation-back.onrender.com/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            // Redirect to /job if registration is successful
            const result = await response.json();
            console.log('Registration successful:', result);
            // Handle successful registration, e.g., redirect or show a success message
            alert(result.message);
            window.location.href = '/job';
        } else {
            const errorData = await response.json();
            alert(errorData.message || 'Registration failed');
        }
    } catch (error) {
        console.error('Registration failed:', error);
        alert('Registration failed. Please try again.');
    }
}

// Example usage:
const form = document.getElementById('registration-form');
form.addEventListener('submit', (event) => {
    event.preventDefault();

    const data = {
        name: form.querySelector('#name').value,
        email: form.querySelector('#email').value,
        language: form.querySelector('#language').value,
        difficulty: form.querySelector('#difficulty').value
    };

    console.log('Submitting data:', data); // Debugging line to check the data being sent
    registerUser(data);
});
