/**
 * Main JavaScript file for YouTube Downloader application.
 * Handles form submission, progress tracking, and UI updates.
 */

// DOM Elements
const downloadForm = document.getElementById('downloadForm');
const videoUrlInput = document.getElementById('videoUrl');
const formatRadios = document.querySelectorAll('input[name="format"]');
const videoQualityGroup = document.getElementById('videoQualityGroup');
const audioQualityGroup = document.getElementById('audioQualityGroup');
const videoQualitySelect = document.getElementById('videoQuality');
const audioQualitySelect = document.getElementById('audioQuality');
const filenameInput = document.getElementById('filename');
const infoBtn = document.getElementById('infoBtn');
const downloadBtn = document.getElementById('downloadBtn');
const videoInfoSection = document.getElementById('videoInfo');
const progressSection = document.getElementById('progressSection');
const messageBox = document.getElementById('messageBox');

// Progress elements
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const statusText = document.getElementById('statusText');
const speedText = document.getElementById('speedText');
const sizeText = document.getElementById('sizeText');
const etaText = document.getElementById('etaText');

// Video info elements
const videoThumbnail = document.getElementById('videoThumbnail');
const videoTitle = document.getElementById('videoTitle');
const videoUploader = document.getElementById('videoUploader');
const videoDuration = document.getElementById('videoDuration');
const videoViews = document.getElementById('videoViews');

// State
let progressInterval = null;
let isDownloading = false;

/**
 * Initialize event listeners
 */
function init() {
    // Format radio change handler
    formatRadios.forEach(radio => {
        radio.addEventListener('change', handleFormatChange);
    });
    
    // Info button handler
    infoBtn.addEventListener('click', handleGetInfo);
    
    // Form submit handler
    downloadForm.addEventListener('submit', handleDownload);
}

/**
 * Handle format selection change (video/audio)
 */
function handleFormatChange(event) {
    const format = event.target.value;
    
    if (format === 'audio') {
        videoQualityGroup.classList.add('hidden');
        audioQualityGroup.classList.remove('hidden');
    } else {
        videoQualityGroup.classList.remove('hidden');
        audioQualityGroup.classList.add('hidden');
    }
}

/**
 * Handle get video info button click
 */
async function handleGetInfo() {
    const url = videoUrlInput.value.trim();
    
    if (!url) {
        showMessage('Please enter a YouTube URL', 'error');
        return;
    }
    
    // Disable button
    infoBtn.disabled = true;
    infoBtn.textContent = 'Loading...';
    hideMessage();
    videoInfoSection.classList.add('hidden');
    
    try {
        const response = await fetch('/api/video-info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayVideoInfo(data.info);
        } else {
            showMessage(data.error || 'Failed to retrieve video information', 'error');
        }
    } catch (error) {
        showMessage('Network error: ' + error.message, 'error');
    } finally {
        infoBtn.disabled = false;
        infoBtn.textContent = 'Get Video Info';
    }
}

/**
 * Display video information
 */
function displayVideoInfo(info) {
    videoThumbnail.src = info.thumbnail;
    videoTitle.textContent = info.title;
    videoUploader.textContent = info.uploader;
    videoDuration.textContent = formatDuration(info.duration);
    videoViews.textContent = formatNumber(info.view_count);
    
    videoInfoSection.classList.remove('hidden');
}

/**
 * Format duration in seconds to MM:SS or HH:MM:SS
 */
function formatDuration(seconds) {
    if (!seconds) return 'N/A';
    
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${hours}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }
    return `${minutes}:${String(secs).padStart(2, '0')}`;
}

/**
 * Format large numbers with commas
 */
function formatNumber(num) {
    if (!num) return 'N/A';
    return num.toLocaleString();
}

/**
 * Handle download form submission
 */
async function handleDownload(event) {
    event.preventDefault();
    
    if (isDownloading) {
        showMessage('A download is already in progress', 'error');
        return;
    }
    
    const url = videoUrlInput.value.trim();
    const format = document.querySelector('input[name="format"]:checked').value;
    const quality = format === 'audio' 
        ? audioQualitySelect.value 
        : videoQualitySelect.value;
    const filename = filenameInput.value.trim();
    
    if (!url) {
        showMessage('Please enter a YouTube URL', 'error');
        return;
    }
    
    // Prepare UI
    isDownloading = true;
    downloadBtn.disabled = true;
    downloadBtn.textContent = 'Downloading...';
    hideMessage();
    progressSection.classList.remove('hidden');
    resetProgress();
    
    // Start progress tracking
    startProgressTracking();
    
    try {
        const response = await fetch('/api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url,
                type: format,
                quality,
                filename: filename || null
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showMessage(
                `✓ Download complete! File: ${data.filename}`,
                'success'
            );
            
            // Trigger file download
            triggerDownload(data.filename);
        } else {
            showMessage(data.error || 'Download failed', 'error');
        }
    } catch (error) {
        showMessage('Network error: ' + error.message, 'error');
    } finally {
        isDownloading = false;
        downloadBtn.disabled = false;
        downloadBtn.textContent = 'Download';
        stopProgressTracking();
    }
}

/**
 * Start polling for progress updates
 */
function startProgressTracking() {
    progressInterval = setInterval(async () => {
        try {
            const response = await fetch('/api/progress');
            const data = await response.json();
            
            if (response.ok) {
                updateProgress(data);
            }
        } catch (error) {
            console.error('Error fetching progress:', error);
        }
    }, 1000); // Poll every second
}

/**
 * Stop progress tracking
 */
function stopProgressTracking() {
    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }
}

/**
 * Update progress UI
 */
function updateProgress(data) {
    progressFill.style.width = `${data.percentage}%`;
    progressText.textContent = `${data.percentage.toFixed(1)}%`;
    statusText.textContent = data.status.charAt(0).toUpperCase() + data.status.slice(1);
    speedText.textContent = data.speed;
    sizeText.textContent = `${data.downloaded} / ${data.total}`;
    etaText.textContent = data.eta;
}

/**
 * Reset progress UI
 */
function resetProgress() {
    progressFill.style.width = '0%';
    progressText.textContent = '0%';
    statusText.textContent = 'Preparing...';
    speedText.textContent = 'N/A';
    sizeText.textContent = '0 MB / 0 MB';
    etaText.textContent = 'N/A';
}

/**
 * Trigger file download
 */
function triggerDownload(filename) {
    const link = document.createElement('a');
    link.href = `/api/download-file/${encodeURIComponent(filename)}`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

/**
 * Show message to user
 */
function showMessage(message, type = 'success') {
    messageBox.textContent = message;
    messageBox.className = `message-box ${type}`;
    messageBox.classList.remove('hidden');
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            hideMessage();
        }, 5000);
    }
}

/**
 * Hide message box
 */
function hideMessage() {
    messageBox.classList.add('hidden');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);
