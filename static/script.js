let voices = [];

// Initialize the app
document.addEventListener('DOMContentLoaded', async () => {
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    document.getElementById('summarize-btn').addEventListener('click', generateSummary);
}

// Generate summary
async function generateSummary() {
    const urlInput = document.getElementById('youtube-url');
    const lengthSelect = document.getElementById('summary-length');
    const summarizeBtn = document.getElementById('summarize-btn');
    
    if (!urlInput.value.trim()) {
        showNotification('Please enter a YouTube URL.', 'warning');
        return;
    }
    
    const originalText = summarizeBtn.textContent;
    summarizeBtn.textContent = 'Generating Summary...';
    summarizeBtn.disabled = true;
    
    try {
        const response = await fetch('/api/summarize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                youtube_url: urlInput.value,
                length: lengthSelect.value
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate summary');
        }
        
        const data = await response.json();
        displaySummaryResult(data);
        showNotification('Summary generated successfully!', 'success');
        
    } catch (error) {
        console.error('Summary Error:', error);
        showNotification(error.message, 'error');
    } finally {
        summarizeBtn.textContent = originalText;
        summarizeBtn.disabled = false;
    }
}

// Display summary result
function displaySummaryResult(data) {
    const resultDiv = document.getElementById('summary-result');
    const videoInfoDiv = document.getElementById('video-info');
    const summaryText = document.getElementById('summary-text');
    const summaryAudio = document.getElementById('summary-audio');
    
    // Show video info
    if (data.video_info) {
        videoInfoDiv.innerHTML = `
            <div style="margin-bottom: 1rem; padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                <strong>Video:</strong> ${data.video_info.title || 'Unknown'}<br>
                <strong>Channel:</strong> ${data.video_info.uploader || 'Unknown'}
            </div>
        `;
    }
    
    // Show summary text
    summaryText.textContent = data.summary;
    
    // Show audio player
    summaryAudio.src = data.audio_url;
    
    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth' });
}

// Show notification
function showNotification(message, type = 'info') {
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease;
    `;
    
    const colors = {
        success: '#4cc9f0',
        error: '#f72585',
        warning: '#f9c74f',
        info: '#4361ee'
    };
    
    notification.style.backgroundColor = colors[type] || colors.info;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
`;
document.head.appendChild(style);