uid = 'u2244509';
% 所有音频的采样频率都是44100
Fs = 44100;
[findme, ~] = get_tune(uid);
similarity = zeros(39, 1);
for i = 1:39
    filename = sprintf('rudenko_%02d.mp4', i);
    [audio, ~] = audioread(filename);
    convResult = conv(audio, flip(findme));
    similarity(i) = max(convResult);
    disp(i)
end
[~, index] = max(similarity);
disp(index)