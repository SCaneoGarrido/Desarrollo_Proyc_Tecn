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

    loginForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const user_email = document.getElementById('user_email').value;
        const user_password = document.getElementById('password').value;

        // comprobar campos que no esten vacios

        if (user_email.trim() === '' || user_password.trim() === '') {
            alert('Por favor, rellene todos los campos.');
            return;
        } else {
            fetch('http://127.0.0.1:5000/app/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ correo: user_email, contrasena: user_password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.url) {
                    // almacenamos info en localstorage
                    console.log("Datos de repuesta del servdirvidor -> ",data);
                    localStorage.setItem('user_id', data.user_id);
                    window.location.href = data.url; // Redirigir al usuario a la página de inicio
                }
            })
            .catch(error => console.error("Error -> ",error));
        }


    })
});