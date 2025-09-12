HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PCB Defect Detector & Chatbot with Gemini</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f2f5;
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
            max-width: 1200px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .header {
            background-color: #3f51b5;
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
        .main-content {
            display: flex;
            flex-wrap: wrap;
            padding: 30px;
            gap: 30px;
        }
        .left-area {
            flex: 2;
            min-width: 400px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .right-area {
            flex: 1;
            min-width: 350px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .analysis-panel, .chatbot-panel {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 25px;
            border: 1px solid #e0e0e0;
            display: flex;
            flex-direction: column;
            gap: 20px;
            flex-grow: 1;
        }
        .analysis-panel h3, .chatbot-panel h3 {
            color: #3f51b5;
            margin-top: 0;
            padding-bottom: 10px;
            border-bottom: 1px solid #e0e0e0;
            font-weight: 500;
        }
        .button-group {
            display: flex;
            gap: 10px;
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
            background-color: #007bff;
            color: white;
        }
        .btn-primary:hover {
            background-color: #0056b3;
        }
        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }
        .btn-secondary:hover {
            background-color: #5a6268;
        }
        .upload-area {
            border: 2px dashed #ced4da;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            background-color: #ffffff;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 150px;
            flex-grow: 1;
            position: relative;
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
            opacity: 0;
            position: absolute;
            width: 100%;
            height: 100%;
            cursor: pointer;
            top: 0;
            left: 0;
        }
        .image-preview {
            background-color: #e9ecef;
            border: 1px solid #ced4da;
            border-radius: 8px;
            min-height: 200px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            flex-grow: 1;
        }
        #uploaded-image {
            max-width: 100%;
            max-height: 400px;
            display: none;
            border-radius: 7px;
        }
        #no-image-placeholder {
            color: #6c757d;
            font-style: italic;
            display: block;
        }
        .analysis-content {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        .analysis-text-display {
            display: none;
            line-height: 1.6;
            text-align: left;
            width: 100%;
        }
        .analysis-text-display p {
            margin-bottom: 10px;
        }
        .loader {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3f51b5;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            display: none;
        }
        .loader-text {
            margin-top: 15px;
            color: #6c757d;
            display: none;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .chat-window {
            flex-grow: 1;
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            overflow-y: auto;
            max-height: 300px;
            margin-bottom: 15px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .chat-message {
            padding: 8px 12px;
            border-radius: 15px;
            max-width: 80%;
            word-wrap: break-word;
        }
        .chat-message.user {
            background-color: #007bff;
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 5px;
        }
        .chat-message.bot {
            background-color: #e2e6ea;
            color: #333;
            align-self: flex-start;
            border-bottom-left-radius: 5px;
        }
        .chat-input-area {
            display: flex;
            gap: 10px;
        }
        .chat-input-area input[type="text"] {
            flex-grow: 1;
            padding: 10px 15px;
            border: 1px solid #ced4da;
            border-radius: 5px;
            font-size: 1em;
        }
        .chat-input-area input[type="text"]:focus {
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
        }
        .chat-send-btn {
            background-color: #28a745;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .chat-send-btn:hover {
            background-color: #218838;
        }
        .chatbot-loader {
            display: none;
            align-self: flex-start;
            margin-top: 5px;
            font-size: 0.9em;
            color: #6c757d;
        }
        @media (max-width: 992px) {
            .main-content {
                flex-direction: column;
            }
            .left-area, .right-area {
                min-width: unset;
                width: 100%;
            }
            .right-area {
                flex-direction: column;
            }
            .chat-window {
                max-height: 250px;
            }
        }
        @media (max-width: 576px) {
            .header h1 {
                font-size: 1.5em;
            }
            .content-area, .main-content {
                padding: 15px;
                gap: 15px;
            }
            .btn {
                padding: 8px 15px;
                font-size: 0.9em;
            }
            .analysis-panel, .chatbot-panel {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header">
            <h1>SOKA_GenesisCircuit</h1>
            <p>PCB Defect Detector and QA Chatbot powered by Morocco AI.</p>
        </div>
        <div class="main-content">
            <div class="left-area">
                <div class="button-group">
                    <label for="file-upload" class="btn btn-primary">Upload PCB Image</label>
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
            <div class="right-area">
                <div class="analysis-panel">
                    <h3>Analysis Results</h3>
                    <div class="analysis-content">
                        <div id="initial-message">Upload an image to start analysis.</div>
                        <div id="loader" class="loader"></div>
                        <div id="loader-text" class="loader-text">Analyzing, please wait...</div>
                        <div id="analysis-text" class="analysis-text-display"></div>
                    </div>
                </div>
                <div class="chatbot-panel">
                    <h3>PCB QA Chatbot</h3>
                    <div class="chat-window" id="chat-window">
                        <div class="chat-message bot">Hello! I'm your PCB QA Chatbot. Ask me anything about PCBs, defects, or manufacturing processes.</div>
                    </div>
                    <div class="chatbot-loader" id="chatbot-loader">Typing...</div>
                    <div class="chat-input-area">
                        <input type="text" id="chat-input" placeholder="Ask a question...">
                        <button id="chat-send-btn" class="chat-send-btn">Send</button>
                    </div>
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

        const chatWindow = document.getElementById('chat-window');
        const chatInput = document.getElementById('chat-input');
        const chatSendBtn = document.getElementById('chat-send-btn');
        const chatbotLoader = document.getElementById('chatbot-loader');

        function resetAnalysisPanel() {
            loader.style.display = 'none';
            loaderText.style.display = 'none';
            analysisText.style.display = 'none';
            initialMessage.style.display = 'block';
            analysisText.innerHTML = '';
        }

        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                currentFile = this.files[0];
                console.log('File selected:', currentFile.name);
                previewImage(currentFile);
                analyzeBtn.disabled = false;
                resetAnalysisPanel();
            } else {
                currentFile = null;
                uploadedImage.src = '#';
                uploadedImage.style.display = 'none';
                noImagePlaceholder.style.display = 'block';
                analyzeBtn.disabled = true;
                resetAnalysisPanel();
            }
        });

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
                analyzeBtn.disabled = false;
                resetAnalysisPanel();
            }
        });

        function previewImage(file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                uploadedImage.src = e.target.result;
                uploadedImage.style.display = 'block';
                noImagePlaceholder.style.display = 'none';
            }
            reader.readAsDataURL(file);
        }

        analyzeBtn.addEventListener('click', function() {
            if (currentFile) {
                console.log('Analyze button clicked for file:', currentFile.name);
                initialMessage.style.display = 'none';
                analysisText.style.display = 'none';
                loader.style.display = 'block';
                loaderText.style.display = 'block';
                analyzeBtn.disabled = true;
                
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
                    analyzeBtn.disabled = false;
                })
                .catch(error => {
                    console.error('Fetch error:', error);
                    loader.style.display = 'none';
                    loaderText.style.display = 'none';
                    analysisText.innerHTML = `<p style="color: #dc3545;">An error occurred: ${error.message}. Please try again.</p>`;
                    analysisText.style.display = 'block';
                    analyzeBtn.disabled = false;
                });
            } else {
                alert('Please upload an image first.');
            }
        });

        function appendMessage(sender, message) {
            const messageElement = document.createElement('div');
            messageElement.classList.add('chat-message', sender);
            messageElement.innerHTML = message;
            chatWindow.appendChild(messageElement);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }

        async function sendMessage() {
            const userMessage = chatInput.value.trim();
            if (userMessage === '') return;

            appendMessage('user', userMessage);
            chatInput.value = '';
            chatbotLoader.style.display = 'block';
            chatSendBtn.disabled = true;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: userMessage })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                appendMessage('bot', data.response);
            } catch (error) {
                console.error('Chatbot fetch error:', error);
                appendMessage('bot', `<span style="color: #dc3545;">Error: ${error.message}. Please try again.</span>`);
            } finally {
                chatbotLoader.style.display = 'none';
                chatSendBtn.disabled = false;
                chatInput.focus();
            }
        }

        chatSendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        resetAnalysisPanel();
        analyzeBtn.disabled = true;
    </script>
</body>
</html>
"""