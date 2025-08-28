// Tab switching functionality
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                // Remove active class from all tabs and content
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                
                // Add active class to clicked tab
                tab.classList.add('active');
                
                // Show corresponding content
                const tabId = tab.getAttribute('data-tab');
                document.getElementById(tabId).classList.add('active');
            });
        });
        
        // Simulate text-to-speech conversion
        document.getElementById('convert-btn').addEventListener('click', () => {
            const textInput = document.getElementById('text-input').value;
            
            if (textInput.trim() === '') {
                alert('Please enter some text to convert.');
                return;
            }
            
            // Show audio player (simulated)
            document.getElementById('audio-player').style.display = 'flex';
            
            // Simulate progress bar
            let width = 0;
            const progressBar = document.getElementById('progress');
            const interval = setInterval(() => {
                if (width >= 100) {
                    clearInterval(interval);
                } else {
                    width += 5;
                    progressBar.style.width = width + '%';
                }
            }, 100);
        });
        
        // Simulate play button
        document.getElementById('play-btn').addEventListener('click', () => {
            alert('Audio playback started (simulated).');
        });
        
        // Simulate download button
        document.getElementById('download-btn').addEventListener('click', () => {
            alert('Audio download started (simulated).');
        });
        
        // Simulate YouTube dubbing
        document.getElementById('generate-dub').addEventListener('click', () => {
            const url = document.getElementById('youtube-url').value;
            
            if (url.trim() === '') {
                alert('Please enter a YouTube URL.');
                return;
            }
            
            alert('Generating dub for: ' + url + ' (simulated)');
        });
        
        // Simulate summarization
        document.getElementById('summarize-btn').addEventListener('click', () => {
            const content = document.getElementById('summarize-input').value;
            
            if (content.trim() === '') {
                alert('Please enter text or a URL to summarize.');
                return;
            }
            
            alert('Generating summary (simulated).');
            
            // Simulate summary result
            document.querySelector('.summary-result p').textContent = 
                "This is a simulated summary of your content. The actual implementation would use NLP algorithms to analyze and condense the text into key points while maintaining the original meaning and important information.";
        });