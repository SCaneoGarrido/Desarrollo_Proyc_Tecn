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

    // Aquí puedes agregar la lógica para guardar el curso inscrito (esto hay que ver como lo vamos a hacer, si lo vamos a buscar a la bd o lo manejamos como una lista en python en el backend)
    

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

    // Aquí puedes agregar la lógica para procesar el archivo Excel (modifcala si quieres saiko, esto es solo un ejemplo basico)

    // Limpiar el formulario
    this.reset();

    alert('Archivo cargado exitosamente.');
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
