function [echo] = myEcho(x, d, a)
    len=max(length(x)-d,d);
    echo=[flip(x(1:d,:)*a);zeros(len-d,1)]+[x(d+1:end,:);zeros(len-(length(x)-d),1)];
end