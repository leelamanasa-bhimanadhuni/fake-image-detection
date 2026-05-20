const fileInput = document.getElementById('file-input');
const dropZone = document.getElementById('drop-zone');
const previewContainer = document.getElementById('preview-container');
const imagePreview = document.getElementById('image-preview');
const uploadContent = document.querySelector('.upload-content');
const analyzeBtn = document.getElementById('analyze-btn');
const resultContainer = document.getElementById('result-container');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('error-message');
const resultLabel = document.getElementById('result-label');
const confidenceBar = document.getElementById('confidence-bar');
const confidenceScore = document.getElementById('confidence-score');

// Drag & Drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        showError('Please upload a valid image file.');
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        previewContainer.style.display = 'block';
        uploadContent.style.display = 'none';
        analyzeBtn.disabled = false;
        hideError();
        resultContainer.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

function removeImage() {
    fileInput.value = '';
    previewContainer.style.display = 'none';
    uploadContent.style.display = 'block';
    analyzeBtn.disabled = true;
    resultContainer.style.display = 'none';
    hideError();
}

function showError(msg) {
    errorMessage.textContent = msg;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

analyzeBtn.addEventListener('click', async () => {
    const file = fileInput.files[0] || (dropZone.files ? dropZone.files[0] : null); // Handle drop case if needed, but fileInput is main source usually. 
    // Actually, drag&drop usually doesn't set fileInput.files directly unless we do `fileInput.files = e.dataTransfer.files`.
    // Let's ensure file is available. 
    // Simplified: we used FileReader to show preview, but we need the file object for upload.
    // The current implementation of handleFile doesn't store the file object easily accessible if dropped.
    // Let's fix handleFile to update fileInput if possible or store in a variable.
    // Since fileInput.files is read-only, we can't set it easily (DataTransfer trick works).
});

// Improved handleFile for the button to work
let currentFile = null;

const originalHandleFile = handleFile;
handleFile = function (file) {
    currentFile = file;
    originalHandleFile(file);
}

analyzeBtn.addEventListener('click', async () => {
    if (!currentFile) return;

    loading.style.display = 'block';
    resultContainer.style.display = 'none';
    analyzeBtn.disabled = true;
    hideError();

    const formData = new FormData();
    formData.append('file', currentFile);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            displayResult(data);
        } else {
            showError(data.error || 'Something went wrong.');
        }
    } catch (err) {
        showError('Network error. Is the server running?');
    } finally {
        loading.style.display = 'none';
        analyzeBtn.disabled = false;
    }
});

function displayResult(data) {
    resultContainer.style.display = 'block';
    resultLabel.textContent = data.label;

    // Parse confidence string "98.5%" -> 98.5
    const confidenceVal = parseFloat(data.confidence);

    // Set color based on label
    if (data.label === 'Real') {
        resultLabel.style.color = 'var(--success)';
        confidenceBar.style.background = 'var(--success)';
    } else {
        resultLabel.style.color = 'var(--danger)';
        confidenceBar.style.background = 'var(--danger)';
    }

    confidenceScore.textContent = data.confidence;

    // Animate bar
    setTimeout(() => {
        confidenceBar.style.width = `${confidenceVal}%`;
    }, 100);
}
