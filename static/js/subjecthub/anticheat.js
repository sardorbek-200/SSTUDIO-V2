// Oynadan chiqib ketishni (tab switch) kuzatish
document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
        alert("Qoida buzilishi qayd etildi! Jarima hisoblandi.");
        window.location.reload(); // Sahifani yangilab, jarayonni qaytadan boshlatadi
    }
});

// O‘ng tugmani bloklash
document.addEventListener('contextmenu', event => event.preventDefault());

// Tugmalar kombinatsiyasini bloklash (F12, Ctrl+Shift+I/J/C, Ctrl+U)
document.addEventListener('keydown', function(e) {
    if (e.key === "F12" || 
       (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'J' || e.key === 'C')) || 
       (e.ctrlKey && e.key === 'U')) {
        e.preventDefault();
        window.location.reload(); // Har qanday urinishda sahifani yangilash
        return false;
    }
});

// Konsol ochilganda avtomatik ishga tushadigan debugger
setInterval(() => {
    const threshold = 160; // Konsol uchun sezgirlik darajasi
    const widthThreshold = window.outerWidth - window.innerWidth > threshold;
    const heightThreshold = window.outerHeight - window.innerHeight > threshold;
    
    if (widthThreshold || heightThreshold) {
        window.location.reload();
    }
}, 1000);