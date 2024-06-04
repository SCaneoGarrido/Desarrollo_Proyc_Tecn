document.addEventListener('DOMContentLoaded', () => {
    const btnSignIn = document.getElementById('sign-in'),
        btnSignUp = document.getElementById('sign-up'),
        formRegister = document.querySelector('.register'),
        formLogin = document.querySelector('.container-form.hide');

    btnSignIn.addEventListener('click', e => {
        formRegister.classList.add('hide');
        formLogin.classList.remove('hide');
    });

    btnSignUp.addEventListener('click', e => {
        formLogin.classList.add('hide');
        formRegister.classList.remove('hide');
    });

    const registerForm = document.getElementById('form-registro');
    const loginForm = document.getElementById('form-login');

    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const nombre = document.getElementById('nombre').value;
        const apellido = document.getElementById('apellido').value;
        const email = document.getElementById('email').value;
        const clave = document.getElementById('clave').value;

        if ((nombre.trim() === '') || (apellido.trim() === '') || (email.trim() === '') || (clave.trim() === '')) {
            // validar que los campos no esten vacios
            alert('Rellene todos los campos');
        }
        const requestData = { nombre, apellido, }
        try {
            const response = await fetch('http://127.0.0.1:5000/app/registro', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ nombre: nombre, apellido: apellido, correo: email, contrasena: clave })
            });
            const data = await response.json();
            console.log(data); // Aquí puedes manejar la respuesta del servidor
            window.location.href = '../FrontEnd/login.html';
        } catch (error) {
            console.error('Error al realizar la solicitud:', error);
            if (error.response) {
                console.error('Código de estado:', error.response.status);
                console.error('Mensaje de error:', error.response.data.message);
            } else {
                console.error('Error desconocido:', error);
            }
        }
    });

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const correo = loginForm.querySelector('input[type="email"][placeholder="Email"]').value;
        const contraseña = loginForm.querySelector('input[type="password"][placeholder="Contraseña"]').value;

        try {
            const response = await fetch('http://127.0.0.1:5000/app/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ correo: correo, contraseña: contraseña })
            });
            const data = await response.json();

            // Verificar si la respuesta contiene datos de sesión válidos
            if (data && data.user_id && data.correo) {
                // Almacenar la sesión en el local storage
                localStorage.setItem('user_id', data.user_id);
                localStorage.setItem('correo', data.correo);
                localStorage.setItem('archivos', data.uploaded_files);
                // También podrías almacenar otros datos de sesión si los necesitas
                console.log(localStorage.user_id);
                console.log(localStorage.correo);
                console.log(localStorage.archivos); 
                // Redireccionar a la página de inicio después del inicio de sesión
                window.location.href = "../FrontEnd/home.html";
            } else {
                console.error('Respuesta de inicio de sesión incompleta:', data);
                // Manejar el caso en que la respuesta del servidor no contiene datos de sesión válidos
            }
        } catch (error) {
            console.error('Error al realizar la solicitud:', error);
        }
    });
});