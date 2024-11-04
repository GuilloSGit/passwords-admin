document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.toggle-password');
  
    toggleButtons.forEach(button => {
      button.addEventListener('click', function(event) {
        event.preventDefault();
  
        const passId = this.getAttribute('data-pass-id');
        const passwordField = document.getElementById(`password-${passId}`);
        const icon = document.getElementById(`icon-${passId}`);
  
        if (passwordField.textContent === '******') {
          fetch(`/get_password/${passId}/`)
            .then(response => response.json())
            .then(data => {
              passwordField.textContent = data.password;
              icon.classList.remove('bi-eye');
              icon.classList.add('bi-eye-slash');
            });
        } else {
          passwordField.textContent = '******';
          setTimeout(() => {
              icon.classList.remove('bi-eye-slash');
              icon.classList.add('bi-eye');
          }, 100);
        }
      });
    });
  });
  