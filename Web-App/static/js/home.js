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
    const user_id = localStorage.getItem('user_id');
    // Validar que los campos no esten vacios
    if (nombreCurso.trim() === '' || anioCurso.trim() === '' || fechaInicio.trim() === '' || fechaTermino.trim() === '') {
        alert('Por favor, complete todos los campos.');
        return;
    }
    let data_to_send = {
        'nombre': nombreCurso,
        'año': anioCurso,
        'fechaInicio': fechaInicio,
        'fechaTermino': fechaTermino,
        'user_id': user_id
    };
    console.log(data_to_send);
    fetch(`http://127.0.0.1:5000/app/register_course/${user_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data_to_send) // Enviando los datos directamente, sin anidar bajo "data"
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        /*
        const cursosLista = document.getElementById('cursos-lista');
        const nuevoCurso = document.createElement('p');
        nuevoCurso.textContent = `Curso: ${nombreCurso}, Año: ${anioCurso}, Inicio: ${fechaInicio}, Término: ${fechaTermino}`;
        cursosLista.appendChild(nuevoCurso);
        // Actualizar el mensaje de estado
        const estadoCursos = document.getElementById('estado-cursos');
        estadoCursos.textContent = "Los cursos inscritos son:";
        */

        alert(data.message);

    })
    .catch(error => console.error(error));
    // Limpiar el formulario
    this.reset();
    // Cerrar el modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('inscribirCursoModal'));
    modal.hide();
});

// Función para obtener los cursos inscritos desde la base de datos
function cargarCursos() {
    const user_id = localStorage.getItem('user_id');
    const div_cursos = document.getElementById('cursos-lista');
    fetch(`http://127.0.0.1:5000/app/get_courses/${user_id}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // IMPRIMIR LOS CURSOS INSCRITOS
        div_cursos.innerHTML = ''; // Limpiar cualquier contenido previo

        if (data.cursos && data.cursos.length > 0) {
            data.cursos.forEach(course => {
                const [id, nombre, año, fecha_inicio, fecha_fin, otra_propiedad] = course;

                const courseItem = document.createElement('div');
                courseItem.className = 'course-item';
                courseItem.innerHTML = `
                    <h3>${nombre}</h3>
                    <p>Año: ${año}</p>
                    <p>Fecha de inicio: ${new Date(fecha_inicio).toLocaleDateString()}</p>
                    <p>Fecha de fin: ${new Date(fecha_fin).toLocaleDateString()}</p>
                `;
                div_cursos.appendChild(courseItem);
            });
        } else {
            div_cursos.textContent = 'No estás inscrito en ningún curso.';
        }
    })
    .catch(error => {
        console.error(error);
        div_cursos.textContent = 'Error al cargar los cursos.';
    });
}


// Llamar a la función para cargar los cursos al cargar la página
document.addEventListener('DOMContentLoaded', cargarCursos);

// Manejar el formulario de carga de excels
document.getElementById('form-cargar-excels').addEventListener('submit', function(e) {
    e.preventDefault();
    const archivoExcel = document.getElementById('archivoExcel').files[0];
    const uploadStatus = document.getElementById('upload-status');
    const excelPreview = document.getElementById('excel-preview');
    uploadStatus.textContent = "Cargando archivo...";
    const formData = new FormData();
    formData.append("file", archivoExcel);
    fetch('/app/recive_data', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            uploadStatus.textContent = "Archivo cargado exitosamente.";
            uploadStatus.style.color = "#28a745";
            // Mostrar el modal para seleccionar curso
            const seleccionarCursoModal = new bootstrap.Modal(document.getElementById('seleccionarCursoModal'));
            seleccionarCursoModal.show();
            // Llenar las opciones del select con los cursos disponibles
            fetch('/app/get_courses')
            .then(response => response.json())
            .then(courses => {
                const cursoSeleccionado = document.getElementById('cursoSeleccionado');
                cursoSeleccionado.innerHTML = '';
                if (courses.length > 0) {
                    courses.forEach(course => {
                        const option = document.createElement('option');
                        option.value = course.id;
                        option.textContent = `${course.nombre} (${course.año})`;
                        cursoSeleccionado.appendChild(option);
                    });
                } else {
                    cursoSeleccionado.innerHTML = '';
                }
            });
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

// Manejar el formulario de selección de curso
document.getElementById('form-seleccionar-curso').addEventListener('submit', function(e) {
    e.preventDefault();
    const cursoSeleccionado = document.getElementById('cursoSeleccionado').value;
    if (cursoSeleccionado === '') {
        alert('Por favor, seleccione un curso.');
        return;
    }
    fetch('/app/vincular_archivo_curso', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cursoId: cursoSeleccionado })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Cerrar el modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('seleccionarCursoModal'));
            modal.hide();
            // Mostrar el archivo cargado en el frontend
            const excelPreview = document.getElementById('excel-preview');
            excelPreview.innerHTML = data.data; // Asumiendo que `data.data` contiene el HTML del archivo Excel
            alert('Archivo vinculado exitosamente al curso.');
            // Agregar botón para limpiar y cargar otro archivo
            const limpiarBtn = document.createElement('button');
            limpiarBtn.textContent = 'Limpiar y cargar otro archivo';
            limpiarBtn.className = 'btn btn-warning';
            limpiarBtn.id = 'limpiar-btn'; // Asignar un ID al botón
            limpiarBtn.addEventListener('click', function() {
                excelPreview.innerHTML = '';
                document.getElementById('archivoExcel').value = '';
                const uploadStatus = document.getElementById('upload-status');
                uploadStatus.textContent = '';
                // Ocultar el botón "Limpiar y cargar otro archivo"
                limpiarBtn.style.display = 'none';
                // Volver a mostrar el botón "Cargar"
                document.getElementById('cargar-btn').style.display = 'block';
            });
            // Añadir el botón "Limpiar y cargar otro archivo" al contenedor
            const buttonContainer = document.getElementById('button-container');
            buttonContainer.appendChild(limpiarBtn);
            // Ocultar el botón "Cargar"
            document.getElementById('cargar-btn').style.display = 'none';
        } else {
            alert('Error al vincular el archivo al curso.');
        }
    })
    .catch(error => {
        console.error(error);
        alert('Error al vincular el archivo al curso.');
    });
});

// Redirigir a la sección de inscripción de cursos
document.getElementById('irAInscribirCurso').addEventListener('click', function() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('seleccionarCursoModal'));
    modal.hide();
    showSection('cursos');
});
