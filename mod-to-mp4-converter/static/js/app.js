/**
 * MOD to MP4 Converter - Frontend Application Logic
 */

// DOM Elements
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const convertBtn = document.getElementById('convertBtn');
const progressSection = document.getElementById('progressSection');
const progressBar = document.getElementById('progressBar');
const progressText = document.getElementById('progressText');
const statusContainer = document.getElementById('statusContainer');
const downloadBtn = document.getElementById('downloadBtn');

// State
let selectedFile = null;

/**
 * Initialize event listeners
 */
function init() {
    // Click to upload
    uploadZone.addEventListener('click', () => {
        fileInput.click();
    });

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop events
    uploadZone.addEventListener('dragover', handleDragOver);
    uploadZone.addEventListener('dragleave', handleDragLeave);
    uploadZone.addEventListener('drop', handleDrop);

    // Convert button
    convertBtn.addEventListener('click', handleConvert);

    // Prevent default drag behavior on document
    document.addEventListener('dragover', (e) => e.preventDefault());
    document.addEventListener('drop', (e) => e.preventDefault());
}

/**
 * Handle file selection via input
 */
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        validateAndSetFile(file);
    }
}

/**
 * Handle drag over event
 */
function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    uploadZone.classList.add('drag-over');
}

/**
 * Handle drag leave event
 */
function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
    uploadZone.classList.remove('drag-over');
}

/**
 * Handle file drop
 */
function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    uploadZone.classList.remove('drag-over');

    const files = event.dataTransfer.files;
    if (files.length > 0) {
        validateAndSetFile(files[0]);
    }
}

/**
 * Validate and set the selected file
 */
function validateAndSetFile(file) {
    // Check file extension
    const fileExtension = file.name.split('.').pop().toLowerCase();
    
    if (fileExtension !== 'mod') {
        showStatus('error', 'Invalid file type. Please select a .mod file.');
        return;
    }

    // Check file size (500MB limit)
    const maxSize = 500 * 1024 * 1024; // 500MB in bytes
    if (file.size > maxSize) {
        showStatus('error', 'File size exceeds 500MB limit. Please select a smaller file.');
        return;
    }

    // Set the file
    selectedFile = file;
    
    // Update UI
    fileName.textContent = file.name;
    fileInfo.classList.add('show');
    convertBtn.disabled = false;
    convertBtn.textContent = '✨ Convert to MP4';
    
    // Clear any previous status messages
    statusContainer.innerHTML = '';
    downloadBtn.classList.add('hidden');
    progressSection.classList.remove('show');

    // Add success animation
    fileInfo.style.animation = 'none';
    setTimeout(() => {
        fileInfo.style.animation = 'fadeIn 0.3s ease';
    }, 10);
}

/**
 * Get selected quality preset
 */
function getSelectedQuality() {
    const qualityRadios = document.querySelectorAll('input[name="quality"]');
    for (const radio of qualityRadios) {
        if (radio.checked) {
            return radio.value;
        }
    }
    return 'medium'; // Default
}

/**
 * Handle conversion process
 */
async function handleConvert() {
    if (!selectedFile) {
        showStatus('error', 'Please select a file first.');
        return;
    }

    // Disable convert button
    convertBtn.disabled = true;
    convertBtn.innerHTML = '<span class="spinner"></span> Converting...';

    // Hide download button and clear status
    downloadBtn.classList.add('hidden');
    statusContainer.innerHTML = '';

    // Show progress
    progressSection.classList.add('show');
    progressBar.style.width = '30%';
    progressText.textContent = 'Uploading and converting your video...';

    // Prepare form data
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('quality', getSelectedQuality());

    try {
        // Send request to server
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        // Update progress
        progressBar.style.width = '70%';

        const data = await response.json();

        if (response.ok && data.success) {
            // Success
            progressBar.style.width = '100%';
            progressText.textContent = 'Conversion complete!';
            
            setTimeout(() => {
                progressSection.classList.remove('show');
                showStatus('success', data.message || 'Video converted successfully!');
                
                // Setup download button
                downloadBtn.href = data.download_url;
                downloadBtn.download = data.filename;
                downloadBtn.classList.remove('hidden');
                
                // Reset convert button
                convertBtn.disabled = false;
                convertBtn.textContent = '✨ Convert Another File';
            }, 1000);
        } else {
            // Error from server
            throw new Error(data.error || 'Conversion failed');
        }
    } catch (error) {
        // Handle errors
        progressSection.classList.remove('show');
        showStatus('error', error.message || 'An error occurred during conversion. Please try again.');
        
        // Reset convert button
        convertBtn.disabled = false;
        convertBtn.textContent = '✨ Convert to MP4';
    }
}

/**
 * Show status message
 */
function showStatus(type, message) {
    const statusDiv = document.createElement('div');
    statusDiv.className = `status-message ${type}`;
    
    // Add icon based on type
    let icon = '';
    switch (type) {
        case 'success':
            icon = '✅ ';
            break;
        case 'error':
            icon = '❌ ';
            break;
        case 'info':
            icon = 'ℹ️ ';
            break;
    }
    
    statusDiv.textContent = icon + message;
    
    // Clear previous messages and add new one
    statusContainer.innerHTML = '';
    statusContainer.appendChild(statusDiv);
    
    // Scroll to status message
    statusDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Add smooth scroll animation to quality selection
 */
function initQualityAnimations() {
    const qualityLabels = document.querySelectorAll('.quality-label');
    
    qualityLabels.forEach((label, index) => {
        // Stagger animation on load
        label.style.opacity = '0';
        label.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            label.style.transition = 'all 0.5s ease';
            label.style.opacity = '1';
            label.style.transform = 'translateY(0)';
        }, 100 * index);
    });
}

/**
 * Check server health on load
 */
async function checkServerHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        
        if (!data.ffmpeg_available) {
            showStatus('error', 'FFmpeg is not installed on the server. Video conversion is currently unavailable.');
            convertBtn.disabled = true;
            convertBtn.textContent = 'FFmpeg Not Available';
        }
    } catch (error) {
        console.error('Health check failed:', error);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    init();
    initQualityAnimations();
    checkServerHealth();
});
