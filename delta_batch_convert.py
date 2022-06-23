
import pathlib
import numpy as np
import pandas as pd
from delta_postprocess import delta_to_df 

#set paths
root = pathlib.Path(pathlib.Path.home(), 'home', 'Delta2_Caulobacter')
data_dir = root / 'data' / 'processed_data'
out_dir = root / 'output'
out_dir.mkdir(exist_ok=True)

csv_dir = out_dir / 'csv_files'
csv_dir.mkdir(exist_ok=True)


#find subfolders
folder_names = [f.name for f in sorted(data_dir.glob('AKS*'))]

df_list = []

for folder in folder_names:
    #get images in subfolder
    movie_names = [f.name for f in sorted((data_dir / folder).glob('*TL*'))]


    for idx, movie in enumerate(movie_names):        
        #path to current position        
        datafiles = [f.name for f in sorted((data_dir / folder / movie).glob('*.pkl'))]
        
        short_name = '%s_%s' %(folder,movie_name_short)
        
        #make nickname of movei (adapt to file name structure, here we take the part starting at TL and stopping before __R3D)
        start = movie.find('TL')
        end = movie.find('_R3D', start)
        movie_name_short = movie[start:end]
        
        pos_path = '/Users/simonvanvliet/I2ICourse/Project2B/ProcessedData/Position000000.pkl'
        df = delta_to_df(data_dir / folder / movie / datafiles[0])
        
        df['strain'] = folder
        df['movie_name'] = short_name
        df['replicate'] = idx
        
        df_list.append(df)
        
        #save data-frame
        save_name = short_name + '.csv'
        df.to_csv(csv_dir / save_name)



        
        #make subfolder for current position
        output_dir = output_path / movie_name_short

        try:  
            print('starting with movie %s->%s' %(folder,movie_name_short)) 
            # Init reader (use bioformats=True if working with nd2, czi, ome-tiff etc):
            im_reader = xpreader(movie_dir, use_bioformats=True)

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
            print('error with movie %s->%s, skipping to next' %(folder,movie_name_short)) 



