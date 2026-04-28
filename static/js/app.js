// Askıda Yemek - Ana JavaScript Dosyası

document.addEventListener('DOMContentLoaded', () => {
    console.log("Food Bridge Application Initialized");
    
    // Add smooth interactions and micro-animations
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mousedown', function() {
            this.style.transform = 'scale(0.95)';
        });
        btn.addEventListener('mouseup', function() {
            this.style.transform = '';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
});
