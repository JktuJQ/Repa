// Retractable profile window
profile_container = document.querySelector(".profile-container");
profile_small = document.querySelector(".profile-container").querySelector(".profile");
profile_small.addEventListener("click", function() {
    profile_container.querySelector(".profile-retractable").classList.toggle("active");
    profile_small.classList.toggle("border");
});

// Repa Clips
let isMuted = true;
const videos = document.querySelectorAll('.clips-grid video');
console.log(videos);
const videoContainer = document.querySelector(".clips-grid")

const togglePlayVideo = (video, shouldPlay, shouldRestart) => {
    console.log(shouldPlay);
    if (shouldPlay) return video.play();

    video.pause();
    if (shouldRestart)
        video.currentTime = 0;
}

const toggleMute = () => {
    isMuted = !isMuted;
    console.log(isMuted);
    videos.forEach(video => video.muted = isMuted);
}

const options = { root: document.querySelector(".clips-grid"), rootMargin: "-10%" };
const obeserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => togglePlayVideo(entry.target, entry.isIntersecting, true));
}, options);

videos.forEach(target => obeserver.observe(target));
videos.forEach(target => target.addEventListener("click", function() { togglePlayVideo(target, target.paused, false) }));

// Files validation
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('.file-input');
    const fileNameDisplay = document.getElementById('file-name');

    if (fileInput && fileNameDisplay) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                fileNameDisplay.textContent = this.files[0].name;
                fileNameDisplay.style.display = 'block';

                const maxSize = 100 * 1024 * 1024;
                if (this.files[0].size > maxSize) {
                    alert('Файл слишком большой');
                    this.value = '';
                    fileNameDisplay.textContent = 'Файл не выбран';
                    fileNameDisplay.style.display = '';
                }
            } else {
                fileNameDisplay.textContent = 'Файл не выбран';
                fileNameDisplay.style.display = '';
            }
        });

        // Drag and drop functionality
        const fileUploadLabel = document.querySelector('.file-upload-label');

        fileUploadLabel.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileUploadLabel.style.borderColor = '#1976d2';
            fileUploadLabel.style.backgroundColor = '#f0f5fd';
        });

        fileUploadLabel.addEventListener('dragleave', () => {
            fileUploadLabel.style.borderColor = '#ddd';
            fileUploadLabel.style.backgroundColor = 'transparent';
        });

        fileUploadLabel.addEventListener('drop', (e) => {
            e.preventDefault();
            fileUploadLabel.style.borderColor = '#ddd';
            fileUploadLabel.style.backgroundColor = 'transparent';

            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                const event = new Event('change');
                fileInput.dispatchEvent(event);
            }
        });
    }
});