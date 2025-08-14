document.addEventListener('DOMContentLoaded', function () {
  const usernameInput = document.querySelector('input[name="username"]');
  const newPasswordInput = document.querySelector('input[name="new_password"]');
  const confirmPasswordInput = document.querySelector('input[name="confirm_password"]');
  const form = document.querySelector('form');

  // Create and insert validation message spans
  [usernameInput, newPasswordInput, confirmPasswordInput].forEach(input => {
    const span = document.createElement('span');
    span.style.color = 'yellow';
    span.style.fontSize = '12px';
    span.style.display = 'block';
    span.className = 'error-message';
    input.parentNode.insertBefore(span, input.nextSibling);
  });

  function showError(input, message) {
    const errorSpan = input.parentNode.querySelector('.error-message');
    errorSpan.textContent = message;
  }

  function clearError(input) {
    const errorSpan = input.parentNode.querySelector('.error-message');
    errorSpan.textContent = '';
  }

  usernameInput.addEventListener('input', () => {
    if (usernameInput.value.trim().length < 3) {
      showError(usernameInput, 'Username must be at least 3 characters.');
    } else {
      clearError(usernameInput);
    }
  });

  newPasswordInput.addEventListener('input', () => {
    if (newPasswordInput.value.length < 6) {
      showError(newPasswordInput, 'Password must be at least 6 characters.');
    } else {
      clearError(newPasswordInput);
    }
  });

  confirmPasswordInput.addEventListener('input', () => {
    if (confirmPasswordInput.value !== newPasswordInput.value) {
      showError(confirmPasswordInput, 'Passwords do not match.');
    } else {
      clearError(confirmPasswordInput);
    }
  });

  form.addEventListener('submit', function (e) {
    let isValid = true;

    if (usernameInput.value.trim().length < 3) {
      showError(usernameInput, 'Username must be at least 3 characters.');
      isValid = false;
    }

    if (newPasswordInput.value.length < 6) {
      showError(newPasswordInput, 'Password must be at least 6 characters.');
      isValid = false;
    }

    if (confirmPasswordInput.value !== newPasswordInput.value) {
      showError(confirmPasswordInput, 'Passwords do not match.');
      isValid = false;
    }

    if (!isValid) {
      e.preventDefault();
    }
  });
});
