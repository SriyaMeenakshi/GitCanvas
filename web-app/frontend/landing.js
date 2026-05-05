// Theme management
const htmlElement = document.documentElement;
const themeToggleNav = document.getElementById('themeToggleNav');

// Load theme from localStorage or use system preference
function initTheme() {
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = savedTheme || (prefersDark ? 'dark' : 'light');
  htmlElement.setAttribute('data-theme', theme);
}

function toggleTheme() {
  const currentTheme = htmlElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  htmlElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
}

themeToggleNav.addEventListener('click', toggleTheme);

// Initialize theme on page load
initTheme();

// Smooth scroll behavior for navigation links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href !== '#' && document.querySelector(href)) {
      e.preventDefault();
      document.querySelector(href).scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });
    }
  });
});

// Intersection Observer for fade-in animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px',
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.feature, .showcase-item, .faq-item').forEach((el) => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = '0.6s ease-out';
  observer.observe(el);
});

// FAQ accordion interaction
const faqItems = document.querySelectorAll('.faq-item');
faqItems.forEach((item) => {
  item.addEventListener('click', () => {
    // Close other items
    faqItems.forEach((otherItem) => {
      if (otherItem !== item && otherItem.hasAttribute('open')) {
        otherItem.removeAttribute('open');
      }
    });
  });
});

// Parallax effect for floating cards
const floatingCards = document.querySelectorAll('.floating-card');
window.addEventListener('mousemove', (e) => {
  const x = e.clientX / window.innerWidth;
  const y = e.clientY / window.innerHeight;

  floatingCards.forEach((card, index) => {
    const offset = 20 * (index + 1);
    card.style.transform = `translate(${x * offset}px, ${y * offset}px)`;
  });
});

// Reset parallax on mouse leave
document.addEventListener('mouseleave', () => {
  floatingCards.forEach((card) => {
    card.style.transform = 'translate(0, 0)';
  });
});

console.log('Landing page initialized');
