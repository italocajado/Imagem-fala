const video = document.getElementById('webcam');
const liveView = document.getElementById('liveView');
const demosSection = document.getElementById('demos');
const enableWebcamButton = document.getElementById('webcamButton');
const reportSection = document.getElementById('report');

//Checkar o acesso a webcam
function getUserMediaSupported() {
  return !!(navigator.mediaDevices &&
    navigator.mediaDevices.getUserMedia);
}

// Ativar camera
if (getUserMediaSupported()) {
  enableWebcamButton.addEventListener('click', enableCam);
} else {
  console.warn('getUserMedia() is not supported by your browser');
}

function enableCam(event) {
}

function enableCam(event) {
  // Prosseguir utilizando modelo de COCO-SSD e TensorFlow
  if (!model) {
    return;
  }
  
  event.target.classList.add('removed');  
  
  const constraints = {
    video: { facingMode: "environment" }
  };

  //mantendo a camera aberta
  navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
    video.srcObject = stream;
    video.addEventListener('loadeddata', predictWebcam);
  });
}

function predictWebcam() {
}

var model = true;
demosSection.classList.remove('invisible');

// Guardando os resultados.
var model = undefined;

//carregando modelo
cocoSsd.load().then(function (loadedModel) {
  model = loadedModel;
  demosSection.classList.remove('invisible');
});

var children = [];

function predictWebcam() {
  // Classificando.
  model.detect(video).then(function (predictions) {
    // remover classificações anteriores para não poluir a tela.
    for (let i = 0; i < children.length; i++) {
      liveView.removeChild(children[i]);
    }
    children.splice(0);
    
    // Loop Entre as classificações e ecibição
    for (let n = 0; n < predictions.length; n++) {
      // Exibir objetos com mais de 40% de confiança!
      if (predictions[n].score > 0.40) {
        const p = document.createElement('p');
        p.innerText = predictions[n].class  + ' - com ' 
            + Math.round(parseFloat(predictions[n].score) * 100) 
            + '% Confiança.';
        p.style = 'margin-left: ' + predictions[n].bbox[0] + 'px; margin-top: '
            + (predictions[n].bbox[1] - 10) + 'px; width: ' 
            + (predictions[n].bbox[2] - 10) + 'px; top: 0; left: 0;';

        const highlighter = document.createElement('div');
        highlighter.setAttribute('class', 'highlighter');
        highlighter.style = 'left: ' + predictions[n].bbox[0] + 'px; top: '
            + predictions[n].bbox[1] + 'px; width: ' 
            + predictions[n].bbox[2] + 'px; height: '
            + predictions[n].bbox[3] + 'px;';

        liveView.appendChild(highlighter);
        liveView.appendChild(p);
        children.push(highlighter);
        children.push(p);
      }
    }
    
    // Loop dos passos anteriores.
    window.requestAnimationFrame(predictWebcam);
  });
}

const descricaoButton = document.getElementById('descricao');

// Criando a função de descrição da imagem
descricaoButton.addEventListener('click', () => {
  if (!model) {
    return;
  }

  // Pega o frame que esta em exibição
  model.detect(video).then(predictions => {
    for (let i = 0; i < children.length; i++) {
      liveView.removeChild(children[i]);
    }
    children.splice(0);

    for (let n = 0; n < predictions.length; n++) {
      // Reutilização do codigo anterior!
      if (predictions[n].score > 0.40) {
        const p = document.createElement('p');
        p.innerText = predictions[n].class  + ' - com ' 
            + Math.round(parseFloat(predictions[n].score) * 100) 
            + '% Confiança.';
        p.style = 'margin-left: ' + predictions[n].bbox[0] + 'px; margin-top: '
            + (predictions[n].bbox[1] - 10) + 'px; width: ' 
            + (predictions[n].bbox[2] - 10) + 'px; top: 0; left: 0;';

        const highlighter = document.createElement('div');
        highlighter.setAttribute('class', 'highlighter');
        highlighter.style = 'left: ' + predictions[n].bbox[0] + 'px; top: '
            + predictions[n].bbox[1] + 'px; width: ' 
            + predictions[n].bbox[2] + 'px; height: '
            + predictions[n].bbox[3] + 'px;';

        liveView.appendChild(highlighter);
        liveView.appendChild(p);
        children.push(highlighter);
        children.push(p);
      }
    }
  });
});

function generateReport(predictions) {
  let report = 'Relatório de objetos: \n\n';

  for (let n = 0; n < predictions.length; n++) {
    report += predictions[n].class + ' - com ' 
        + Math.round(parseFloat(predictions[n].score) * 100) 
        + '% de Confiança. \n';
  }

  // Converter o relatorio em fala
  const speech = new SpeechSynthesisUtterance(report);

  // configurando a linguagem.
  speech.lang = 'pt-BR';
  speech.pitch = 1.5;

  // Falando.
  window.speechSynthesis.speak(speech);

  reportSection.innerText = report;
}

descricaoButton.addEventListener('click', () => {
  model.detect(video).then(predictions => {
    generateReport(predictions);
  });
});