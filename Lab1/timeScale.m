function [y,Fs] = timeScale(inputFile, outputFile, scaleFactor)
    [y,Fs] = audioread(inputFile);
    Fs = Fs * scaleFactor;
    audiowrite(outputFile,y,Fs);
end