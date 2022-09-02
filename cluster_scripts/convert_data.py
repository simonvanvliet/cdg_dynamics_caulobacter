#path handling
import pathlib
import numpy as np

#out of memory computation
from dask_image.imread import imread
import tifffile

#set root dir
root = pathlib.Path(pathlib.Path.home(), 'home', 'Delta2_Caulobacter', 'Twitching')
im_path = root / '20220830_PAO1wt_Twitching0.5Agar0.3Tryp.tif'

process_dir = root / 'tiffiles'
process_dir.mkdir(exist_ok=True)

#set number of color channels in image
n_channel = 3

im_stack = imread(im_path) #load image with dask-image for out of memory processing 
nframe = int(im_stack.shape[0]/n_channel)

newshape = (nframe, n_channel, *im_stack.shape[1:])
im_stack = im_stack.reshape(newshape)
    
nframe =  im_stack.shape[0]   
    
for fr in range(nframe):
    for ch in range(n_channel):
        
        imname = process_dir / ('pos0_ch%i_frm%.04i.tif' % (ch,fr))
        tifffile.imwrite(imname, np.squeeze(im_stack[fr,ch,:,:]))