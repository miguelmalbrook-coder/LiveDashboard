document.addEventListener('DOMContentLoaded', () => {
    // 1. Splash Screen
    const splash = document.getElementById('splash-screen');
    setTimeout(() => {
        splash.style.opacity = '0';
        splash.style.visibility = 'hidden';
    }, 2500); // Wait 2.5 seconds to show off the premium animation

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

    // 4. Portfolio Data and Logic
    const portfolioData = [
        { id: 1, type: 'artwork', img: 'https://images.unsplash.com/photo-1543857778-c4a1a3e0b2eb?q=80&w=500&auto=format&fit=crop', title: 'Abstract Harmony' },
        { id: 2, type: 'photography', sub: 'landscape', img: 'https://images.unsplash.com/photo-1506744626753-eda8151a7471?q=80&w=500&auto=format&fit=crop', title: 'Mountain Vista' },
        { id: 3, type: 'photography', sub: 'portraits', img: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=500&auto=format&fit=crop', title: 'Urban Portrait' },
        { id: 4, type: 'poster', img: 'https://images.unsplash.com/photo-1557672172-298e090bd0f1?q=80&w=500&auto=format&fit=crop', title: 'Event Poster' },
        { id: 5, type: 'logo', img: 'https://images.unsplash.com/photo-1626785774573-4b799315345d?q=80&w=500&auto=format&fit=crop', title: 'Brand Identity' },
        { id: 6, type: 'digital', img: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=500&auto=format&fit=crop', title: 'Cyber City' },
        { id: 7, type: 'illustration', img: 'https://images.unsplash.com/photo-1578301978018-3005759f48f7?q=80&w=500&auto=format&fit=crop', title: 'Character Design' },
        { id: 8, type: 'web', img: 'https://images.unsplash.com/photo-1507238692062-110ce05f9401?q=80&w=500&auto=format&fit=crop', title: 'E-commerce UI' },
        { id: 9, type: 'photography', sub: 'architect', img: 'https://images.unsplash.com/photo-1511818966892-d7d671e672a2?q=80&w=500&auto=format&fit=crop', title: 'Modern Lines' },
        { id: 10, type: 'photography', sub: 'product', img: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=500&auto=format&fit=crop', title: 'Watch Commercial' },
    ];

    const portfolioGrid = document.getElementById('portfolio-grid');
    const photoSubFilters = document.getElementById('photo-sub-filters');
    
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
