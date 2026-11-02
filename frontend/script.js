const startButton = document.getElementById("startCamera");
const cameraBox = document.querySelector(".camera-box");

let cameraStream = null;

startButton.addEventListener("click", async function () {
    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: true
        });

        cameraBox.innerHTML = "";

        const video = document.createElement("video");
        video.srcObject = cameraStream;
        video.autoplay = true;
        video.playsInline = true;

        video.style.width = "100%";
        video.style.height = "100%";
        video.style.objectFit = "cover";
        video.style.borderRadius = "10px";

        cameraBox.appendChild(video);

        startButton.textContent = "Camera Started";

    } catch (error) {
        alert("Unable to access camera. Please allow camera permission.");
        console.error(error);
    }
});