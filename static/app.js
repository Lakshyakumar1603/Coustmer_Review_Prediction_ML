// Scroll animations
document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('.section');

    const handleScroll = () => {
        sections.forEach(section => {
            const sectionPosition = section.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;

            // If the section is in view, add animation class
            if (sectionPosition < windowHeight - 100) {
                section.classList.add('fade-in');
            }
        });
    };

    // Listen for scroll event to trigger animation
    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Initialize the animations on page load
});
