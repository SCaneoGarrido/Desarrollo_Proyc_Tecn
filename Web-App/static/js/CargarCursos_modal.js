document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('form-seleccionar-curso').addEventListener('submit', function(event){
    event.preventDefault();
  });
    // Cargar cursos cuando se abra el modal
    const seleccionarCursoModal = document.getElementById('seleccionarCursoModal');
    seleccionarCursoModal.addEventListener('shown.bs.modal', function() {
        cargarCursos();
    });
});


function cargarCursos() {
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

