// Main JavaScript for SGEA

// Auto-hide alerts after 5 seconds
document.addEventListener("DOMContentLoaded", function () {
  // Auto-hide alerts
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  // Confirmation for delete actions
  const deleteButtons = document.querySelectorAll("[data-confirm-delete]");
  deleteButtons.forEach(function (button) {
    button.addEventListener("click", function (e) {
      if (!confirm("Tem certeza que deseja excluir? Esta ação não pode ser desfeita.")) {
        e.preventDefault();
      }
    });
  });

  // Form validation feedback
  const forms = document.querySelectorAll(".needs-validation");
  forms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (!form.checkValidity()) {
        e.preventDefault();
        e.stopPropagation();
      }
      form.classList.add("was-validated");
    });
  });
});

// Função para copiar código de verificação
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(
    function () {
      alert("Código copiado para a área de transferência!");
    },
    function (err) {
      console.error("Erro ao copiar: ", err);
    }
  );
}
