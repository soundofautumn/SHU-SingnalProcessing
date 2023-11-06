function x=lower_strength(input)
    x=input;
   for i=1:length(input)
       if(abs(input(i))>200)
           x(i)=0;
       end
   end
end