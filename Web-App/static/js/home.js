// Función para ocultar todas las secciones
function hideAllSections() {
  document.getElementById('inicio').style.display = 'none';
  document.getElementById('cursos').style.display = 'none';
  document.getElementById('cargar-excels').style.display = 'none';
  document.getElementById('analisis-cursos').style.display = 'none';
  document.getElementById('cargar-certificado').style.display = 'none';
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
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.nav-link').forEach(item => {
    item.addEventListener('click', function (e) {
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


// Evento de clic para registrar el curso
document.getElementById('form-inscribir-curso').addEventListener('submit', function (e) {
  e.preventDefault();
  formData = new FormData(this);
  const nombreCurso = document.getElementById('nombreCurso').value;
  const fechaInicio = document.getElementById('fechaInicio').value;
  const fechaTermino = document.getElementById('fechaTermino').value;
  const mes_curso = document.getElementById('selectorMES').value;
  const escuela = document.getElementById('escuela').value;
  const actividad_servicio = document.getElementById('selectorAS').value;
  const institucion = document.getElementById('institucion').value;
  const totalClases = document.getElementById('totalClases').value; //total de clases, nuevo campo agregado
  const google_form_excel = document.getElementById('google-form-excel').files[0];
  const user_id = localStorage.getItem('user_id');

  formData.append('nombre', nombreCurso);
  formData.append('fechaInicio', fechaInicio);
  formData.append('fechaTermino', fechaTermino);
  formData.append('mesCurso', mes_curso);
  formData.append('escuela', escuela);
  formData.append('actividadServicio', actividad_servicio);
  formData.append('institucion', institucion);
  formData.append('totalClases', totalClases);
  formData.append('user_id', user_id);
  formData.append('google_form_excel', google_form_excel);

  console.log('Data para api -> ', formData);

  fetch(`http://127.0.0.1:5000/app/register_courses/${user_id}`, {
    method: 'POST',
    body: formData
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

/// Función para obtener los cursos inscritos desde la base de datos
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
                      <p class="card-text"><strong>Institución: </strong> ${course[7]}</p>
                      <p class="card-text"><strong>Escuela: </strong> ${course[5]}</p>
                      <p class="card-text"><strong>Actividad o Servicio: </strong> ${course[6]}</p>
                      <p class="card-text"><strong>Cantidad total de clases: </strong> ${course[9]}</p>
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
document.getElementById('form-cargar-excels').addEventListener('submit', function (e) {
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
document.getElementById('form-seleccionar-curso').addEventListener('submit', function (e) {
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
        limpiarBtn.addEventListener('click', function () {
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
document.getElementById('irAInscribirCurso').addEventListener('click', function () {
  const modal = bootstrap.Modal.getInstance(document.getElementById('seleccionarCursoModal'));
  modal.hide();
  showSection('cursos');
});

/// Manejar carga de datos de usuarios en seccion de usuarios
document.addEventListener('DOMContentLoaded', function () {
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

document.addEventListener('DOMContentLoaded', function () {
  let selectedCourseId = null;

  // Función para obtener los cursos desde la base de datos
  function fetchCourses() {
    const user_id = localStorage.getItem('user_id');
    fetch(`/app/get_courses/${user_id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        if (data.cursos) {
          const courseList = document.getElementById('courseList');
          courseList.innerHTML = ''; // Limpiar la lista antes de llenarla
          data.cursos.forEach(course => {
            const listItem = document.createElement('li');
            listItem.classList.add('list-group-item');
            listItem.textContent = course[1]; // Asumiendo que el nombre del curso está en la segunda posición
            listItem.dataset.courseId = course[0]; // Asignar el curso_id al elemento
            listItem.addEventListener('click', function () {
              // Remover la clase 'selected' de todos los elementos
              document.querySelectorAll('.list-group-item').forEach(item => {
                item.classList.remove('selected');
              });
              // Agregar la clase 'selected' al elemento clicado
              this.classList.add('selected');
              selectedCourseId = this.dataset.courseId;
              console.log('Curso seleccionado ID:', selectedCourseId);
              document.getElementById('analyzeButton').disabled = false; // Habilitar el botón "Analizar"
            });
            courseList.appendChild(listItem);
          });
        } else {
          console.error('No hay cursos registrados');
        }
      })
      .catch(error => console.error('Error al obtener los cursos:', error));
  }

  // Llamar a la función para obtener los cursos cuando se abre el modal
  const courseModal = document.getElementById('courseModal');
  courseModal.addEventListener('show.bs.modal', fetchCourses);


  /**
   * EDITAR ESTE ANALITICO
   * const seleccionarCursoModal = new bootstrap.Modal(document.getElementById('seleccionarCursoModal'));
   */
  // Manejar el clic en el botón "Analizar"
  document.getElementById('analyzeButton').addEventListener('click', function () {
    if (selectedCourseId) {
        const user_id = localStorage.getItem('user_id');
        const url = `/app/analytical_engine/${user_id}?cursoID=${selectedCourseId}`;
        const dataframe_container = document.getElementById('dataframe-container');
        const ver_tabla_bd = document.getElementById('get-report-button');
        const modal_get_report = new bootstrap.Modal(document.getElementById('reportModal'));
        const clean_btn = document.getElementById('clear-button');

        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Análisis completado con éxito');
                ver_tabla_bd.style.display = 'block';
                ver_tabla_bd.style.marginTop = '20px';
                clean_btn.style.display = 'block';
                clean_btn.style.marginTop = '20px';
                dataframe_container.innerHTML = "<p>Análisis completo</p>";

                ver_tabla_bd.addEventListener('click', function () {
                    const newWindow = window.open('', '_blank');
                    newWindow.document.write('<html><head><title>Información de Base de Datos</title></head><body>');
                    newWindow.document.write(data.dataframe);
                    newWindow.document.write('</body></html>');
                });

                modal_get_report.show();

                const download_btn = document.getElementById('download-button');
                const cancel_btn = document.getElementById('cancel-button');

                download_btn.addEventListener('click', function () {
                    const downloadLink = document.createElement('a');
                    downloadLink.href = data.reporte_url;
                    downloadLink.download = 'reporte_curso.html';
                    document.body.appendChild(downloadLink);
                    downloadLink.click();
                    document.body.removeChild(downloadLink);
                    modal_get_report.hide();
                });

                cancel_btn.addEventListener('click', function () {
                    modal_get_report.hide();
                });
            } else {
                console.error('Error en el análisis:', data.error);
            }
        })
        .catch(error => console.error('Error al llamar al motor analítico:', error));
    }
  });

});


