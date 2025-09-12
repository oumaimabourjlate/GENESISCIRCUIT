HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PCB Defect Detector with Gemini Pro</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f2f5; /* Light grey background */
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
            color: #333;
        }
        .app-container {
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 960px; /* Wider container */
            display: flex;
            flex-direction: column;
            overflow: hidden; /* For rounded corners on children */
        }
        .header {
            background-color: #3f51b5; /* Deep blue header */
            color: white;
            padding: 20px 30px;
            text-align: center;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }
        .header h1 {
            margin: 0;
            font-size: 1.8em;
            font-weight: 500;
        }
        .header p {
            margin: 5px 0 0;
            font-size: 0.9em;
            opacity: 0.8;
        }
        .content-area {
            display: flex;
            flex-wrap: wrap; /* Allows wrapping on smaller screens */
            padding: 30px;
            gap: 30px; /* Space between columns */
        }
        .left-panel {
            flex: 2; /* Takes more space */
            min-width: 350px; /* Minimum width for the left panel */
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .right-panel {
            flex: 1; /* Takes less space */
            min-width: 300px; /* Minimum width for the right panel */
            background-color: #f8f9fa; /* Lighter background for analysis results */
            border-radius: 8px;
            padding: 25px;
            border: 1px solid #e0e0e0;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .button-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            transition: background-color 0.3s ease;
            flex-grow: 1;
        }
        .btn-primary {
            background-color: #007bff; /* Blue button */
            color: white;
        }
        .btn-primary:hover {
            background-color: #0056b3;
        }
        .btn-secondary {
            background-color: #6c757d; /* Grey button */
            color: white;
        }
        .btn-secondary:hover {
            background-color: #5a6268;
        }

        .upload-area {
            border: 2px dashed #ced4da; /* Light grey dashed border */
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            background-color: #ffffff;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 150px; /* Ensure some height for drop zone */
            flex-grow: 1; /* Allow it to take available space */
            position: relative; /* For file input overlay */
        }
        .upload-area:hover, .upload-area.dragover {
            border-color: #007bff;
            box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
        }
        .upload-area p {
            margin: 0;
            color: #6c757d;
            font-size: 1.1em;
        }
        #file-upload {
            opacity: 0; /* Hide the file input */
            position: absolute;
            width: 100%;
            height: 100%;
            cursor: pointer;
            top: 0;
            left: 0;
        }

        .image-preview {
            background-color: #e9ecef; /* Lighter grey background for image */
            border: 1px solid #ced4da;
            border-radius: 8px;
            min-height: 200px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden; /* To contain the image */
        }
        #uploaded-image {
            max-width: 100%;
            max-height: 400px; /* Limit max height */
            display: none; /* Hidden by default */
            border-radius: 7px; /* Slightly smaller than parent for visual effect */
        }
        #no-image-placeholder {
            color: #6c757d;
            font-style: italic;
            display: block; /* Visible by default */
        }

        /* Right Panel Styling */
        .right-panel h3 {
            color: #3f51b5; /* Deep blue heading */
            margin-top: 0;
            padding-bottom: 10px;
            border-bottom: 1px solid #e0e0e0;
            font-weight: 500;
        }
        .analysis-content {
            flex-grow: 1; /* Allows content to push down loader */
            display: flex;
            flex-direction: column;
            justify-content: center; /* Center loader vertically */
            align-items: center; /* Center loader horizontally */
            text-align: center;
        }
        .analysis-text-display {
            display: none; /* Hidden until results are available */
            line-height: 1.6;
            text-align: left;
            width: 100%; /* Take full width of parent */
        }
        .analysis-text-display p {
            margin-bottom: 10px;
        }

        .loader {
            border: 4px solid #f3f3f3; /* Light grey */
            border-top: 4px solid #3f51b5; /* Blue */
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            display: none; /* Hidden by default */
        }
        .loader-text {
            margin-top: 15px;
            color: #6c757d;
            display: none; /* Hidden by default */
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .content-area {
                flex-direction: column;
            }
            .left-panel, .right-panel {
                min-width: unset; /* Remove min-width on small screens */
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header">
            <h1>SOKA_GenesisCircuit</h1>
            <p>Upload a PCB image to identify potential defects.</p>
        </div>
        <div class="content-area">
            <div class="left-panel">
                <div class="button-group">
                    <label for="file-upload" class="btn btn-primary">Upload Image</label>
                    <button id="analyze-btn" class="btn btn-secondary" disabled>Analyze PCB</button>
                </div>
                <div class="upload-area" id="drop-zone">
                    <p>Drag & Drop your PCB image here</p>
                    <input id="file-upload" type="file" accept="image/*">
                </div>
                <div class="image-preview">
                    <img id="uploaded-image" src="#" alt="Uploaded PCB">
                    <span id="no-image-placeholder">No Image Selected</span>
                </div>
            </div>
            <div class="right-panel">
                <h3>Analysis Results</h3>
                <div class="analysis-content">
                    <div id="initial-message">Upload an image to start analysis.</div>
                    <div id="loader" class="loader"></div>
                    <div id="loader-text" class="loader-text">Analyzing, please wait...</div>
                    <div id="analysis-text" class="analysis-text-display"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const dropZone = document.getElementById('drop-zone');
        const fileInput = document.getElementById('file-upload');
        const analyzeBtn = document.getElementById('analyze-btn');
        const uploadedImage = document.getElementById('uploaded-image');
        const noImagePlaceholder = document.getElementById('no-image-placeholder');
        const loader = document.getElementById('loader');
        const loaderText = document.getElementById('loader-text');
        const initialMessage = document.getElementById('initial-message');
        const analysisText = document.getElementById('analysis-text');
        let currentFile = null;

        // Function to reset the analysis panel
        function resetAnalysisPanel() {
            loader.style.display = 'none';
            loaderText.style.display = 'none';
            analysisText.style.display = 'none';
            initialMessage.style.display = 'block';
            analysisText.innerHTML = '';
        }

        // --- File Input Change ---
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                currentFile = this.files[0];
                console.log('File selected:', currentFile.name);
                previewImage(currentFile);
                analyzeBtn.disabled = false; // Enable analyze button
                resetAnalysisPanel(); // Clear previous results
            } else {
                currentFile = null;
                uploadedImage.src = '#';
                uploadedImage.style.display = 'none';
                noImagePlaceholder.style.display = 'block';
                analyzeBtn.disabled = true; // Disable analyze button if no file
                resetAnalysisPanel();
            }
        });

        // --- Drag & Drop Handlers ---
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
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                currentFile = e.dataTransfer.files[0];
                console.log('File dropped:', currentFile.name);
                previewImage(currentFile);
                analyzeBtn.disabled = false; // Enable analyze button
                resetAnalysisPanel(); // Clear previous results
            }
        });

        // --- Image Preview ---
        function previewImage(file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                uploadedImage.src = e.target.result;
                uploadedImage.style.display = 'block';
                noImagePlaceholder.style.display = 'none';
            }
            reader.readAsDataURL(file);
        }

        // --- Analyze Button Click ---
        analyzeBtn.addEventListener('click', function() {
            if (currentFile) {
                console.log('Analyze button clicked for file:', currentFile.name);
                initialMessage.style.display = 'none';
                analysisText.style.display = 'none';
                loader.style.display = 'block';
                loaderText.style.display = 'block';
                analyzeBtn.disabled = true; // Disable during analysis
                
                const formData = new FormData();
                formData.append('file', currentFile);

                fetch('/analyze', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    console.log('Response status:', response.status);
                    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                    return response.json();
                })
                .then(data => {
                    console.log('Analysis data received:', data);
                    loader.style.display = 'none';
                    loaderText.style.display = 'none';
                    analysisText.innerHTML = data.analysis || '<p>No analysis result returned.</p>';
                    analysisText.style.display = 'block';
                    analyzeBtn.disabled = false; // Re-enable after analysis
                })
                .catch(error => {
                    console.error('Fetch error:', error);
                    loader.style.display = 'none';
                    loaderText.style.display = 'none';
                    analysisText.innerHTML = `<p style="color: #dc3545;">An error occurred: ${error.message}. Please try again.</p>`;
                    analysisText.style.display = 'block';
                    analyzeBtn.disabled = false; // Re-enable after error
                });
            } else {
                alert('Please upload an image first.');
            }
        });

        // Initialize state on page load
        resetAnalysisPanel();
        analyzeBtn.disabled = true; // Disable analyze button initially
    </script>
</body>
</html>
"""