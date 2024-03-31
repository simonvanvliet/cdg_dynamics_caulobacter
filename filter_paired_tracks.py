import numpy as np
import pandas as pd

def check_growth(len, min_dl, max_dl):
    """Check if change in length between frames stays within bounds

    Parameters
    ----------
    len : np.array
        length of cell over time
    min_dl : float
        lowest value of l(t+1)/l(t) that is allowed
    max_dl : float
        highest value of l(t+1)/l(t) that is allowed

    Returns
    -------
    Boolean
        True if  min_dl < l(t+1)/l(t) < max_dl for all t; false otherwise
    """
    dl = len[1:] / len[0:-1]
    return np.all(dl>min_dl) & np.all(dl<max_dl)


def filter_paired_tracks(movie, par_cell, filter_par, reason_skipped):
    """Filter pairs of tracks (2 daughter cells) based on criteria
    
    Filters pairs of sibling cell tracks based on criteria defined in filter_par.
    We start from parent cell and check if both offspring cells have been tracked for enough frames. Additionally, we check if the length change across division is within bounds and if the length change over time is within bounds. If a the cell pairs pass all criteria, they are classified in a cdg-high and a cdg-low cell based on their minimum cdg level. Both are added to a new DataFrame. If any check fails, the reason for skipping is recorded in reason_skipped.
    

    Parameters
    ----------
    movie : pd.DataFrame 
        grouped by DataFrame containing data of single position
    par_cell : pd.DataFrame 
        grouped by DataFrame containing data of single cell, whose offspring will be analyzed
    filter_par : dictionary
        dictionary with filter parameter
    reason_skipped : dictionary
        dictionary that tracks reason why cell was skipped 

    Returns
    -------
    pd.DataFrame or None
        If tracking passes all criteria output is a DataFrame containing paired data of both offspring cells of par_cell, else a None is returned 
    """
    
    #columns to copy
    cols = ['uni_par_id', 'strain', 'movie_name', 'replicate', 'id_colony', 
            'id_par', 'frames', 'generation', 'age']

    #init output
    new_df = None
    
    #check if division was tracked
    has_d1 = par_cell["id_d1"].iloc[0] > -1
    has_d2 = par_cell["id_d2"].iloc[0] > -1
    paired_lin = has_d1 & has_d2
    if not paired_lin: reason_skipped['division not tracked'] += 1

    if paired_lin:
        #get offspring cells
        d1_idx = movie['id_cell'] == par_cell["id_d1"].iloc[0]
        d2_idx = movie['id_cell'] == par_cell["id_d2"].iloc[0]
    
        #check if both offspring cells have been tracked for enough frames
        len_d1 = movie.loc[d1_idx, 'length']
        len_d2 = movie.loc[d2_idx, 'length']
        len_ok = (len_d1.size >= filter_par['min_num_frm']) & (len_d2.size >= filter_par['min_num_frm']) 
        if not len_ok: reason_skipped['too few frames'] +=1

        if len_ok:
            #check length change across division    
            # [l(offspring 1, t=0) +  l(offspring 2, t=0)] / l(mother, t=last)                   
            dl = (len_d1.iloc[0] + len_d2.iloc[0]) / par_cell['length'].iloc[-1]
            div_ok = (dl > filter_par['min_dl_div']) &  (dl < filter_par['max_dl_div'])
            if not div_ok: reason_skipped['dL error at div.'] +=1
            
            if div_ok:
                #crop movies to shortest length
                frms = np.arange(min(len_d1.size, len_d2.size))
                len_d1 = len_d1.iloc[frms].values 
                len_d2 = len_d2.iloc[frms].values
                
                #check length change over time  
                len_ok = check_growth(len_d1, filter_par['min_dl'], filter_par['max_dl']) & \
                        check_growth(len_d2, filter_par['min_dl'], filter_par['max_dl'])
                if not len_ok: reason_skipped['dL error'] +=1

                if len_ok:
                    #cell pair ok, process
                    reason_skipped['properly tracked'] +=1
                    
                    id_d1 = par_cell["id_d1"].iloc[0]
                    id_d2 = par_cell["id_d2"].iloc[0]
                    
                    #copy data frame   
                    cell_d1 = movie.loc[d1_idx, :]
                    new_df = cell_d1.iloc[frms, cell_d1.columns.get_indexer(cols)].reset_index(drop=True)
                    
                    #get fluorescent values of cdg
                    fluo_d1 = cell_d1[filter_par['cdg_ch']].iloc[frms].values 
                    fluo_d2 = movie.loc[d2_idx, filter_par['cdg_ch']].iloc[frms].values 

                    #calc fluorescence ratio
                    rel_fluor = fluo_d1 / fluo_d2
                    fluo_ratio = rel_fluor.mean()
                    
                    #order d1 and d2 based on cdg levels
                    d1_is_high = True if fluo_ratio>1 else False
                    
                    #normalize fluor
                    max_fluor = fluo_d1[0] if fluo_ratio>1 else fluo_d2[0]
                    fluo_d1_norm = fluo_d1 / max_fluor
                    fluo_d2_norm = fluo_d2 / max_fluor
                                        
                    #add new fields to df
                    new_df['cdg_dh'] =  fluo_d1 if d1_is_high  else fluo_d2
                    new_df['cdg_dl'] =  fluo_d2 if d1_is_high  else fluo_d1
                    new_df['cdg_norm_dh'] =  fluo_d1_norm if d1_is_high  else fluo_d2_norm
                    new_df['cdg_norm_dl'] =  fluo_d2_norm if d1_is_high  else fluo_d1_norm
                    new_df['len_dh'] =  len_d1 if d1_is_high  else len_d2
                    new_df['len_dl'] =  len_d2 if d1_is_high  else len_d1
                    new_df['idc_dh'] =  id_d1 if d1_is_high  else id_d2
                    new_df['idc_dl'] =  id_d2 if d1_is_high  else id_d1
                    new_df['rel_cdg_hl'] = 1/rel_fluor if d1_is_high else rel_fluor

    return new_df