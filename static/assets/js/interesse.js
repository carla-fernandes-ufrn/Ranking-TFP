function abrirModalInteresse(sorteioId) {
        var modalEl = document.getElementById('modalInteresse' + sorteioId);
        var modalInstance = new bootstrap.Modal(modalEl);
        modalInstance.show();
    }
  
  function salvarInteresse(sorteioId) {
    var quantidade = $('#quantidade_input_' + sorteioId).val();
    const form = document.getElementById('form-interesse-' + sorteioId);
    const url = form.dataset.urlSalvar;
    $.ajax({
      url: `interesses/salvar/`,
      type: "POST",
      // data: {
      //   'sorteio': sorteioId,
      //   'quantidade': quantidade
      // },
      data: $('#form-interesse-' + sorteioId).serialize(),
      success: function(data) {
        if (data.success) {
          var modalEl = document.getElementById('modalInteresse' + sorteioId);
          var modalInstance = bootstrap.Modal.getOrCreateInstance(modalEl);
          modalInstance.hide();

          $('#quantidade-exibida-' + sorteioId).text('Meus jogos: ' + data.quantidade);
          $('#total-pedidos-' + sorteioId).text('Total de pedidos: ' + data.total_pedidos + ' jogos');
        } else {
          alert("Erro: " + JSON.stringify(data.errors));
        }
      },
      error: function() {
        alert("Erro de conexão.");
      }
    });
  }