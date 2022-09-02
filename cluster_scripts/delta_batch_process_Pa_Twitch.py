
import pathlib
import delta.config as cfg
from delta.utilities import xpreader
from delta.pipeline import Pipeline
import tensorflow as tf

dev = tf.config.list_physical_devices()
print(dev)

def to_str(posixpath):
    return str(posixpath.resolve())   

#set paths
root = pathlib.Path(pathlib.Path.home(), 'home', 'Delta2_Caulobacter')
data_dir = root / 'Twitching' 

#create output dir
output_path = root / 'processed_dataTwitching'
(output_path).mkdir(exist_ok=True) #create output data folder,  each position will be placed in a subfolder

#get config file
config_file = root / 'config_2D_caulobacter.json'
cfg.load_config(config_file)
cfg.model_file_seg = to_str(root / 'models' / 'unet_pads_seg.hdf5') 
cfg.save_format = ('pickle','movie')


movie_names = [f.name for f in sorted((data_dir).glob('*.tif*'))]


for movie in movie_names:        
    #path to current position
    movie_dir = data_dir / movie
    
    #make nickname of movei (adapt to file name structure, here we take the part starting at TL and stopping before __R3D)
    start = movie.find('TL')
    end = movie.find('_R3D', start)
    movie_name_short = movie[start:end]
    
    #make subfolder for current position
    output_dir = output_path / movie_name_short
    (output_dir).mkdir(exist_ok=True)

    try:  
        print('starting with movie %s' %(movie_name_short)) 
        # Init reader (use bioformats=True if working with nd2, czi, ome-tiff etc):
        im_reader = xpreader(movie_dir) #, use_bioformats=True)

        # Print experiment parameters to make sure it initialized properly:
        print("""Initialized experiment reader:
            - %d positions
            - %d imaging channels
            - %d timepoints"""%(im_reader.positions, im_reader.channels, im_reader.timepoints)
        )

        # Init pipeline:
        xp = Pipeline(im_reader, resfolder=to_str(output_dir))   

        # Run pipeline
        xp.process()
        
    except:
        print('error with movie %s, skipping to next' %(movie_name_short)) 


#exit python
import os
os._exit(os.EX_OK)
