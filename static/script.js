document.getElementById('youtube-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const youtubeUrl = document.getElementById('youtube-url').value;
    
    // Clear previous results
    document.getElementById('metadata-output').textContent = '';
    document.getElementById('transcription-output').textContent = '';
    document.getElementById('summary-output').textContent = '';

    try {
        const response = await fetch('/process-youtube-video/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `youtube_url=${encodeURIComponent(youtubeUrl)}`,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        // Populate the metadata, transcription, and summary sections
        document.getElementById('metadata-output').textContent = JSON.stringify(data.metadata, null, 2);
        document.getElementById('transcription-output').textContent = data.transcription;
        document.getElementById('summary-output').textContent = data.summary;
    } catch (error) {
        console.error('Error fetching video data:', error);
    }
});