
const toggleButton = document.getElementById("toggle-button");
const leftPane = document.getElementById("left-pane");
const clock = document.getElementById("clock");

toggleButton.addEventListener("click", () => {
    leftPane.style.width = leftPane.style.width === "0px" ? "400px" : "0px";
    leftPane.style.padding = leftPane.style.padding === "10px" ? "20px" : "10px";
    toggleButton.style.left = toggleButton.style.left === "10px" ? "430px" : "10px";
});

// デジタル時計を更新する関数
function updateClock() {
    const now = new Date();
    const formattedDate = now.toLocaleDateString();
    const formattedTime = now.toLocaleTimeString();
    clock.textContent = `${formattedDate} ${formattedTime}`;
}

// 初回表示と1秒ごとに時計を更新
updateClock();
setInterval(updateClock, 1000);