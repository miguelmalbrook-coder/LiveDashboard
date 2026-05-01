document.addEventListener('DOMContentLoaded', () => {
    // 1. Splash Screen
    const splash = document.getElementById('splash-screen');
    window.addEventListener('load', () => {
        setTimeout(() => {
            splash.style.opacity = '0';
            splash.style.visibility = 'hidden';
        }, 500); // Small delay to ensure smooth transition after everything loads
    });

    // 2. Localization
    const langSwitcher = document.getElementById('langSwitcher');
    
    function updateTranslations(lang) {
        const t = translations[lang];
        if(!t) return;
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if(t[key]) {
                el.innerText = t[key];
            }
        });
    }

    langSwitcher.addEventListener('change', (e) => {
        updateTranslations(e.target.value);
    });

    // 2.5 Theme Toggle
    const themeToggleBtn = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme');
    
    // Default to light mode if no preference is set
    if (currentTheme === 'light' || !currentTheme) {
        document.body.classList.add('light-mode');
        if (!currentTheme) localStorage.setItem('theme', 'light');
    }

    themeToggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('light-mode');
        if (document.body.classList.contains('light-mode')) {
            localStorage.setItem('theme', 'light');
        } else {
            localStorage.setItem('theme', 'dark');
        }
    });

    // 3. Scroll Reveal Animations
    const reveals = document.querySelectorAll('.reveal');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if(entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, { threshold: 0.1 });
    
    reveals.forEach(reveal => observer.observe(reveal));

    // 3.5 Logo Visibility Logic
    const navLogo = document.getElementById('nav-logo');
    const heroLogoContainer = document.getElementById('hero-logo-container');
    
    if (navLogo && heroLogoContainer) {
        const logoObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Hero logo is visible, hide nav logo
                    navLogo.classList.remove('visible');
                } else {
                    // Hero logo is NOT visible, show nav logo
                    navLogo.classList.add('visible');
                }
            });
        }, { threshold: 0.1 });
        
        logoObserver.observe(heroLogoContainer);
    }

    // 4. Portfolio Data and Logic
    const portfolioData = [
        { id: 1, type: 'photography', sub: 'landscape', img: 'images/Abstract-Photography.jpeg', title: 'Abstract Photography', desc: 'A stunning abstract perspective captured through the lens, showcasing vibrant colors and dynamic lighting.' },
        { id: 2, type: 'digital', img: 'images/Digital Art.jpeg', title: 'Digital Art 1', desc: 'An imaginative digital piece exploring modern themes and futuristic aesthetics with bold turquoise accents.' },
        { id: 3, type: 'digital', img: 'images/Digital-Art (2).jpeg', title: 'Digital Art 2', desc: 'A vivid digital creation focusing on intricate details and a breathtaking holographic color palette.' },
        { id: 4, type: 'digital', img: 'images/Digital-Art (3).jpeg', title: 'Digital Art 3', desc: 'Surreal digital artwork that blends reality with fantasy, designed entirely using modern software tools.' },
        { id: 5, type: 'digital', img: 'images/Digital-Art (4).jpeg', title: 'Digital Art 4', desc: 'A conceptual piece that reflects the intersection of technology and natural forms.' },
        { id: 6, type: 'digital', img: 'images/Digital-Art (5).jpeg', title: 'Digital Art 5', desc: 'A vibrant character study rendered in stunning 3D using Blender and Adobe Photoshop.' },
        { id: 7, type: 'illustration', img: 'images/Illustration.jpeg', title: 'Illustration 1', desc: 'A hand-drawn vector illustration utilizing smooth curves and a pastel color scheme.' },
        { id: 8, type: 'illustration', img: 'images/Illustration (2).jpeg', title: 'Illustration 2', desc: 'A narrative-driven illustration designed to tell a story through visual depth and composition.' },
        { id: 9, type: 'illustration', img: 'images/Illustration (3).jpeg', title: 'Illustration 3', desc: 'Stylized character illustration highlighting unique fashion and modern graphic design principles.' },
        { id: 10, type: 'illustration', img: 'images/Illustration (4).jpeg', title: 'Illustration 4', desc: 'An abstract vector illustration created with Adobe Illustrator, featuring geometric harmony.' },
        { id: 11, type: 'photography', sub: 'portraits', img: 'images/Photgraphy2.jpeg', title: 'Photography 2', desc: 'A striking portrait capturing genuine emotion, framed perfectly against a soft backdrop.' },
        { id: 12, type: 'photography', sub: 'architect', img: 'images/Photography.jpeg', title: 'Photography 1', desc: 'Architectural photography focusing on leading lines and the structural elegance of modern buildings.' },
        { id: 13, type: 'photography', sub: 'product', img: 'images/Photography (2).jpeg', title: 'Photography 2', desc: 'Commercial product photography with crisp lighting to highlight the premium quality of the subject.' },
        { id: 14, type: 'photography', sub: 'landscape', img: 'images/Photography (3).jpeg', title: 'Photography 3', desc: 'A beautiful landscape photograph demonstrating the vastness and serenity of nature.' },
        { id: 15, type: 'photography', sub: 'portraits', img: 'images/Photography (4).jpeg', title: 'Photography 4', desc: 'An intimate portrait emphasizing the interplay between natural light and shadow.' },
        { id: 16, type: 'photography', sub: 'architect', img: 'images/Photography (5).jpeg', title: 'Photography 5', desc: 'Capturing the raw geometric beauty of urban architecture and glass facades.' },
        { id: 17, type: 'photography', sub: 'product', img: 'images/Photography (6).jpeg', title: 'Photography 6', desc: 'A clean, minimalist product shot designed for a high-end e-commerce campaign.' },
        { id: 18, type: 'photography', sub: 'landscape', img: 'images/Photography (7).jpeg', title: 'Photography 7', desc: 'A breathtaking sunset landscape showcasing vibrant orange and teal skies over the horizon.' },
        { id: 19, type: 'photography', sub: 'portraits', img: 'images/Photography (8).jpeg', title: 'Photography 8', desc: 'A creative portrait using unique angles and shallow depth of field.' }
    ];

    const portfolioGrid = document.getElementById('portfolio-grid');
    const photoSubFilters = document.getElementById('photo-sub-filters');
    
    // Modal Elements
    const modal = document.getElementById('gallery-modal');
    const modalImg = document.getElementById('modal-img');
    const modalTitle = document.getElementById('modal-title');
    const modalDesc = document.getElementById('modal-desc');
    const closeModal = document.querySelector('.close-modal');

    function openModal(item) {
        modalImg.src = item.img;
        modalTitle.innerText = item.title;
        modalDesc.innerText = item.desc;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }

    closeModal.addEventListener('click', () => {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    });

    function renderPortfolio(filterType, subFilterType = null) {
        portfolioGrid.innerHTML = '';
        portfolioData.forEach(item => {
            if (filterType === 'all' || 
               (filterType === 'photography' && item.type === 'photography' && (!subFilterType || item.sub === subFilterType)) ||
               (item.type === filterType && filterType !== 'photography')) {
                
                const div = document.createElement('div');
                div.className = 'portfolio-item';
                div.innerHTML = `
                    <img src="${item.img}" alt="${item.title}" loading="lazy">
                    <div class="portfolio-overlay">
                        <h3 style="color: white; margin:0;">${item.title}</h3>
                    </div>
                `;
                
                // Add click event to open modal
                div.addEventListener('click', () => openModal(item));
                
                portfolioGrid.appendChild(div);
            }
        });
    }

    renderPortfolio('all'); // Initial render

    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            const filter = e.target.getAttribute('data-filter');
            
            if (filter === 'photography') {
                photoSubFilters.classList.add('active');
                renderPortfolio('photography');
                document.querySelectorAll('.sub-filter-btn').forEach(b => b.classList.remove('active'));
            } else {
                photoSubFilters.classList.remove('active');
                renderPortfolio(filter);
            }
        });
    });

    document.querySelectorAll('.sub-filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.sub-filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            const subFilter = e.target.getAttribute('data-sub');
            renderPortfolio('photography', subFilter);
        });
    });

    // 5. Testimonial Data
    const testimonials = [
        { name: 'Sarah J.', text: '"Salomé delivered an outstanding logo for my brand. Her attention to detail is unmatched!"', rating: 5 },
        { name: 'Michel D.', text: '"The photoshoot was so professional. The pictures came out breathtaking."', rating: 5 },
        { name: 'Chloe T.', text: '"Great web design! Modern, responsive, and beautifully colored. Highly recommend."', rating: 5 },
        { name: 'David W.', text: '"A true artist. The poster design helped our event gain a lot of traction."', rating: 4 }
    ];

    const testimonyContainer = document.getElementById('testimony-container');
    testimonials.forEach(t => {
        const div = document.createElement('div');
        div.className = 'glass-card testimony-card';
        div.innerHTML = `
            <div class="stars">${'★'.repeat(t.rating)}${'☆'.repeat(5-t.rating)}</div>
            <p style="font-style: italic; margin-bottom: 15px;">${t.text}</p>
            <h4 style="color: var(--color-mint);">- ${t.name}</h4>
        `;
        testimonyContainer.appendChild(div);
    });

    // 6. Map Initialization (Anse Boileau, Mahe, Seychelles)
    // Coordinates for Anse Boileau: -4.7083, 55.4833
    const map = L.map('map').setView([-4.7083, 55.4833], 13);
    
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    L.marker([-4.7083, 55.4833]).addTo(map)
        .bindPopup('SOLOARTITUDE<br>Anse Boileau, Mahé.')
        .openPopup();
});
