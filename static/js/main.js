document.addEventListener('DOMContentLoaded', () => {
    // Para alertas estilo fadeout automático
    const flashes = document.querySelectorAll('.animation-fade-in');
    if (flashes.length > 0) {
        setTimeout(() => {
            flashes.forEach(flash => {
                flash.style.opacity = '0';
                flash.style.transform = 'translateY(-10px)';
                flash.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                setTimeout(() => flash.remove(), 400);
            });
        }, 3500);
    }

    // Funcionalidad básica de lectura de notificaciones
    const notifButtons = document.querySelectorAll('.mark-read-btn');
    notifButtons.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const notifId = e.target.dataset.id;
            const row = document.getElementById(`notif-${notifId}`);
            try {
                const res = await fetch(`/notifications/read/${notifId}`, { method: 'POST' });
                if (res.ok) {
                    row.classList.remove('bg-gingerfizz-50');
                    e.target.remove(); // Removes the "Marcar" button
                    
                    // Comprobar si hay más notifs no leídas
                    const remainingBtns = document.querySelectorAll('.mark-read-btn');
                    if (remainingBtns.length === 0) {
                        const badge = document.getElementById('notifBadge');
                        if (badge) badge.classList.add('hidden');
                    }
                }
            } catch (err) {
                console.error("Error al marcar como leído:", err);
            }
        });
    });

    // Cierra el centro de notificaciones si clickean afuera
    window.addEventListener('click', (e) => {
        const notifCenter = document.getElementById('notifCenter');
        if (notifCenter && !notifCenter.classList.contains('hidden')) {
            // Verificar si el click no ocurrió dentro del notifCenter O en el botón que lo abre
            if (!notifCenter.contains(e.target) && !e.target.closest('button[onclick*="notifCenter"]')) {
                notifCenter.classList.add('hidden');
            }
        }
    });
});
