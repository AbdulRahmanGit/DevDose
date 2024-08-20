document.addEventListener('DOMContentLoaded', () => {
    const deleteForm = document.getElementById('submit-otp-form');
    const loadingBar = document.getElementById('loading-bar');
    const storedEmail = sessionStorage.getItem('email');

    if (deleteForm && loadingBar) {
        deleteForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Show loading bar
            loadingBar.classList.add('loading-bar-active');

            const data = {
                otp: deleteForm.querySelector('#otp').value,
                email: storedEmail
            };

            console.log('Confirming deletion with data:', data);
            try {
                const response = await fetch('https://llm-email-automation-back.onrender.com/delete'|| 'http://localhost:8000/delete', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });

                if (response.ok) {
                    const result = await response.json();
                    alert(result.message);
                    // Redirect or display a success message as needed
                    window.location.href = '/frontend'; // Redirect to home or another page
                } else {
                    const errorData = await response.json();
                    alert(errorData.detail || 'OTP verification failed'); // Use detail if returned by backend
                }
            } catch (error) {
                console.error('OTP verification failed:', error);
                alert('OTP verification failed. Please try again.');
            } finally {
                // Hide loading bar
                setTimeout(() => loadingBar.classList.remove('loading-bar-active'), 3000); // Adjust timing as needed
            }
        });
    } else {
        console.error('Form with ID "submit-otp-form" or loading bar with ID "loading-bar" not found.');
    }
});
