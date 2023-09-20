document.addEventListener("DOMContentLoaded", function () {
    const timerDisplay = document.getElementById("timer");
    const timerWrapper = document.getElementById("timer-wrapper");
    const timerField = document.getElementById("timerField");
    const startButton = document.getElementById("start");
    const pauseButton = document.getElementById("pause");
    const alarmSound = document.getElementById("alarm");

    let countdown;
    let isPaused = true;
    let remainingTime = 0; // 残り時間を追加

    // クエリパラメータからタイマーの分数を取得
    const initialMinutes = parseInt(timerField.getAttribute("data-minutes")) || 10;
    timerDisplay.value = `${String(initialMinutes).padStart(2, '0')}:00`;

    function startTimer(minutes) {
        isPaused = false;
        timerDisplay.disabled = true;
        timerWrapper.style.backgroundColor = "white"; // 背景色を白色に設定
        
        // ユーザーの入力から残り秒数を計算
        const inputTime = timerDisplay.value.split(":");
        const inputMinutes = parseInt(inputTime[0]) || 0;
        const inputSeconds = parseInt(inputTime[1]) || 0;
        remainingTime = inputMinutes * 60 * 1000 + inputSeconds * 1000;
        const endTime = Date.now() + (remainingTime || minutes * 60 * 1000);

        function updateTimer() {
            remainingTime = endTime - Date.now();

            if (remainingTime <= 0) {
                clearInterval(countdown);
                timerDisplay.value = "00:00";
                alarmSound.play();
            } else {
                const minutes = Math.floor(remainingTime / 1000 / 60);
                const seconds = Math.floor((remainingTime / 1000) % 60);
                timerDisplay.value = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
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
            timerDisplay.disabled = false;
            timerWrapper.style.backgroundColor = "orange"; 
        }
    });
});
