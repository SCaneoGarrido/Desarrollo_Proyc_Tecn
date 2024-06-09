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
    let data_to_send = {
        'nombre': nombreCurso,
        'año': anioCurso,
        'fechaInicio': fechaInicio,
        'fechaTermino': fechaTermino
    };
    console.log(data_to_send);
    fetch('/app/register_courses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data_to_send) // Enviando los datos directamente, sin anidar bajo "data"
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Actualizar la lista de cursos inscritos
        const cursosLista = document.getElementById('cursos-lista');
        const nuevoCurso = document.createElement('p');
        nuevoCurso.textContent = `Curso: ${nombreCurso}, Año: ${anioCurso}, Inicio: ${fechaInicio}, Término: ${fechaTermino}`;
        cursosLista.appendChild(nuevoCurso);
        // Actualizar el mensaje de estado
        const estadoCursos = document.getElementById('estado-cursos');
        estadoCursos.textContent = "Los cursos inscritos son:";
    })
    .catch(error => console.error(error));
    // Limpiar el formulario
    this.reset();
    // Cerrar el modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('inscribirCursoModal'));
    modal.hide();
});

// Función para cargar los cursos al iniciar
function cargarCursos() {
    fetch('/app/get_courses')
    .then(response => response.json())
    .then(courses => {
        const cursosLista = document.getElementById('cursos-lista');
        const estadoCursos = document.getElementById('estado-cursos');
        cursosLista.innerHTML = '';
        if (courses.length > 0) {
            estadoCursos.textContent = "Los cursos inscritos son:";
            courses.forEach(course => {
                const cursoItem = document.createElement('p');
                cursoItem.textContent = `Curso: ${course.nombre}, Año: ${course.año}, Inicio: ${course.fechaInicio}, Término: ${course.fechaTermino}`;
                cursosLista.appendChild(cursoItem);
            });
        } else {
            estadoCursos.textContent = "No hay cursos inscritos aún.";
        }
    })
    .catch(error => console.error(error));
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
            limpiarBtn.addEventListener('click', function() {
                excelPreview.innerHTML = '';
                document.getElementById('archivoExcel').value = '';
                const uploadStatus = document.getElementById('upload-status');
                uploadStatus.textContent = '';
            });
            excelPreview.appendChild(limpiarBtn);
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