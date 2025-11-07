/**
 * Audio Recorder Worklet
 */

let micStream;

// app/static/js/audio-recorder.js
export async function startAudioRecorderWorklet(audioRecorderHandler) {
  // Force 16kHz context
  const audioRecorderContext = new (window.AudioContext || window.webkitAudioContext)({
    sampleRate: 16000
  });

  // Load worklet
  const workletURL = new URL("./pcm-recorder-processor.js", import.meta.url);
  await audioRecorderContext.audioWorklet.addModule(workletURL);

  // Get mic stream (let browser choose, then resample via AudioContext)
  const micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const source = audioRecorderContext.createMediaStreamSource(micStream);

  const audioRecorderNode = new AudioWorkletNode(
    audioRecorderContext,
    "pcm-recorder-processor"
  );

  source.connect(audioRecorderNode);
  audioRecorderNode.port.onmessage = (event) => {
    const float32Data = event.data;
    // Convert to 16-bit PCM
    const int16Data = new Int16Array(float32Data.length);
    for (let i = 0; i < float32Data.length; i++) {
      int16Data[i] = Math.max(-32768, Math.min(32767, float32Data[i] * 32767));
    }
    audioRecorderHandler(int16Data.buffer);
  };

  return [audioRecorderNode, audioRecorderContext, micStream];
}

/**
 * Stop the microphone.
 */
export function stopMicrophone(micStream) {
  micStream.getTracks().forEach((track) => track.stop());
  console.log("stopMicrophone(): Microphone stopped.");
}

// Convert Float32 samples to 16-bit PCM.
function convertFloat32ToPCM(inputData) {
  // Create an Int16Array of the same length.
  const pcm16 = new Int16Array(inputData.length);
  for (let i = 0; i < inputData.length; i++) {
    // Multiply by 0x7fff (32767) to scale the float value to 16-bit PCM range.
    pcm16[i] = inputData[i] * 0x7fff;
  }
  // Return the underlying ArrayBuffer.
  return pcm16.buffer;
}
