# Latency measurements: hand tracking module

## Measurement conditions

- **Machine:** DELL Inspiron 16+ running Linux Mint
- **Camera:** webcam, resolution: *1920 x 1080*. The driver reports 30 FPS (`CAP_PROP_FPS`).
- **Debug mode:** enabled (the overlay is drawn on every frame)
- **Initial measurements:** none discarded, so model loading is included in the statistics
- **Sessions:** one session per condition, 22 to 33 seconds each

### Definitions

- **Latency:** for each frame, the time between the call to `detect_async` and the moment the result arrives in the `on_result` callback. It is measured for every frame, and the table reports statistics over all frames of a session.
- **Frames lost:** frames sent minus results received.
- **Average FPS:** frames sent divided by the session duration. It measures the speed of the main loop, not the speed of the model.

### Scope of the measurement

This is the latency of the **tracking module only**. It does not include:

- camera capture, including the wait for the next image (see "Camera limitation" below)
- the BGR to RGB conversion and the creation of the MediaPipe image, which happen before the timestamp is taken
- audio synthesis and playback

The timestamp is truncated to an integer number of milliseconds, so the measured latency is overestimated by less than 1 ms.

## Results

| Condition | Mean (ms) | Median (ms) | Min (ms) | Max (ms) | 95th perc. (ms) | Frames sent | Frames received | Frames lost | Duration (s) | Average FPS |
|---|---|---|---|---|---|---|---|---|---|---|
| No hands, plugged in | 20.36 | 18.74 | 9.23 | 33.22 | 30.19 | 574 | 573 | 1 | 28.89 | 19.87 |
| Both hands, plugged in | 29.44 | 25.17 | 12.67 | 62.26 | 44.52 | 652 | 652 | 0 | 32.85 | 19.85 |
| No hands, on battery | 46.89 | 49.51 | 18.30 | 105.97 | 59.54 | 608 | 603 | 5 | 30.65 | 19.83 |
| Both hands, on battery | 88.47 | 90.30 | 28.52 | 147.13 | 128.82 | 439 | 327 | 112 | 22.18 | 19.79 |

Derived values:

| Condition | Frames lost (%) | Results per second |
|---|---|---|
| No hands, plugged in | 0.2 % | 19.8 |
| Both hands, plugged in | 0 % | 19.9 |
| No hands, on battery | 0.8 % | 19.7 |
| Both hands, on battery | 25.5 % | 14.7 |

## Analysis

We have only a few measurement sessions, but they already give some important information.

### Power source

Running on battery makes the latency 2 to 3 times higher. With both hands, the median goes from 25 ms (plugged in) to 90 ms (on battery), and the 95th percentile from 45 ms to 129 ms. In the worst case (both hands, on battery), about a quarter of the frames are lost, so the pitch can only change about 15 times per second, at irregular intervals.

Frames are lost only when the latency becomes higher than the interval between two camera images (about 50 ms). This is consistent with the model dropping new frames while it is still busy, but we have not verified this behavior directly.

The application should therefore be run **plugged in** (laptop) or on a **desktop PC**.

### Camera limitation

The main loop runs at about 19.8 FPS in all four conditions, even though the tracking latency changes by a factor of 4. A constant rate like this means that something imposes its rhythm on the whole loop. Timing the `cap.read()` call alone gives an average of about **50 ms**, which matches 20 FPS. The camera is therefore the limiting element, even though the driver reports 30 FPS (this value is declared by the driver, not measured).

A short test with extra light gave about 21 FPS on a sample of about 100 frames. This supports the idea that the camera lowers its frame rate in dim light, but the gain is small and the sample is limited, so the cause is suspected rather than proven. Forcing the MJPG format has not been tested yet.

For the end-to-end latency, this means that the interval of about 50 ms between camera images adds to the tracking latency, before the audio buffer is taken into account.

### Limitations

- Only one machine has been tested. Results can change from one machine to another, regarding performance, camera resolution and camera FPS cap.
- Each condition was measured once. An earlier session in the same condition (both hands, on battery) gave a median of about 66 ms, against 90 ms here, so the values vary from one session to another.
- The sessions are short, and the first frames (model loading) were not discarded, which can inflate the maximum.

### Recommendations and next steps

1. Run the application plugged in, in a well-lit room.
2. Repeat each condition several times and report the spread between sessions.
3. Record the camera resolution, and test whether forcing the MJPG format raises the real frame rate.
4. Combine these values with the audio latency to estimate the end-to-end latency.