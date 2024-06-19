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

// Evento de clic para agregar un asistente
document.getElementById('add-asistente').addEventListener('click', function() {
    const asistentesContainer = document.getElementById('accordionAsistentes');
    const newAsistenteId = `asistente-${Date.now()}`;
    const newAsistente = document.createElement('div');
    newAsistente.classList.add('accordion-item');
    newAsistente.innerHTML = `
      <h2 class="accordion-header" id="heading-${newAsistenteId}">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-${newAsistenteId}" aria-expanded="false" aria-controls="collapse-${newAsistenteId}">
          Asistente
        </button>
      </h2>
      <div id="collapse-${newAsistenteId}" class="accordion-collapse collapse" aria-labelledby="heading-${newAsistenteId}" data-bs-parent="#accordionAsistentes">
        <div class="accordion-body">
          <label for="rut" class="form-label">RUT</label>
          <input type="text" class="form-control" name="rut" required>
          <label for="edad" class="form-label">Edad</label>
          <input type="number" class="form-control" name="edad" required>
          <label for="genero" class="form-label">Género</label>
          <select class="form-control" name="genero" required>
            <option value="Masculino">Masculino</option>
            <option value="Femenino">Femenino</option>
            <option value="Otro">Otro</option>
          </select>
          <label for="nombre" class="form-label">Nombre</label>
          <input type="text" class="form-control" name="nombre" required>
          <label for="apellido" class="form-label">Apellido</label>
          <input type="text" class="form-control" name="apellido" required>
          <label for="direccion" class="form-label">Dirección</label>
          <input type="text" class="form-control" name="direccion" required>
          <label for="estadoCivil" class="form-label">Estado Civil</label>
          <select class="form-control" name="estadoCivil" required>
            <option value="Soltero">Soltero</option>
            <option value="Casado">Casado</option>
            <option value="Divorciado">Divorciado</option>
            <option value="Viudo">Viudo</option>
          </select>
          <button type="button" class="btn btn-danger remove-asistente mt-2">Eliminar</button>
        </div>
      </div>
    `;
    asistentesContainer.appendChild(newAsistente);
  
    // Añadir evento para eliminar asistente
    newAsistente.querySelector('.remove-asistente').addEventListener('click', function() {
      newAsistente.remove();
    });
  });

  // Evento de clic para registrar el curso
  document.getElementById('form-inscribir-curso').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const nombreCurso = document.getElementById('nombreCurso').value;
    const anioCurso = document.getElementById('anioCurso').value;
    const fechaInicio = document.getElementById('fechaInicio').value;
    const fechaTermino = document.getElementById('fechaTermino').value;
    const user_id = localStorage.getItem('user_id');
  
    const asistentes = [];
    document.querySelectorAll('.accordion-item').forEach(asistente => {
      const rut = asistente.querySelector('input[name="rut"]').value;
      const edad = asistente.querySelector('input[name="edad"]').value;
      const genero = asistente.querySelector('select[name="genero"]').value;
      const nombre = asistente.querySelector('input[name="nombre"]').value;
      const apellido = asistente.querySelector('input[name="apellido"]').value;
      const direccion = asistente.querySelector('input[name="direccion"]').value;
      const estadoCivil = asistente.querySelector('select[name="estadoCivil"]').value;
  
      asistentes.push({ rut, edad, genero, nombre, apellido, direccion, estadoCivil });
    });
  
    const data_to_send = {
      nombre: nombreCurso,
      año: anioCurso,
      fechaInicio: fechaInicio,
      fechaTermino: fechaTermino,
      user_id: user_id,
      asistentes: asistentes
    };

    console.log('Data para api -> ', data_to_send);
  
    fetch(`http://127.0.0.1:5000/app/register_courses/${user_id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data_to_send)
    })
    .then(response => response.json())
    .then(data => {
      alert(data.message || data.error);
    })
    .catch(error => {
      console.error("Error en la solicitud:", error);
      alert("Error al registrar el curso. Por favor, intente nuevamente.");
    });
  
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
        // Limpiar cualquier contenido previo
        div_cursos.innerHTML = '';

        if (data.cursos && data.cursos.length > 0) {
            data.cursos.forEach(course => {
                const [id, nombre, fecha_inicio, fecha_fin, user_id, año] = course;

                const courseItem = document.createElement('div');
                courseItem.className = 'course-item card mb-3';
                courseItem.innerHTML = `
                    <div class="card-body">
                        <h3 class="card-title">${nombre}</h3>
                        <p class="card-text"><strong>UID del curso:</strong> ${id}</p>
                        <p class="card-text"><strong>Año:</strong> ${año}</p>
                        <p class="card-text"><strong>Fecha de inicio:</strong> ${new Date(fecha_inicio).toLocaleDateString()}</p>
                        <p class="card-text"><strong>Fecha de fin:</strong> ${new Date(fecha_fin).toLocaleDateString()}</p>
                    </div>
                `;
                div_cursos.appendChild(courseItem);
            });
        } else {
            div_cursos.textContent = 'No hay cursos inscritos.';
        }
    })
    .catch(error => {
        console.error(error);
        div_cursos.textContent = 'Error al cargar los cursos.';
    });
}

// Llamar a la función para cargar los cursos al cargar la página
document.addEventListener('DOMContentLoaded', cargarCursos());

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
