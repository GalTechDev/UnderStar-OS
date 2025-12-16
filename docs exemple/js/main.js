/**
 * ABM-Temp-Analyser - Main JavaScript
 * Navigation, animations et interactions
 */

document.addEventListener('DOMContentLoaded', function () {
    initNavigation();
    initHeroAnimation();
    initScrollAnimations();
    initArchitectureAnimation();
});

/**
 * Navigation fluide et effet de scroll
 */
function initNavigation() {
    const nav = document.querySelector('.nav');
    const navLinks = document.querySelectorAll('.nav-links a');

    // Effet de transparence au scroll
    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            nav.style.background = 'rgba(10, 10, 15, 0.95)';
        } else {
            nav.style.background = 'rgba(10, 10, 15, 0.9)';
        }
    });

    // Navigation fluide
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Highlight du lien actif
    const sections = document.querySelectorAll('section[id]');

    window.addEventListener('scroll', function () {
        let current = '';

        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.offsetHeight;

            if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.style.color = '#e8e8ec';
            } else {
                link.style.color = '#9ca3af';
            }
        });
    });
}

/**
 * Animation de la température dans le hero
 */
function initHeroAnimation() {
    const tempDisplay = document.getElementById('hero-temp');
    if (!tempDisplay) return;

    const targetTemp = -77;
    const startTemp = 20;
    const duration = 2000;
    const startTime = performance.now();

    function animate(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Easing: ease-out cubic
        const easeProgress = 1 - Math.pow(1 - progress, 3);

        const currentTemp = Math.round(startTemp + (targetTemp - startTemp) * easeProgress);
        tempDisplay.textContent = currentTemp;

        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    }

    // Démarrer l'animation quand la section est visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                requestAnimationFrame(animate);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    observer.observe(document.querySelector('.hero'));
}

/**
 * Animations au scroll (fade-in des éléments)
 */
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.card, .arch-node, .timeline-item, .code-viewer, .chart-container, .simulator-controls, .result-box');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';

                setTimeout(() => {
                    entry.target.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);

                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    animatedElements.forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
}

/**
 * Animation des nœuds d'architecture au survol
 */
function initArchitectureAnimation() {
    const archNodes = document.querySelectorAll('.arch-node');
    const arrows = document.querySelectorAll('.arch-arrow');

    archNodes.forEach((node, index) => {
        node.addEventListener('mouseenter', function () {
            // Highlight ce nœud
            this.style.borderColor = '#00d4ff';
            this.style.boxShadow = '0 0 30px rgba(0, 212, 255, 0.3)';

            // Highlight les flèches adjacentes
            if (arrows[index - 1]) {
                arrows[index - 1].style.color = '#00d4ff';
                arrows[index - 1].style.textShadow = '0 0 10px rgba(0, 212, 255, 0.5)';
            }
            if (arrows[index]) {
                arrows[index].style.color = '#00d4ff';
                arrows[index].style.textShadow = '0 0 10px rgba(0, 212, 255, 0.5)';
            }
        });

        node.addEventListener('mouseleave', function () {
            this.style.borderColor = 'rgba(255, 255, 255, 0.1)';
            this.style.boxShadow = 'none';

            arrows.forEach(arrow => {
                arrow.style.color = '#00d4ff';
                arrow.style.textShadow = 'none';
            });
        });
    });

    // Animation séquentielle au chargement
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                archNodes.forEach((node, index) => {
                    setTimeout(() => {
                        node.style.transform = 'scale(1.05)';
                        node.style.borderColor = '#00d4ff';

                        setTimeout(() => {
                            node.style.transform = 'scale(1)';
                            node.style.borderColor = 'rgba(255, 255, 255, 0.1)';
                        }, 200);
                    }, index * 150);
                });

                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    const archSection = document.querySelector('.architecture-diagram');
    if (archSection) {
        observer.observe(archSection);
    }
}

/**
 * Gestion du chargement des images
 */
function initImageLoading() {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

/**
 * Basculement du thème (optionnel)
 */
function toggleTheme() {
    document.body.classList.toggle('light-theme');
    localStorage.setItem('theme', document.body.classList.contains('light-theme') ? 'light' : 'dark');
}

// Vérification du thème sauvegardé
if (localStorage.getItem('theme') === 'light') {
    document.body.classList.add('light-theme');
}
