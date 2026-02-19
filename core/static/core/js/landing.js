document.addEventListener('DOMContentLoaded', () => {
    const words = document.querySelectorAll('.rotating-word');
    let currentIndex = 0;

    const rotateWords = () => {
        // Remove active class from current word
        words[currentIndex].classList.remove('active');

        // Increment index
        currentIndex = (currentIndex + 1) % words.length;

        // Add active class to next word
        words[currentIndex].classList.add('active');
    };

    // Initialize first word
    if (words.length > 0) {
        words[0].classList.add('active');
        // Start interval
        setInterval(rotateWords, 1500);
    }

    // Dynamic Particle Background
    const createParticles = () => {
        const container = document.createElement('div');
        container.className = 'particles-container';
        document.querySelector('.hero-section').appendChild(container);

        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';

            const size = Math.random() * 4 + 1;
            const x = Math.random() * 100;
            const y = Math.random() * 100;
            const delay = Math.random() * 4;
            const duration = Math.random() * 3 + 2;

            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.left = `${x}%`;
            particle.style.top = `${y}%`;
            particle.style.animationDelay = `${delay}s`;
            particle.style.animationDuration = `${duration}s`;

            container.appendChild(particle);
        }
    };

    if (document.querySelector('.hero-section')) {
        createParticles();
    }
});
