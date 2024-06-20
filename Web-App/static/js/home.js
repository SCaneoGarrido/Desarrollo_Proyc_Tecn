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

// Función para ocultar elementos de la sección "perfil" al cargar la página
function hideProfileElements() {
    const profileElements = document.querySelectorAll('#perfil *');
    profileElements.forEach(element => {
        element.style.display = 'none';
    });
}

// Función para mostrar elementos de la sección "perfil" cuando se selecciona la sección "perfil"
function showProfileElements() {
    const profileElements = document.querySelectorAll('#perfil *');
    profileElements.forEach(element => {
        element.style.display = 'block';
    });
}

// Eventos de clic para los enlaces de la barra de navegación
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.nav-link').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault(); // Previene el comportamiento por defecto de los enlaces
            const sectionId = this.getAttribute('href').substring(1); // Obtiene el ID de la sección desde el href del enlace
            showSection(sectionId);
            if (sectionId === 'perfil') {
                showProfileElements();
            } else {
                hideProfileElements();
            }
        });
    });

    // Mostrar la sección de landing page por defecto al cargar la página
    showSection('inicio');
    hideProfileElements(); // Asegúrate de ocultar los elementos de "perfil" al cargar la página
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
          <label for="Telefono" class="form-label">Telefono</label>
          <input type="text" class="form-control" name="telefono" required>
          <label for="email" class="form-label">Email</label>
          <input type="email" class="form-control" name="email" required>
          <label for="nacionalidad" class="form-label">Nacionalidad</label>
          <input type="text" class="form-control" name="nacionalidad" required>
          <label for="Comuna" class="form-label">Comuna</label>
          <input type="text" class="form-control" name="comuna" required>
          <label for="Barrio" class="form-label">Barrio</label>
          <input type="text" class="form-control" name="barrio" required>
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
    
    const nombreCurso        = document.getElementById('nombreCurso').value;
    const fechaInicio        = document.getElementById('fechaInicio').value;
    const fechaTermino       = document.getElementById('fechaTermino').value;
    const mes_curso          = document.getElementById('selectorMES').value;
    const escuela            = document.getElementById('escuela').value;
    const actividad_servicio = document.getElementById('selectorAS').value;
    const institucion        = document.getElementById('institucion').value;
    const user_id            = localStorage.getItem('user_id');
    

    const asistentes = [];
    document.querySelectorAll('.accordion-item').forEach(asistente => {
      const rut          = asistente.querySelector('input[name="rut"]').value;
      const edad         = asistente.querySelector('input[name="edad"]').value;
      const genero       = asistente.querySelector('select[name="genero"]').value;
      const nombre       = asistente.querySelector('input[name="nombre"]').value;
      const apellido     = asistente.querySelector('input[name="apellido"]').value;
      const direccion    = asistente.querySelector('input[name="direccion"]').value;
      const telefono     = asistente.querySelector('input[name="telefono"]').value;
      const email        = asistente.querySelector('input[name="email"]').value;
      const nacionalidad = asistente.querySelector('input[name="nacionalidad"]').value;
      const comuna       = asistente.querySelector('input[name="comuna"]').value;
      const barrio       = asistente.querySelector('input[name="barrio"]').value;
      
      // TRANSFORMACIONES PARA ENVIO
      const nombre_completo = `${nombre} ${apellido}`;
      const [rut_noDV, rut_DV] = rut.split('-'); // AQUI SEPARE EL DIGITO VERIFICADOR DEL RUT Y LOS PUSE EN VARIABLES DISTINTAS

      /**
       * ACTUALIZACION DE VARIABLES 
       * rut_noDV: contiene el rut sin Digito Verificador ni guion
       * rut_DV: contiene el Digito Verificador
       * nombre_completo: contiene el nombre completo del asistente
       * 
       * SE QUITA ESTADO CIVIL, NO ES NECESARIO YA QUE EL FORMATO DE ASISTENCIA NO LO CONTIENE
       */
    
      asistentes.push({ 
        rut_noDV, 
        rut_DV, 
        edad, 
        genero, 
        nombre_completo, 
        direccion, 
        telefono, 
        email, 
        nacionalidad, 
        comuna, 
        barrio 
      });

    });
  
    const data_to_send = {
      nombre:             nombreCurso,
      fechaInicio:        fechaInicio,
      fechaTermino:       fechaTermino,
      mes_curso:          mes_curso,
      escuela:            escuela,
      actividad_servicio: actividad_servicio,
      institucion:        institucion,
      user_id:            user_id,
      asistentes:         asistentes
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
                

                const courseItem = document.createElement('div');
                courseItem.className = 'course-item card mb-3';
                courseItem.innerHTML = `
                    <div class="card-body">
                        <h3 class="card-title">${course[1]}</h3>
                        <p class="card-text"><strong>UID del curso: </strong> ${course[0]}</p>
                        <p class="card-text"><strong>Mes: </strong> ${course[8]}</p>
                        <p class="card-text"><strong>Fecha de inicio: </strong> ${new Date(course[2]).toLocaleDateString()}</p>
                        <p class="card-text"><strong>Fecha de fin: </strong> ${new Date(course[3]).toLocaleDateString()}</p>
                        <p class="card-text"><strong>Institucion </strong> ${course[7]}</p>
                        <p class="card-text"><strong>Escuela </strong> ${course[5]}</p>
                        <p class="card-text"><strong>Actividad o Servicio </strong> ${course[6]}</p>

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

function cargarCursos_modal() {
    const userID = localStorage.getItem('user_id');
  
    if (userID) {
      fetch(`/app/get_courses/${userID}`)
      .then(response => response.json())
      .then(data => {
        cursoSeleccionado = document.getElementById('cursoSeleccionado');
        cursoSeleccionado.innerHTML = '';
  
        if (data.cursos && data.cursos.length > 0) {
          data.cursos.forEach(curso => {
            const [id, nombre] = curso;
            const option = document.createElement('option');
            option.style = 'color: black;';
            option.value = id;
            option.textContent = nombre;
            option.textContent = `${nombre} UID -> (${id})`;
            cursoSeleccionado.appendChild(option);
          })
        }
      })
      .catch(error => console.error(error));
    }
  }
  
let archivoExcelGlobal = null; // Variable global para almacenar el archivo Excel

  // Manejar el formulario de carga de excels
document.getElementById('form-cargar-excels').addEventListener('submit', function(e) {
    e.preventDefault();
    const archivoExcel = document.getElementById('archivoExcel').files[0];
    const uploadStatus = document.getElementById('upload-status');
    
  
    if (!archivoExcel) {
        uploadStatus.textContent = "Por favor, selecciona un archivo.";
        uploadStatus.style.color = "#dc3545";
        return;
    }
  
    uploadStatus.textContent = "Archivo cargado y listo para vincular.";
    uploadStatus.style.color = "#28a745";
    archivoExcelGlobal = archivoExcel; // Guardar el archivo en la variable global
  
    // Mostrar el modal para seleccionar curso
    const seleccionarCursoModal = new bootstrap.Modal(document.getElementById('seleccionarCursoModal'));
    seleccionarCursoModal.show();
    // Llenar las opciones del select con los cursos disponibles
    cargarCursos_modal();
});
  
  // Manejar el formulario de selección de curso
document.getElementById('form-seleccionar-curso').addEventListener('submit', function(e) {
    e.preventDefault();
    const cursoSeleccionado = document.getElementById('cursoSeleccionado').value;
    const uploadStatus = document.getElementById('upload-status');
    const userID = localStorage.getItem('user_id');
  
    if (cursoSeleccionado === '') {
        alert('Por favor, seleccione un curso.');
        return;
    }
  
    if (!archivoExcelGlobal) {
        alert('Por favor, cargue un archivo antes de seleccionar un curso.');
        return;
    }
  
    const formData = new FormData();
    formData.append("file", archivoExcelGlobal);
    formData.append("cursoId", cursoSeleccionado);
  
    fetch(`/app/recive_data/${userID}`, {
        method: 'POST',
        body: formData
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
                uploadStatus.textContent = '';
                archivoExcelGlobal = null; // Limpiar la variable global
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



/**
 * MENSAJE PARA PANA BENJA EL FRONT END MAESTRO
 * puedes revisar este evento que carga los datos del usuario
 * bug:
 * cuando te logeas entras a la web y el cuadro o seccion del usuario
 * se ve en cada seccion. No de manera permantente pero es como si caminara 
 * entre secciones. 
 * 
 * INICIA LA APP LOGUEA Y VERAS EL BUG
 */

/// Manejar carga de datos de usuarios en seccion de usuarios
document.addEventListener('DOMContentLoaded', function() {
    // verificar un user_id en localstorage
    const userId = localStorage.getItem('user_id');

    if (userId) {
        // si este existe hacemos una peticion a la API
        fetch(`http://127.0.0.1:5000/app/get_info_User/${userId}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);

                // Verificar si data.info existe y no está vacío
                if (data.info) {
                    const userInfo = data.info;
                    document.getElementById('nombreUsuario').textContent = userInfo[1];
                    document.getElementById('apellidoUsuario').textContent = userInfo[2];
                    document.getElementById('emailUsuario').textContent = userInfo[0];
                    document.getElementById('perfil').style.display = 'block'; // Mostrar la sección de perfil
                } else {
                    console.error('No se encontró información del usuario.');
                }
            })
            .catch(error => console.error('Error al obtener la información del usuario:', error));
    }
});