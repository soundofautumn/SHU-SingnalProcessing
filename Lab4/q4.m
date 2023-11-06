x1=sin(pi/10*(0:19)); 
x2=sin(pi/5*(0:19));
x3=sin(pi/2*(0:19));
x4=(-1).^(0:19);
x=[x1 x2 x3 x4];


y1=conv(flip(x),x1);
y2=conv(flip(x),x2);
y3=conv(flip(x),x3);
y4=conv(flip(x),x4);
y=y4;
stem(0:1:length(y)-1, y)