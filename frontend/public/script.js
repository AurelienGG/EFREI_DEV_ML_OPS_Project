document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData();
    const imageInput = document.getElementById('imageInput');
    formData.append('file', imageInput.files[0]);

    // Simple fetch API call to your Flask endpoint
    fetch('http://localhost:8000/predict/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('prediction').textContent = data.predicted_name;
        console.log(data.class_probabilities)
        document.getElementById('predictionResult').classList.remove('hidden');
        // Smoothly reveal the prediction result
        document.getElementById('predictionResult').style.opacity = 0;
        setTimeout(() => {
            document.getElementById('predictionResult').style.opacity = 1;
        }, 10);
    })
    .catch(error => console.error('Error:', error));
});
