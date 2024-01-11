document.getElementById('youtube-form').onsubmit = async function(event) {
    event.preventDefault();

    const youtubeUrl = document.getElementById('youtube-url').value;
    const resultDiv = document.getElementById('result');

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
        document.getElementById('transcription-output').textContent = data.transcription;
        document.getElementById('summary-output').textContent = data.summary;

        // resultDiv.innerHTML = `
        //     <p><strong>Metadata:</strong> ${JSON.stringify(data.metadata)}</p>
        //     <p><strong>Transcription:</strong> ${data.transcription}</p>
        //     <p><strong>Summary:</strong> ${data.summary}</p>
        // `;
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        resultDiv.textContent = 'Error: Could not process video.';
    }
};
