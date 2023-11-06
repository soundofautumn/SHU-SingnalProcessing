function x = harmon(A, f, phi, Fs, T, L)
Ts = 1/Fs;
N = T*Fs;
t = (0:1:N-1)*Ts;
x = zeros(size(t));
for m=1:L
    x = x+ A(m)*sin(2*pi*m*f*t+phi(m));
end
plot(1:1:300,x(1:300))
sound(x,Fs);
end