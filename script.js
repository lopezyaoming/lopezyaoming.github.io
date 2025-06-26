document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM loaded. Initializing script.");
    const video = document.getElementById('axo-video');
    const scrollContainer = document.getElementById('scroll-container');

    // A factor to control playback speed vs scroll.
    // e.g. 1000 means 1 second of video for every 1000 pixels scrolled.
    const scrollSpeedFactor = 1000;

    // We need to wait for the video's metadata to load to get its duration.
    video.addEventListener('loadedmetadata', () => {
        console.log("Video metadata loaded.");
        console.log("Video duration:", video.duration, "seconds");

        // Set the height of the scroll container to be large enough for multiple loops.
        // Let's say 10 loops.
        const scrollHeight = (video.duration * scrollSpeedFactor) * 10;
        scrollContainer.style.height = `${scrollHeight}px`;
        console.log("Scroll container height set to:", scrollHeight, "px");

        // "Prime" the video for seeking
        video.play().then(() => {
            video.pause();
            // Initial update
            updateVideoTime();
        });

        // Function to update video time based on scroll
        const updateVideoTime = () => {
            const scrollPos = window.scrollY;
            let newTime = scrollPos / scrollSpeedFactor;
            console.log("Scroll position:", scrollPos, "New video time:", newTime);
            
            // Use modulo for looping
            if (video.duration) {
                video.currentTime = newTime % video.duration;
                // Force a redraw
                video.play().then(() => {
                    video.pause();
                });
            }
        };

        // Listen for scroll events
        window.addEventListener('scroll', updateVideoTime);
    });

    video.addEventListener('error', (e) => {
        console.error("Video error:", e);
    });

    // Ensure the video is ready to play.
    video.load();
    video.pause();
}); 