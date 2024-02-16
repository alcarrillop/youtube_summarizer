document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('youtube-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevenir el comportamiento de envío predeterminado del formulario.
        const youtubeUrl = document.getElementById('youtube-url').value; // Obtener la URL ingresada por el usuario.

        try {
            const metadataResponse = await fetchMetadata(youtubeUrl); // Llamar a la función para obtener la metadata.
            if (metadataResponse && metadataResponse.metadata) {
                updateMetadataDisplay(metadataResponse.metadata); // Actualizar el frontend con la metadata.
                
                // Proceder con la transcripción y el resumen.
                const videoId = metadataResponse.metadata.video_id;
                const transcriptionResponse = await fetchTranscription(videoId, youtubeUrl);
                updateTranscriptionDisplay(transcriptionResponse.transcription); // Actualizar el frontend con la transcripción.

                const summaryResponse = await fetchSummary(videoId, youtubeUrl);
                updateSummaryDisplay(summaryResponse.summary); // Actualizar el frontend con el resumen.
            } else {
                console.error('Metadata is missing in the response');
            }
        } catch (error) {
            console.error('Error processing video data:', error); // Manejar cualquier error que ocurra en la solicitud.
        }
    });
});

async function fetchMetadata(youtubeUrl) {
    // Realizar la solicitud POST al backend para obtener la metadata.
    const response = await fetch('/metadata/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `youtube_url=${encodeURIComponent(youtubeUrl)}` // Asegurarse de codificar la URL.
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`); // Lanzar un error si la respuesta no es exitosa.
    }
    return await response.json(); // Devolver la respuesta como JSON.
}

async function fetchTranscription(videoId, youtubeUrl) {
    toggleLoadingIndicator(true, 'transcription-text'); // Mostrar el indicador de carga
    try {
        const response = await fetch('/transcription/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `video_id=${encodeURIComponent(videoId)}&youtube_url=${encodeURIComponent(youtubeUrl)}`
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } finally {
        toggleLoadingIndicator(false, 'transcription-text'); // Ocultar el indicador de carga
    }
}

async function fetchSummary(videoId) {
    toggleLoadingIndicator(true, 'summary-text'); // Mostrar el indicador de carga
    try {
        const response = await fetch('/summary/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `video_id=${videoId}`
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } finally {
        toggleLoadingIndicator(false, 'summary-text'); // Ocultar el indicador de carga
    }
}

function updateMetadataDisplay(metadata) {
    // Actualizar el DOM con los valores de la metadata.
    document.getElementById('meta-title').textContent = metadata.title || 'Title not available';
    document.getElementById('meta-author').textContent = metadata.author || 'Author not available';
    document.getElementById('meta-publish-date').textContent = metadata.publish_date || 'Publish date not available';
}

function updateTranscriptionDisplay(transcription) {
    document.getElementById('transcription-text').textContent = transcription || 'Transcription not available';
}

function updateSummaryDisplay(summary) {
    document.getElementById('summary-text').textContent = summary || 'Summary not available';
}

function toggleLoadingIndicator(show, containerId) {
    const container = document.getElementById(containerId);
    if (show) {
        // Insertar el HTML del indicador de carga directamente
        container.innerHTML = '<div class="loading-indicator"></div>';
    } else {
        // Limpiar el contenedor para futuros datos
        container.innerHTML = '';
    }
}
