document.querySelectorAll('.expand-button').forEach(button => {
    button.addEventListener('click', () => {
        const action = button.dataset.tgAction;
        console.log(`Mock action triggered: ${action}`);
        if (action === 'showDailyMessage') {
            alert('Показать историю сообщений!');
        } else if (action === 'showTasks') {
            alert('Переход к странице задач.');
        } else if (action === 'showFinances') {
            alert('Переход к странице финансов.');
        }
    });
});
