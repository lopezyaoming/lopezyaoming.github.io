document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('axo-video');
    const scrollContainer = document.getElementById('scroll-container');

    const scrollSpeedFactor = 1000; // pixels per second of video
    const loops = 5;

    // Motion physics
    const accelerationFactor = 0.0025; // how much velocity we gain from scroll
    const friction = 0.9;              // friction applied per frame
    const easing = 0.1;                // how fast currentTime approaches targetTime

    let videoDuration = 0;
    let velocity = 0;
    let targetTime = 0;
    let currentTime = 0;
    let lastScrollY = window.scrollY;

    video.addEventListener('loadedmetadata', () => {
        videoDuration = video.duration;
        const scrollHeight = videoDuration * scrollSpeedFactor * loops;
        scrollContainer.style.height = `${scrollHeight}px`;

        video.pause();
        video.currentTime = 0;

        // Prime video
        video.play().then(() => video.pause());

        // Scroll input → velocity (accumulates on scroll)
        window.addEventListener('scroll', () => {
            const deltaY = window.scrollY - lastScrollY;
            lastScrollY = window.scrollY;

            velocity += deltaY * accelerationFactor;
        });

        const animate = () => {
            // Apply velocity to targetTime
            targetTime += velocity;

            // Clamp targetTime to loop cleanly
            targetTime = (targetTime % videoDuration + videoDuration) % videoDuration;

            // Smooth currentTime toward targetTime
            currentTime += (targetTime - currentTime) * easing;
            currentTime = (currentTime + videoDuration) % videoDuration;

            // Apply friction to velocity
            velocity *= friction;

            // Set video frame
            video.currentTime = currentTime;

            requestAnimationFrame(animate);
        };

        requestAnimationFrame(animate);
    });

    video.addEventListener('error', (e) => {
        console.error("Video error:", e);
    });

    video.load();
});
