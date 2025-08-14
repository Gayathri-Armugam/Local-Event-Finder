// Validate Registration Form
document.addEventListener("DOMContentLoaded", function () {
    const registrationForm = document.getElementById("registrationForm");
    const loginForm = document.getElementById("loginForm");

    if (registrationForm) {
        registrationForm.addEventListener("submit", function (event) {
            event.preventDefault();
            validateRegistrationForm();
        });
    }

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault();
            validateLoginForm();
        });
    }

    function validateRegistrationForm() {
        let name = document.getElementById("full-name").value.trim();
        let email = document.getElementById("email").value.trim();
        let password = document.getElementById("reg-password").value.trim();
        let confirmPassword = document.getElementById("confirm-password").value.trim();
        let errors = [];

        // Validate Full Name
        if (name.length < 3) {
            errors.push("Full Name must be at least 3 characters.");
        }

        // Validate Email
        let emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!emailPattern.test(email)) {
            errors.push("Please enter a valid email address.");
        }

        // Validate Password (Minimum 6 characters, 1 number, 1 uppercase)
        let passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/;
        if (!passwordPattern.test(password)) {
            errors.push("Password must be at least 6 characters long and contain at least 1 number.");
        }

        // Validate Confirm Password
        if (password !== confirmPassword) {
            errors.push("Passwords do not match.");
        }

        if (errors.length > 0) {
            alert(errors.join("\n"));
        } else {
            alert("Registration successful!");
            registrationForm.submit(); // Submit form if all validations pass
        }
    }

    function validateLoginForm() {
        let username = document.getElementById("username").value.trim();
        let password = document.getElementById("reg-password").value.trim();
        let errors = [];

        // Validate Username
        if (username.length < 3) {
            errors.push("Username must be at least 3 characters.");
        }

        // Validate Password
        if (password.length < 6) {
            errors.push("Password must be at least 6 characters.");
        }

        if (errors.length > 0) {
            alert(errors.join("\n"));
        } else {
            alert("Login successful!");
            loginForm.submit(); // Submit form if all validations pass
        }
    }
});
