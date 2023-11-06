x = zeros(1,20);
h = zeros(1,20);
for n=0:19
    x(n+1)=u(n-3)-u(n-8)-d(n-17);
    h(n+1)=-d(n)+2*d(n-1)-d(n-2);
end
y=conv(x,h);
stem(0:1:length(y)-1, y)