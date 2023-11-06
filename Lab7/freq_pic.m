[y,Fs_s] = audioread('rudenko_26.mp4');
clip = resample(y,8000,Fs_s);
window=64;
noverlap=32;
spectrogram(clip,8000/1000*window,8000/1000*noverlap,8000/1000*window,8000);