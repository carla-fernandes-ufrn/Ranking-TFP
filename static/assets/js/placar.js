function abrirPlacar(partidaId, nome1, nome2) {
    document.getElementById('partidaId').value = partidaId;
    document.getElementById('jogadoresLabel').innerText = `${nome1} X ${nome2}`;
    document.getElementById('optionJogador1').innerText = nome1;
    document.getElementById('optionJogador2').innerText = nome2;

    ['set1j1','set1j2','tb1j1','tb1j2','set2j1','set2j2','tb2j1','tb2j2','superj1','superj2'].forEach(id => {
      document.getElementById(id).value = '';
    });

    document.getElementById('placar-errors').innerHTML = '';
    document.querySelectorAll('.text-danger').forEach(el => el.innerHTML = '');

    fetch(`/placar/get/${partidaId}/`)
      .then(response => response.json())
      .then(data => {
        if (data.set1jogador1 !== null) document.getElementById('set1j1').value = data.set1jogador1;
        if (data.set1jogador2 !== null) document.getElementById('set1j2').value = data.set1jogador2;
        if (data.tiebreak1jogador1 !== null) document.getElementById('tb1j1').value = data.tiebreak1jogador1;
        if (data.tiebreak1jogador2 !== null) document.getElementById('tb1j2').value = data.tiebreak1jogador2;
        if (data.set2jogador1 !== null) document.getElementById('set2j1').value = data.set2jogador1;
        if (data.set2jogador2 !== null) document.getElementById('set2j2').value = data.set2jogador2;
        if (data.tiebreak2jogador1 !== null) document.getElementById('tb2j1').value = data.tiebreak2jogador1;
        if (data.tiebreak2jogador2 !== null) document.getElementById('tb2j2').value = data.tiebreak2jogador2;
        if (data.supertiejogador1 !== null) document.getElementById('superj1').value = data.supertiejogador1;
        if (data.supertiejogador2 !== null) document.getElementById('superj2').value = data.supertiejogador2;

        document.getElementById('tb1Row').style.display = (data.tiebreak1jogador1 !== null || data.tiebreak1jogador2 !== null) ? 'flex' : 'none';
        document.getElementById('tb2Row').style.display = (data.tiebreak2jogador1 !== null || data.tiebreak2jogador2 !== null) ? 'flex' : 'none';
        document.getElementById('superRow').style.display = (data.supertiejogador1 !== null || data.supertiejogador2 !== null) ? 'flex' : 'none';
      });

    const myModal = new bootstrap.Modal(document.getElementById('modalPlacar'));
    myModal.show();
  }


document.addEventListener('DOMContentLoaded', function () {
    const woCheckbox = document.getElementById('woCheckbox');
    const woSelection = document.getElementById('woSelection');
    const setSection = document.getElementById('setSection');

    if (woCheckbox) {
      woCheckbox.addEventListener('change', function () {
        if (this.checked) {
          woSelection.style.display = 'block';
          setSection.style.display = 'none';
        } else {
          woSelection.style.display = 'none';
          setSection.style.display = 'block';
        }
      });
    }

    function toggleTiebreakRows() {
      const s1j1 = parseInt(document.getElementById('set1j1').value);
      const s1j2 = parseInt(document.getElementById('set1j2').value);
      const s2j1 = parseInt(document.getElementById('set2j1').value);
      const s2j2 = parseInt(document.getElementById('set2j2').value);

      document.getElementById('tb1Row').style.display = ((s1j1 === 7 && s1j2 === 6) || (s1j1 === 6 && s1j2 === 7)) ? 'flex' : 'none';
      document.getElementById('tb2Row').style.display = ((s2j1 === 7 && s2j2 === 6) || (s2j1 === 6 && s2j2 === 7)) ? 'flex' : 'none';

      const set1Winner = s1j1 > s1j2 ? 1 : s1j2 > s1j1 ? 2 : 0;
      const set2Winner = s2j1 > s2j2 ? 1 : s2j2 > s2j1 ? 2 : 0;

      const showSuperTie = set1Winner > 0 && set2Winner > 0 && set1Winner !== set2Winner;
      document.getElementById('superRow').style.display = showSuperTie ? 'flex' : 'none';
    }

    ['set1j1', 'set1j2', 'set2j1', 'set2j2'].forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('input', toggleTiebreakRows);
      }
    });
  });

function salvarPlacar() {
  const partidaId = $('#partidaId').val();
  const url = `/placar/save/${partidaId}/`;

  // Remove campos de tiebreak e supertie invisíveis antes de serializar
  const tb1Visible = $('#tb1Row').is(':visible');
  const tb2Visible = $('#tb2Row').is(':visible');
  const superVisible = $('#superRow').is(':visible');

  if (!tb1Visible) {
    $('#tb1j1').val('');
    $('#tb1j2').val('');
  }
  if (!tb2Visible) {
    $('#tb2j1').val('');
    $('#tb2j2').val('');
  }
  if (!superVisible) {
    $('#superj1').val('');
    $('#superj2').val('');
  }

  console.log("Enviando para:", url);

  $.ajax({
    url: url,
    type: "POST",
    data: $('#placarForm').serialize(),
    success: function(data) {
      $('#placar-errors').html('');
      $('.text-danger').html('');

      if (data.success) {
        bootstrap.Modal.getInstance(document.getElementById('modalPlacar')).hide();
        location.reload();
      } else {
        if (data.errors['__all__']) {
          $('#placar-errors').append(
            `<div class="alert alert-danger small mb-2">${data.errors['__all__'].join('<br>')}</div>`
          );
        }

        for (const [field, messages] of Object.entries(data.errors)) {
          if (field === '__all__') continue;
          $(`#error-${field}`).html(messages.join('<br>'));
        }
      }
    },
    error: function(xhr, status, error) {
      console.error("Falha:", error);
      alert("Erro inesperado.");
    }
  });
}
