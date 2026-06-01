document.addEventListener('DOMContentLoaded', function() {
    // 1. FUNCIONALIDADE DE BUSCA EM TEMPO REAL
    const searchInput = document.querySelector('.search-input');
    const serviceItems = document.querySelectorAll('.service-item');

    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const term = e.target.value.toLowerCase();

            serviceItems.forEach(item => {
                const label = item.querySelector('.service-label').textContent.toLowerCase();
                
                if (label.includes(term)) {
                    item.style.display = 'flex';
                    item.style.opacity = '1';
                } else {
                    item.style.display = 'none';
                    item.style.opacity = '0';
                }
            });
        });
    }

    // 2. ANIMAÇÃO DE ENTRADA (Reveal)
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    serviceItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        item.style.transition = 'all 0.6s ease-out';
        observer.observe(item);
    });

    // CSS Injetado para a animação
    const style = document.createElement('style');
    style.innerHTML = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);
});