/**
 * MÙSIC Shop - JavaScript da Página de Login
 */

document.addEventListener('DOMContentLoaded', function () {
    const nomeInput = document.getElementById('login_nome');
    if (nomeInput && !nomeInput.value) {
        nomeInput.focus();
    }
});
