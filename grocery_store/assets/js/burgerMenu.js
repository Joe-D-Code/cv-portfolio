const burger = document.getElementById('burger-icon');
const menu  = document.getElementById('nav-links');

burger.addEventListener('click', () => {
  menu.classList.toggle('show');
});
