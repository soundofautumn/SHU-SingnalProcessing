function [dst_img] = max_pooling(img,win_size)
fun = @(block_struct) max(block_struct.data(:));
X=win_size; Y=win_size; 
dst_img = blockproc (img, [X Y], fun);
end