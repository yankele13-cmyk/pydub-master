const socket = io.connect('http://' + location.hostname + ':' + location.port)
let textarea;
document.addEventListener('DOMContentLoaded', () => {
    textarea = document.querySelector('textarea');
    const csvpathInput = document.getElementById('csvFile')
    const voicepathInput = document.getElementById('audioFile')
    const outpathInput = document.getElementById('outputFolder')
    csvpathInput.addEventListener('click', () => window.pywebview.api.choose_file([['CSV files' ,'.csv']]).then((filePath) => csvpathInput.value = filePath));
    voicepathInput.addEventListener('click', () => window.pywebview.api.choose_file([['WAV files' ,'.wav']]).then((filePath) => voicepathInput.value = filePath));
    outpathInput.addEventListener('click', () => window.pywebview.api.choose_folder().then((folderPath) => outpathInput.value = folderPath));
    document.getElementById('runBtn').addEventListener('click', runTTS);
});

socket.on('progress', function(data) {
    document.getElementById('progressBar').firstElementChild.style.width = (data.downloaded) + '%';
    document.getElementById('progressText').textContent = `${Math.round(data.downloaded)}%`
});

socket.on('TTS_output', (data) => {
    let msg = data.output;
    if (msg.startsWith('\r')) {
        msg = msg.replace(/^\r+/, '');
        textarea.textContent = textarea.textContent.split('\n').pop().join('\n');
    }
    textarea.textContent += data.output + '\n';
    textarea.scrollTop = textarea.scrollHeight;
});

window.onload = function () {
    this.fetch('/check_model').then(res => res.json()).then(data => {if (!data.modelExists) installModel()}).catch(err => console.error('Error checking model: ' + err))
}

function installModel() {
    const modal = document.getElementById('loadingModal');
    modal.style.display = 'flex';
    fetch('/install_model', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            modal.style.display = 'none';
            alert(data.success ? "Model installed successfully!" : "Failed to install model: " + data.error);
        })
        .catch(err => {
            modal.style.display = 'none';
            alert("An error occured: " + err);
        });
}

function runTTS() {
    const csvFile = document.getElementById('csvFile').value;
    const audioFile = document.getElementById('audioFile').value;
    const outputFolder = document.getElementById('outputFolder').value;
    
    if (!csvFile || !audioFile || !outputFolder) {
        alert("Please select all files.");
        return;
    }

    const paths = {
        'csvFile': csvFile,
        'audioFile': audioFile,
        'outputFolder': outputFolder
    };

    window.pywebview.api.run_tts(paths).then((mes) => alert(mes));

    // fetch('/run_tts', {
    //     method: 'POST',
    //     headers: {'Content-Type': 'application/json'},
    //     body: paths
    // })
    // .then(response => response.json())
    // .then(data => {
    //     if (data.success) {
    //         alert("TTS conversion completed successfully!");
    //     } else {
    //         alert("TTS returned an error: " + data.error);
    //     }
    // });
}
