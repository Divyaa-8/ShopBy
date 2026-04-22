// app.js – Shopzy Django frontend helpers

// Auto-dismiss flash messages after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
  const msgs = document.querySelectorAll('.flash-msg');
  msgs.forEach(function (msg) {
    setTimeout(function () {
      msg.style.transition = 'opacity 0.5s ease';
      msg.style.opacity = '0';
      setTimeout(function () { msg.remove(); }, 500);
    }, 4000);
  });
});
