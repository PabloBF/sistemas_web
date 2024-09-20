// INFO: Definindo a função makeEditable no escopo global
function makeEditable(postUrl, tableId) {
    // INFO: Adiciona uma coluna de ação para editar e deletar (exceto no thead)
    $('#' + tableId + ' tbody tr').each(function () {
        $(this).append('<td><a href="#" class="edit-row btn btn-sm btn-primary me-2"><i class="bx bx-edit"></i></a> <a href="#" class="delete-row btn btn-sm btn-danger"><i class="bx bx-trash"></i></a></td>');
    });

    // INFO: Manipulador de eventos para o botão de editar
    $('#' + tableId).on('click', '.edit-row', function (e) {
        e.preventDefault();
        var $row = $(this).closest('tr');
        var formHtml = '<form id="editForm">';

        // INFO: Itera sobre as células da linha para criar o formulário com os valores atuais
        $row.find('td').not(':last').each(function (index) {
            if ($(this).hasClass('noeditable')) {
                var thName = $('#' + tableId + ' th').eq(index).text().toLowerCase();
                var value = $(this).text();
                formHtml += '<input type="hidden" name="' + thName + '" value="'+value+'">';
                return;
            }

            var thName = $('#' + tableId + ' th').eq(index).text().toLowerCase();
            var value = $(this).text().trim();
            formHtml += '<div class="mb-3"><label class="form-label">' + thName + ':</label><input type="text" class="form-control" name="' + thName + '" value="'+value+'"></div>';
        });

        formHtml += '<button type="submit" class="btn btn-primary">Salvar</button></form>';
        // INFO: Exibe a popup de edição com o formulário gerado
        showModal('Editar Registro', formHtml);

        // INFO: Manipulador de eventos para o envio do formulário de edição
        $('#editForm').on('submit', function (e) {
            e.preventDefault();
            var formData = {};
            $(this).serializeArray().forEach(function (field) {
                formData[field.name] = field.value;
            });
            formData.tipo = 'edit';

            // INFO: Obtém o CSRF token antes de enviar os dados
            $.getJSON('/api/csrf-token', function (data) {
                formData.csrf_token = data.csrf_token;

                // INFO: Envia os dados do formulário via AJAX para o postUrl em formato JSON
                $.ajax({
                    url: postUrl,
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(formData),
                    success: function (response) {
                        // INFO: Lógica para lidar com a resposta do servidor após a edição
                        alert('Registro atualizado com sucesso.');
                        hideModal();
                        window.location.reload()
                    },
                    error: function () {
                        alert('Erro ao atualizar o registro.');
                    }
                });
            }).fail(function () {
                alert('Erro ao obter o CSRF token.');
            });
        });
    });

    // INFO: Manipulador de eventos para o botão de deletar
    $('#' + tableId).on('click', '.delete-row', function (e) {
        e.preventDefault();
        var $row = $(this).closest('tr');
        var id = $row.find('td:first').text();

        // INFO: Exibe a popup de confirmação para deletar
        var deleteHtml = `
            <p>Tem certeza que deseja deletar este registro?</p>
            <button id="confirmDelete" class="btn btn-danger">Deletar</button>`;
        showModal('Confirmar Deleção', deleteHtml);

        $('#confirmDelete').on('click', function () {
            // INFO: Obtém o CSRF token antes de enviar os dados
            $.getJSON('/api/csrf-token', function (data) {
                var postData = { id: id, tipo: 'delete', csrf_token: data.csrf_token };

                // INFO: Envia a solicitação de exclusão via AJAX para o postUrl em formato JSON
                $.ajax({
                    url: postUrl,
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(postData),
                    success: function (response) {
                        // INFO: Lógica para lidar com a resposta do servidor após a exclusão
                        alert('Registro deletado com sucesso.');
                        $row.remove();
                        hideModal();
                        window.location.reload()
                    },
                    error: function () {
                        alert('Erro ao deletar o registro.');
                    }
                });
            }).fail(function () {
                alert('Erro ao obter o CSRF token.');
            });
        });
    });

    // INFO: Função para exibir a modal com o conteúdo fornecido
    function showModal(title, content) {
        var modalHtml = `
            <div class="modal fade" data-bs-theme="dark" id="actionModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content bg-dark text-white">
                        <div class="modal-header">
                            <h5 class="modal-title">${title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            ${content}
                        </div>
                    </div>
                </div>
            </div>`;

        $('body').append(modalHtml);
        var modal = new bootstrap.Modal(document.getElementById('actionModal'));
        modal.show();

        $('#actionModal').on('hidden.bs.modal', function () {
            $(this).remove();
        });
    }

    // INFO: Função para ocultar a modal
    function hideModal() {
        var modalElement = document.getElementById('actionModal');
        var modal = bootstrap.Modal.getInstance(modalElement);
        modal.hide();
    }
}

function Novopost(postUrl) {
    // INFO: Constrói a estrutura HTML do modal
    var modalHtml = '<div class="modal" id="novoPostModal">';
    modalHtml += '<div class="modal-dialog">';
    modalHtml += '<div class="modal-content bg-dark text-white">';
    
    // INFO: Cabeçalho do Modal
    modalHtml += '<div class="modal-header">';
    modalHtml += '<h5 class="modal-title">Novo Item</h5>';
    modalHtml += '<button type="button" class="btn-close" data-bs-dismiss="modal"></button>';
    modalHtml += '</div>';
    
    // INFO: Corpo do Modal com os campos do formulário
    modalHtml += '<div class="modal-body">';
    modalHtml += '<form id="novoPostForm">';
    
    // INFO: Loop através dos argumentos passados, começando do segundo argumento
    for (var i = 1; i < arguments.length; i++) {
        var field = arguments[i];
        if (field && field.label && field.type && field.name) {
            modalHtml += '<div class="mb-3">';
            modalHtml += '<label class="form-label">' + field.label + '</label>';
            modalHtml += '<input type="' + field.type + '" class="form-control" name="' + field.name + '" />';
            modalHtml += '</div>';
        }
    }
    
    modalHtml += '</form>';
    modalHtml += '</div>';
    
    //INFO:  Rodapé do Modal
    modalHtml += '<div class="modal-footer">';
    modalHtml += '<button type="button" class="btn btn-primary" id="saveNovoPost">Salvar</button>';
    modalHtml += '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>';
    modalHtml += '</div>';
    modalHtml += '</div>';
    modalHtml += '</div>';
    modalHtml += '</div>';
    $('body').append(modalHtml);
    
    //INFO: Mostra o modal
    $('#novoPostModal').modal('show');
    
    //INFO: Lida com a ação de salvar
    $('#saveNovoPost').on('click', function() {
        // INFO:Cria um objeto de dados do formulário
        var formData = {};
        $('#novoPostForm').serializeArray().forEach(function(field) {
            formData[field.name] = field.value;
        });
        formData.tipo = 'novo';



        // INFO: Obtém o CSRF token antes de enviar os dados
        $.getJSON('/api/csrf-token', function (data) {
            formData.csrf_token = data.csrf_token;
            $.ajax({
                type: 'POST',
                url: postUrl,
                contentType: 'application/json',
                data: JSON.stringify(formData), 
                success: function(response) {

                    $('#novoPostModal').modal('hide');
                    alert('Adicionado com sucesso!');
                    window.location.reload()
                },
                error: function(xhr, status, error) {

                    alert('Erro ao salvar : ' + error);
                }
            });

 
        }).fail(function () {
            alert('Erro ao obter o CSRF token.');
        });
    

    });
}

