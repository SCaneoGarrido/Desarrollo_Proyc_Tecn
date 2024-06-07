// Función para ocultar todas las secciones
function hideAllSections() {
    document.getElementById('inicio').style.display = 'none';
    document.getElementById('cursos').style.display = 'none';
    document.getElementById('cargar-excels').style.display = 'none';
    document.getElementById('analisis-cursos').style.display = 'none';
    document.getElementById('perfil').style.display = 'none';
}

// Función para mostrar la sección seleccionada
function showSection(sectionId) {
    hideAllSections();
    document.getElementById(sectionId).style.display = 'block';
}

// Eventos de clic para los enlaces de la barra de navegación
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.nav-link').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault(); // Previene el comportamiento por defecto de los enlaces
            const sectionId = this.getAttribute('href').substring(1); // Obtiene el ID de la sección desde el href del enlace
            showSection(sectionId);
        });
    });

    // Mostrar la sección de landing page por defecto al cargar la página
    showSection('inicio');
});

// Manejar el formulario de inscripción de cursos
document.getElementById('form-inscribir-curso').addEventListener('submit', function(e) {
    e.preventDefault();
    const nombreCurso = document.getElementById('nombreCurso').value;
    const anioCurso = document.getElementById('anioCurso').value;
    const fechaInicio = document.getElementById('fechaInicio').value;
    const fechaTermino = document.getElementById('fechaTermino').value;

    // Validar que los campos no esten vacios
    if (nombreCurso.trim() === '' || anioCurso.trim() === '' || fechaInicio.trim() === '' || fechaTermino.trim() === '') {
        alert('Por favor, complete todos los campos.');
        return;
    }

    // Aquí puedes agregar la lógica para guardar el curso inscrito (esto hay que ver como lo vamos a hacer, si lo vamos a buscar a la bd o lo manejamos como una lista en python en el backend)
    
    let data_to_send = {
        'nombre': nombreCurso,
        'año': anioCurso,
        'fechaInicio': fechaInicio,
        'fechaTermino': fechaTermino
    };
    
    console.log(data_to_send);
    
    fetch('http://127.0.0.1:5000/app/register_courses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data_to_send) // Enviando los datos directamente, sin anidar bajo "data"
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error(error));
    
    

    // Limpiar el formulario
    this.reset();

    // Cerrar el modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('inscribirCursoModal'));
    modal.hide();

    // Actualizar la lista de cursos inscritos
    const cursosLista = document.getElementById('cursos-lista');
    cursosLista.innerHTML = `<p>Curso: ${nombreCurso}, Año: ${anioCurso}, Inicio: ${fechaInicio}, Término: ${fechaTermino}</p>`;
});

// Manejar el formulario de carga de excels
document.getElementById('form-cargar-excels').addEventListener('submit', function(e) {
    e.preventDefault();
    const archivoExcel = document.getElementById('archivoExcel').files[0];
    const uploadStatus = document.getElementById('upload-status');
    uploadStatus.textContent = "Cargando archivo...";

    const formData = new FormData();
    formData.append("file", archivoExcel);

    fetch('http://127.0.0.1:5000/app/recive_data', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            uploadStatus.textContent = "Archivo cargado exitosamente.";
            uploadStatus.style.color = "#28a745";
        } else {
            uploadStatus.textContent = "Error al cargar el archivo.";
            uploadStatus.style.color = "#dc3545";
        }
    })
    .catch(error => {
        console.error(error);
        uploadStatus.textContent = "Error al cargar el archivo.";
        uploadStatus.style.color = "#dc3545";
    });
});

// Manejar el formulario de edición de perfil
document.getElementById('form-editar-perfil').addEventListener('submit', function(e) {
    e.preventDefault();
    const nombreUsuario = document.getElementById('editarNombreUsuario').value;
    const cargoUsuario = document.getElementById('editarCargoUsuario').value;

    // Aquí puedes agregar la lógica para guardar los cambios del perfil del usuario

    // Actualizar la información en la tarjeta de perfil
    document.getElementById('nombreUsuario').textContent = nombreUsuario;
    document.getElementById('cargoUsuario').textContent = `Cargo: ${cargoUsuario}`;

    // Cerrar el modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('editarPerfilModal'));
    modal.hide();

    alert('Perfil actualizado exitosamente.');
});
