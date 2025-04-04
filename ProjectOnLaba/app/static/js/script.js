function toggleForm() {
            const loginForm = document.getElementById('login-form');
            const registerForm = document.getElementById('register-form');

            if (loginForm.style.display === 'block') {
                loginForm.style.display = 'none';
                registerForm.style.display = 'block';
            } else {
                loginForm.style.display = 'block';
                registerForm.style.display = 'none';
            }
        }