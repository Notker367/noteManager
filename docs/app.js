document.querySelectorAll('.footer-line').forEach(button => {
    button.addEventListener('click', () => {
        const action = button.dataset.tgAction;
        if (action === 'showDailyMessage') {
            alert('Показать историю сообщений!');
        } else if (action === 'showTasks') {
            alert('Переход к странице задач.');
        } else if (action === 'showFinances') {
            alert('Переход к странице финансов.');
        }
    });
});
