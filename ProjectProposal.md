**1\. Project Definition** This project aims to develop a real-time, computer vision-based musical instrument that translates human hand gestures into spatial audio control. Our application will be fully standalone, capturing video and synthesizing the audio. The exact scope focuses on a two-handed control scheme:

* **Pitch Control (Dominant Hand):** The vertical position (Y-axis) of the first hand will be mapped to discrete pitch generation, strictly bounded to a single octave (12 semitones) for this prototype. The camera frame will be divided into 12 horizontal zones.  
* **Volume Control (Non-Dominant Hand):** The vertical position (Y-axis) of the second hand will act as a spatial slider, dynamically adjusting the amplitude (volume) of the generated audio signal.  
* **Articulation (Hand Tracking):** The shape of the pitch-controlling hand will dictate the sound generation. A flat, open hand will trigger a single continuous wave, while a closed fist will trigger a full chord based on the root note of that Y-axis zone.

**2\. Preliminary Work Plan** Our general approach is to build a low-latency tracking pipeline that converts visual data into mathematical frequencies, generating and playing the audio waveforms dynamically in real-time.

**Software & Components:**

* **Input & Tracking:** We will use a standard webcam processed via **OpenCV** (`cv2`). Real-time hand landmark extraction (x, y coordinates and hand state) will be handled by **MediaPipe**.  
* **Audio Synthesis & Playback:** We will use **`numpy`** to mathematically generate the audio waveforms (e.g., sine or triangle waves for the notes and chords) based on the mapped frequencies. We will use the **`sounddevice`** or **`PyAudio`** Python libraries to stream these generated arrays to the computer's speakers with minimal buffer latency.  
* **Tutorials/References:** We plan to reference the official Google MediaPipe Hand Tracking documentation, as well as tutorials on real-time Digital Signal Processing (DSP) and audio generation in Python.

**Team Contributions:**

* **AUBRY Mathias:** Responsible for the OpenCV video capture, integrating the MediaPipe hand tracking model, and extracting reliable Y-coordinates and hand-state (fist vs. flat) classifications.  
* **CHENAL Hadrien :** Responsible for the mathematical mapping logic (translating coordinates into exact Hz frequencies for the 12-semitone octave and volume slider).  
* **ABD EL MEGUID Rayan:** Responsible for building the `numpy`/`sounddevice` audio engine to synthesize and play the frequencies dynamically, and conducting the formal accuracy and latency evaluations.

**3\. Evaluation Plan** To evaluate the gesture classification accuracy (fist vs. flat hand), we will utilize the **HaGRID (HAnd Gesture Recognition Image Dataset)**. HaGRID is exceptionally suitable for this task because it is one of the largest gesture datasets available, featuring over 552,000 images across 18 distinct gesture classes under various lighting and background conditions, ensuring robust validation.

**Existing Baseline Result:** Current literature demonstrates that deep learning architectures (such as ResNet-34 or Graph Neural Networks) achieve up to 99.7% classification accuracy on the HaGRID dataset. We will use this high-end benchmark as a reference point for our system's hand-state recognition reliability.

**Evaluation Metrics:** Because this is a live musical application, our evaluation will be strictly twofold:

1. **Classification Accuracy (%):** Measuring how accurately the system identifies the fist versus flat hand state to successfully trigger the intended chord or single note without misfires.  
2. **System Latency (ms):** Measuring the end-to-end response time from the physical execution of a gesture on camera to the actual playback of the synthesized audio signal from the speakers. Keeping this audio buffer latency minimized is our primary technical hurdle for a viable musical instrument.

