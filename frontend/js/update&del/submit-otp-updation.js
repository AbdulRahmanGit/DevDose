document.addEventListener('DOMContentLoaded', () => {
    const updateForm = document.getElementById('submit-update-otp');
    const loadingBar = document.getElementById('loading-bar');
    const storedEmail = sessionStorage.getItem('email');
    const storedName = sessionStorage.getItem('name');
    const storedLang = sessionStorage.getItem('language');
    const storedDiff = sessionStorage.getItem('difficulty');

    console.log('Stored Values:', {
        email: storedEmail,
        name: storedName,
        language: storedLang,
        difficulty: storedDiff
    });

    if (updateForm && loadingBar) {
        updateForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Show loading bar
            loadingBar.classList.add('loading-bar-active');

            const data = {
                otp: updateForm.querySelector('#otp').value,
                email: storedEmail || '',  // Default to empty string if not set
                name: storedName || '',
                language: storedLang || '',
                difficulty: storedDiff || ''
            };

            console.log('Confirming updation with OTP:', data);
            try {
                const response = await fetch( 'https://llm-email-automation-back.onrender.com/update', {
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
                    window.location.href = '/'; // Redirect to home or another page
                } else {
                    const errorData = await response.json();
                    alert(errorData.detail || 'OTP verification failed'); // Use detail if returned by backend
                }
            } catch (error) {
                console.error('OTP verification failed:', error);
                alert('OTP verification failed. Please try again.');
            } finally {
                // Hide loading bar after the process completes
                setTimeout(() => loadingBar.classList.remove('loading-bar-active'), 3000);
            }
        });
    } else {
        console.error('Form with ID "submit-update-otp" or loading bar with ID "loading-bar" not found.');
    }
});
