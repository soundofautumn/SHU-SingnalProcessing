notes
furelise
phi = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]*(pi/2);
F_sample = 16000;
len = length(na);
T=zeros(len);
x=[];
nak=[];
for k=1:10
    nak=[nak,1/((10+1-k)*pi)];
end
for k=1:len
    x = [x,harmon(nak,nf(k),phi,F_sample,TD/nd(k),10)];
end
sound(x,F_sample)
freq_evaluation(x,8000)