// Función para ocultar todas las secciones
function hideAllSections() {
    document.getElementById('inicio').style.display = 'none';
    document.getElementById('cursos').style.display = 'none';
    document.getElementById('soporte').style.display = 'none';
    document.getElementById('cuenta').style.display = 'none';
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

    // Aquí puedes agregar la lógica para guardar el curso inscrito
    // Por ejemplo, puedes agregarlo a una lista de cursos inscritos

    // Limpiar el formulario
    this.reset();

    // Cerrar el modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('inscribirCursoModal'));
    modal.hide();

    // Actualizar la lista de cursos inscritos
    const cursosLista = document.getElementById('cursos-lista');
    cursosLista.innerHTML = `<p>Curso: ${nombreCurso}, Año: ${anioCurso}, Inicio: ${fechaInicio}, Término: ${fechaTermino}</p>`;
});
