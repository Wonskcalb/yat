// JavaScript to toggle sidebar on scroll
window.addEventListener('scroll', function () {
    const sidebar = document.getElementById('sidebar');
    const horizontalSidebar = document.getElementById('horizontalSidebar');

    if (window.scrollY > 200) { // Adjust the scroll value based on when you want to toggle
        sidebar.style.display = 'none';
        horizontalSidebar.classList.remove('hidden');
    } else {
        sidebar.style.display = 'block';
        horizontalSidebar.classList.add('hidden');
    }
});
