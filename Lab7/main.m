[findme,Fs_s] = get_tune_slow('u7654321');
clip = resample(findme,8000,Fs_s);
window=64;
noverlap=32;
clip_s=spectrogram(clip,8000/1000*window,8000/1000*noverlap,8000/1000*window,8000);
clip_s=real(clip_s);
w_s=7;
correlation=zeros(1,39);
c_p=max_pooling(clip_s,w_s);
for i = 1:39
    filename = sprintf('rudenko_%02d.mp4', i);
    [y, ~] = audioread(filename);
    y=resample(y/max(y)*max(clip),8000,Fs_s);
    s=spectrogram(y,8000/1000*window,8000/1000*noverlap,8000/1000*window,8000);
    s=real(s);
    s_p=max_pooling(s,w_s);
    len=floor(size(s,2)/w_s-size(clip_s,2)/w_s);
    all_corr=zeros(1,len);

    for j=1:len
        s_p_part=s_p(:,j:j+floor(size(clip_s,2)/w_s));
        corr=corrcoef(c_p,s_p_part);
        all_corr(j)=corr(2,1);
    end
    
    [m,p]=max(all_corr);
    correlation(i)=max(all_corr);
end

[c,i]=max(correlation);
disp(i)

