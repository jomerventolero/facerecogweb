navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
        var videoElement = document.getElementById('video');
        videoElement.srcObject = stream;
    })
    .catch(function (error) {
        console.error('Error accessing webcam:', error);
    });
