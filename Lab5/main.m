% 读取音频文件和噪声文件
[x, Fs_x] = audioread('whknight.wav');
[noise_sine, ~] = audioread('sines.wav');
[noise_hfnoise,~] = audioread('hfnoise.wav');

% 添加噪声到原始信号
x_sine = x + noise_sine;
x_hfnoise = x + noise_hfnoise;

% 设置自适应滤波器参数
filterLength = 64; % 滤波器长度
stepSize = 0.01; % 步长，控制自适应程度

% 初始化自适应滤波器
d = x; % 期望输出为原始信号
mu = stepSize;
ha = dsp.LMSFilter('Length', filterLength, 'StepSize', mu);

% 使用自适应滤波器进行滤波
[y_sine, ~] = step(ha, x_sine, d);
[y_hfnoise, ~] = step(ha, x_hfnoise, d);

% 播放滤波前后的信号
%soundsc(x_sine, Fs_x); % 播放滤波前的x_sine
%pause(length(x_sine)/Fs_x); % 等待信号播放完成
%soundsc(y_sine, Fs_x); % 播放滤波后的y_sine
%pause(length(y_sine)/Fs_x); % 等待信号播放完成

%soundsc(x_hfnoise, Fs_x); % 播放滤波前的x_hfnoise
%pause(length(x_hfnoise)/Fs_x); % 等待信号播放完成
%soundsc(y_hfnoise, Fs_x); % 播放滤波后的y_hfnoise
