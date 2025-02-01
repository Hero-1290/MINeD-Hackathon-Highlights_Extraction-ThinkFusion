const video = document.getElementById("highlight-video");
const playPauseButton = document.getElementById("play-pause");
const seekBar = document.getElementById("seek-bar");
const currentTime = document.getElementById("current-time");
const duration = document.getElementById("duration");
const videoPlaylist = document.getElementById("video-playlist");

// Fetch videos from the "highlights" folder
async function fetchVideos() {
  try {
    const response = await fetch("/highlights"); // Replace with your server endpoint
    const files = await response.json();
    populateVideoList(files);
  } catch (error) {
    console.error("Error fetching videos:", error);
  }
}

// Populate video list
function populateVideoList(files) {
  files.forEach((file) => {
    const li = document.createElement("li");
    li.textContent = file.name;
    li.addEventListener("click", () => loadVideo(file.name)); // Pass only the file name
    videoPlaylist.appendChild(li);
  });
}

// Load selected video
function loadVideo(videoName) {
  const videoPath = `/highlights/${videoName}`; // Correct path to the video
  video.src = videoPath;
  video.load();
  video.play();
  playPauseButton.textContent = "Pause";
}

// Play/Pause Button
playPauseButton.addEventListener("click", () => {
  if (video.paused) {
    video.play();
    playPauseButton.textContent = "Pause";
  } else {
    video.pause();
    playPauseButton.textContent = "Play";
  }
});

// Seek Bar
video.addEventListener("timeupdate", () => {
  const value = (video.currentTime / video.duration) * 100;
  seekBar.value = value;
  currentTime.textContent = formatTime(video.currentTime);
});

seekBar.addEventListener("input", () => {
  const time = (seekBar.value / 100) * video.duration;
  video.currentTime = time;
});

// Format Time
function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${String(minutes).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
}

// Set Duration
video.addEventListener("loadedmetadata", () => {
  duration.textContent = formatTime(video.duration);
});

// Fetch videos on page load
fetchVideos();
