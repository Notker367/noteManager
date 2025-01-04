// Проверяем доступность Telegram Web App API
if (window.Telegram && window.Telegram.WebApp) {
    const tg = window.Telegram.WebApp;

    // Инициализация Web App
    tg.ready();

    // Логируем данные о пользователе
    console.log("Пользователь:", tg.initDataUnsafe.user);

    // Добавляем обработчик события 'mainButton'
    tg.MainButton.text = "Подтвердить";
    tg.MainButton.color = "#008000"; // Зелёный цвет кнопки

    // Обработчик клика на MainButton
    tg.MainButton.onClick(() => {
        tg.showAlert("Кнопка нажата!");
    });

    // Включаем кнопку MainButton
    tg.MainButton.show();

    // Событие на закрытие Web App
    tg.onEvent("close", () => {
        console.log("Web App закрыт пользователем.");
    });

    // Добавляем взаимодействие с кнопкой на странице
    const actionButton = document.getElementById("actionButton");
    actionButton.addEventListener("click", () => {
        tg.sendData(JSON.stringify({
            action: "button_clicked",
            timestamp: Date.now()
        }));
        tg.showAlert("Данные отправлены в бот!");
    });
} else {
    console.error("Telegram Web App API недоступен.");
    alert("Telegram Web App API недоступен.");
}
