document.addEventListener('DOMContentLoaded', () => {
    const updateForm = document.getElementById('update-form');
    const loadingBar = document.getElementById('loading-bar');

    if (updateForm && loadingBar) {
        updateForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            // Retrieve values from form fields
            const userEmail = updateForm.querySelector('#email').value;
            const userName = updateForm.querySelector('#name').value || '';
            const userLang = updateForm.querySelector('#language').value || '';
            const userDiff = updateForm.querySelector('#difficulty').value || '';

            // Store values in session storage
            sessionStorage.setItem('email', userEmail);
            sessionStorage.setItem('name', userName);
            sessionStorage.setItem('language', userLang);
            sessionStorage.setItem('difficulty', userDiff);

            // Prepare data to be sent to the server
            const data = {
                email: userEmail,
                name: userName,
                language: userLang,
                difficulty: userDiff
            };

            // Show loading bar
            loadingBar.classList.add('loading-bar-active');

            try {
                const response = await fetch('https://llm-email-automation-back.onrender.com/request-update-otp', {
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
                    window.location.href = '/frontend/templates/verify_update.html';
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
