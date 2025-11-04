document.addEventListener('DOMContentLoaded', function () {
    function showDeleteModal(movieId) {
        const modal = document.getElementById('deleteModal');
        modal.style.display = 'block';

        const confirmDeleteBtn = document.getElementById('confirmDelete');
        confirmDeleteBtn.onclick = function () {
            deleteMovie(movieId);
            modal.style.display = 'none';
        };
    }
    function hideDeleteModal() {
        const modal = document.getElementById('deleteModal');
        modal.style.display = 'none';
    }
    function deleteMovie(movieId) {
        fetch(`/delete/${movieId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => {
            if (response.ok) {
                const movieCard = document.getElementById(`movie-${movieId}`);
                if (movieCard) {
                    movieCard.remove();
                }
                alert('Filme deletado com sucesso!');
            } else {
                alert('Erro ao deletar o filme.');
            }
        }).catch(error => {
            console.error('Erro:', error);
        });
    }
    const deleteButtons = document.querySelectorAll('.delete-button');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            const movieId = this.dataset.id;
            showDeleteModal(movieId);
        });
    });
    const closeModal = document.getElementById('closeModal');
    closeModal.addEventListener('click', hideDeleteModal);

    function updateMovieList() {
        fetch('/')
            .then(response => response.text())
            .then(html => {
                document.getElementById('movies-list').innerHTML = html;
            })
            .catch(error => {
                console.error('Erro ao atualizar a lista de filmes:', error);
            });
    }
});
