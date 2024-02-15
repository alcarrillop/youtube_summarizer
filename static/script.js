document.getElementById('youtube-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const youtubeUrl = document.getElementById('youtube-url').value;

    // Clear previous results
    clearPreviousResults();

    try {
        // Fetch and process metadata
        const metadataResponse = await fetchMetadata(youtubeUrl);
        if (metadataResponse && metadataResponse.message === "Metadata processed successfully") {
            updateMetadataDisplay(metadataResponse.metadata);
            const videoId = metadataResponse.metadata.video_id;

            // Fetch and process transcription
            const transcriptionResponse = await fetchTranscription(videoId);
            if (transcriptionResponse && transcriptionResponse.message === "Transcription processed successfully") {
                updateTranscriptionDisplay(transcriptionResponse.transcription);

                // Fetch and process summary
                const summaryResponse = await fetchSummary(videoId);
                if (summaryResponse && summaryResponse.message === "Summary processed successfully") {
                    updateSummaryDisplay(summaryResponse.summary);
                }
            }
        }
    } catch (error) {
        console.error('Error processing video data:', error);
        displayErrorMessage('Failed to process video data. Please try again.');
    }
});

async function fetchMetadata(youtubeUrl) {
    const response = await fetch('/metadata/', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `youtube_url=${encodeURIComponent(youtubeUrl)}`
    });
    return await response.json();
}

async function fetchTranscription(videoId) {
    const response = await fetch('/transcription/', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `video_id=${encodeURIComponent(videoId)}`
    });
    return await response.json();
}

async function fetchSummary(videoId) {
    const response = await fetch('/summary/', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `video_id=${encodeURIComponent(videoId)}`
    });
    return await response.json();
}


function updateMetadataDisplay(metadata) {
    document.getElementById('metadata-output').textContent = `Title: ${metadata.title}\nAuthor: ${metadata.author}\nPublish Date: ${metadata.publish_date}`;
}

function updateTranscriptionDisplay(transcription) {
    document.getElementById('transcription-output').textContent = transcription;
}

function updateSummaryDisplay(summary) {
    document.getElementById('summary-output').textContent = summary;
}

function clearPreviousResults() {
    document.getElementById('metadata-output').textContent = '';
    document.getElementById('transcription-output').textContent = '';
    document.getElementById('summary-output').textContent = '';
}


function displayErrorMessage(message) {
    // Implement a way to display error messages to the user
    console.error(message); // Placeholder for actual UI error handling
}
