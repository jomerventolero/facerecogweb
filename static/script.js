document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video_feed');

    if (video) {
        video.src = "{{ url_for('video_feed') }}";
    }
});
