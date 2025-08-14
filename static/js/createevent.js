document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');
  const inputs = form.querySelectorAll('input, textarea, select');
  
  // You can customize validation rules here
  const validators = {
    event_name: value => value.trim().length >= 5,
    event_date: value => {
      const today = new Date().setHours(0,0,0,0);
      const selectedDate = new Date(value).setHours(0,0,0,0);
      return selectedDate >= today;
    },
    event_time: value => value !== '',
    event_image: input => {
      if (input.files.length === 0) return false;
      const file = input.files[0];
      const validTypes = ['image/jpeg', 'image/png', 'image/gif'];
      return validTypes.includes(file.type);
    }
    // Add more validators if your form has more fields
  };

  // Function to show or clear error message
  function showError(input, message) {
    let errorElem = input.nextElementSibling;
    if (!errorElem || !errorElem.classList.contains('error-message')) {
      errorElem = document.createElement('div');
      errorElem.classList.add('error-message');
      errorElem.style.color = 'red';
      errorElem.style.fontSize = '0.85rem';
      input.parentNode.insertBefore(errorElem, input.nextSibling);
    }
    errorElem.textContent = message;
  }

  function clearError(input) {
    const errorElem = input.nextElementSibling;
    if (errorElem && errorElem.classList.contains('error-message')) {
      errorElem.textContent = '';
    }
  }

  // Real-time validation function
  inputs.forEach(input => {
    input.addEventListener('input', () => {
      const name = input.name;
      if (!name) return; // skip inputs without a name

      // Special case for file input, listen for change event instead
      if (input.type === 'file') return;

      if (validators[name]) {
        if (!validators[name](input.value)) {
          showError(input, `Invalid ${name.replace('_', ' ')}`);
        } else {
          clearError(input);
        }
      }
    });

    // For file inputs, validate on change
    if (input.type === 'file') {
      input.addEventListener('change', () => {
        if (validators[input.name]) {
          if (!validators[input.name](input)) {
            showError(input, 'Please upload a valid image file (jpeg, png, gif)');
          } else {
            clearError(input);
          }
        }
      });
    }
  });

  // Final form validation on submit
  form.addEventListener('submit', (e) => {
    let isValid = true;
    inputs.forEach(input => {
      const name = input.name;
      if (!name) return;
      if (validators[name] && !validators[name](input.type === 'file' ? input : input.value)) {
        showError(input, `Invalid ${name.replace('_', ' ')}`);
        isValid = false;
      } else {
        clearError(input);
      }
    });
    if (!isValid) {
      e.preventDefault(); // stop form submission if invalid
    }
  });
});
