document.addEventListener('DOMContentLoaded', () => {
    const deleteForm = document.getElementById('delete-form');
    const loadingBar = document.getElementById('loading-bar');

    if (deleteForm && loadingBar) {
        deleteForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const userEmail = deleteForm.querySelector('#email').value;
            

            // Store values in session storage
            sessionStorage.setItem('email', userEmail);
            

            const data = {
                email: userEmail,
                
            };

            // Show loading bar
            loadingBar.classList.add('loading-bar-active');

            try {
                const response = await fetch('https://llm-email-automation-back.onrender.com/request-delete-otp', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });

                if (response.ok) {
                    const result = await response.json();
                    alert(result.message);
                    // Redirect to OTP verification page
                    window.location.href = '/templates/verify_del.html';
                } else {
                    const errorData = await response.json();
                    alert(errorData.detail || 'Failed to request OTP');
                    console.log(errorData.detail);
                }
            } catch (error) {
                console.error('Failed to request OTP:', error);
                alert('Failed to request OTP. Please try again.');
            } finally {
                // Hide loading bar after a delay or when the operation completes
                setTimeout(() => loadingBar.classList.remove('loading-bar-active'), 3000);
            }
        });
    } else {
        console.error('Form with ID "update-form" or loading bar with ID "loading-bar" not found.');
    }
});
