document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const usernameInput = document.getElementById('username');

    form.addEventListener('submit', function(e) {
        const username = usernameInput.value.trim();

        // Validar: solo letras, mínimo 3 caracteres, sin espacios ni números
        if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ]{3,}$/.test(username)) {
            e.preventDefault();
            alert('El nombre de usuario debe tener solo letras (sin espacios ni números) y al menos 3 caracteres.');
            usernameInput.focus();
        }
    });
});