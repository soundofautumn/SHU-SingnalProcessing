function my_bodeplot(Hw)
%   �������Դ��ݺ���Hwʵ�ֿ��ӻ���չʾ��ͬ��Ƶ������£����ݺ���Hw�������С
opts=bodeoptions;
opts.PhaseVisible = 'off';
opts.FreqScale = 'linear';
opts.MagUnits = 'abs';
bodeplot(Hw,opts)
grid
end

