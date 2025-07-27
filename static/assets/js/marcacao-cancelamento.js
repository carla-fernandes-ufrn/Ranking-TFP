function abrirPartida(partidaId, nome1, nome2) {
  $('#partidaIdPartida').val(partidaId);
    $('#jogadoresPartidaLabel').text(`${nome1} X ${nome2}`);

  // Limpa erros
  $('#partida-errors').html('');
  $('.text-danger').html('');

  // Limpa campos
  $('#dataPartida').val('');
  $('#localSelect').empty();

  // Carrega dados atuais da Partida
  $.get(`partida/get/${partidaId}/`, function(data) {
    if (data.local_id) {
      $('#localSelect').append(
        `<option value="${data.local_id}" selected>${data.local_nome}</option>`
      );
    }

    if (data.data) {
      console.log("Data ISO recebida:", data.data);

      // Garante formato: yyyy-MM-ddTHH:mm
      const dt = new Date(data.data);

      const year = dt.getFullYear();
      const month = String(dt.getMonth() + 1).padStart(2, '0');
      const day = String(dt.getDate()).padStart(2, '0');
      const hours = String(dt.getHours()).padStart(2, '0');
      const minutes = String(dt.getMinutes()).padStart(2, '0');

      const formatted = `${year}-${month}-${day}T${hours}:${minutes}`;

      console.log("Formatado para input:", formatted);

      $('#dataPartida').val(formatted);
    }

    // Opcional: Carregar lista de Locais
    $.get('partida/locais/', function(locais) {
      locais.forEach(function(local) {
        if (local.id != data.local_id) {
          $('#localSelect').append(`<option value="${local.id}">${local.nome}</option>`);
        }
      });
    });
  });

  var myModal = new bootstrap.Modal(document.getElementById('modalPartida'));
  myModal.show();
}

function salvarPartida() {
  const partidaId = $('#partidaIdPartida').val();
  $.ajax({
    url: `partida/save/${partidaId}/`,
    type: "POST",
    data: $('#partidaForm').serialize(),
    success: function(data) {
      $('#partida-errors').html('');
      $('.text-danger').html('');

      if (data.success) {
        bootstrap.Modal.getInstance(document.getElementById('modalPartida')).hide();
        location.reload();
      } else {
        if (data.errors['__all__']) {
          $('#partida-errors').html(`<div class="alert alert-danger">${data.errors['__all__'].join('<br>')}</div>`);
        }
        for (const [field, messages] of Object.entries(data.errors)) {
          if (field === '__all__') continue;
          $(`#error-${field}`).html(messages.join('<br>'));
        }
      }
    },
    error: function() {
      alert('Erro inesperado.');
    }
  });
}

function cancelarPartida() {
  const partidaId = $('#partidaIdPartida').val();
  $.post(`partida/cancelar/${partidaId}/`, {'csrfmiddlewaretoken': '{{ csrf_token }}'}, function(data) {
    if (data.success) {
      bootstrap.Modal.getInstance(document.getElementById('modalPartida')).hide();
      location.reload();
    } else {
      alert("Erro ao cancelar.");
    }
  });
}