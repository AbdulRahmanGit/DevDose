async function registerUser(data) {
    try {
        const response = await fetch('https://llm-email-automation-back.onrender.com/register', { //https://llm-email-automation-back.onrender.com/register
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        }); 

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Registration successful:', result);
        // Handle successful registration, e.g., redirect or show a success message
        alert(result.message);
    } catch (error) {
        console.error('Registration failed:', error);
        // Handle errors, e.g., show an error message
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
