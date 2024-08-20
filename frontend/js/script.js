document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registration-form');
    const loadingBar = document.getElementById('loading-bar'); // Assuming you have a loading bar

    if (form && loadingBar) {
        form.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent the default form submission

            const data = {
                name: form.querySelector('#name').value,
                email: form.querySelector('#email').value,
                language: form.querySelector('#language').value,
                difficulty: form.querySelector('#difficulty').value
            };

            console.log('Submitting registration data:', data);

            // Show loading bar
            loadingBar.classList.add('loading-bar-active'); // Assuming this class expands the bar

            try {
                const response = await registerUser(data);
                if (response.ok) {
                    const result = await response.json();
                    console.log('Registration successful:', result);
                    alert(result.message);
                    window.location.href = 'https://devdoses-worker.onrender.com/'; // Redirect after success
                } else {
                    const errorData = await response.json();
                    alert(errorData.detail || 'Registration failed');
                }
            } catch (error) {
                console.error('Registration failed:', error);
                alert('Registration failed. Please try again.');
            } finally {
                // Hide loading bar after a delay or when the operation completes
                setTimeout(() => loadingBar.classList.remove('loading-bar-active'), 3000);
            }
        });
    } else {
        console.error('Form with ID "registration-form" or loading bar with ID "loading-bar" not found.');
    }
});

async function registerUser(data) {
    return fetch('https://llm-email-automation-back.onrender.com/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
}
