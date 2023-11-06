% 读取音频文件
[y, Fs] = audioread('tel.wav');

y1=y(5500:6500);
N=length(y1);
Y1=fft(y1);
stem((-N/2:N/2-1)*(2*pi/N),real(fftshift(Y1)))