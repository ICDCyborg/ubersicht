document.addEventListener("DOMContentLoaded", function () {
    const timerDisplay = document.getElementById("timer");
    const timerWrapper = document.getElementById("timer-wrapper");
    const startButton = document.getElementById("start");
    const pauseButton = document.getElementById("pause");
    const alarmSound = document.getElementById("alarm");

    let countdown;
    let isPaused = true;
    let remainingTime = 0; // 残り時間を追加

    // クエリパラメータからタイマーの分数を取得
    const urlParams = new URLSearchParams(window.location.search);
    const initialMinutes = parseInt(urlParams.get("timer")) || 10;
    timerDisplay.textContent = `${String(initialMinutes).padStart(2, '0')}:00`;

    function startTimer(minutes) {
        isPaused = false;
        timerWrapper.style.backgroundColor = "white"; // 背景色を白色に設定

        // タイマーが再開される場合、現在の残り時間を使用
        const endTime = Date.now() + (remainingTime || minutes * 60 * 1000);

        function updateTimer() {
            remainingTime = endTime - Date.now();

            if (remainingTime <= 0) {
                clearInterval(countdown);
                timerDisplay.textContent = "00:00";
                alarmSound.play();
            } else {
                const minutes = Math.floor(remainingTime / 1000 / 60);
                const seconds = Math.floor((remainingTime / 1000) % 60);
                timerDisplay.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            }
        }

        updateTimer();
        countdown = setInterval(updateTimer, 1000);
    }

    startButton.addEventListener("click", function () {
        if (isPaused) {
            startTimer(initialMinutes);
        }
    });

    pauseButton.addEventListener("click", function () {
        if (!isPaused) {
            clearInterval(countdown);
            isPaused = true;
            timerWrapper.style.backgroundColor = "lightyellow"; // 背景色を薄い黄色に設定
        }
    });
});
