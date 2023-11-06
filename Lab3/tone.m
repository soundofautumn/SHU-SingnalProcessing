function x = tone(A, f, phi, Fs, T, K)
Ts = 1/Fs;
N = T*Fs;
t = (0:1:N-1)*Ts;
x = zeros(size(t));
for i=1:K
    x = x+ A(i)*sin(2*pi*f(i)*t+phi(i));
end
end