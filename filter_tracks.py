import numpy as np
import pandas as pd



def check_growth_crop(length, min_dl, max_dl):
    """Check if change in length between frames stays within bounds, return index of first frame that fails

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
        max_frm: index of first frame that fails the check
    """
    dl = length[1:] / length[0:-1]
    
    len_ok = np.logical_and(dl>min_dl, dl<max_dl)
    
    if np.all(len_ok):
        max_frm = length.size
    elif len_ok[0]:
        max_frm = np.argmax(np.logical_not(len_ok))
    else:
        max_frm = 0
    
    return max_frm



def filter_tracks(df, cur_cell, filter_par, reason_skipped):
    """Filter cell tracks based on criteria
    
    Filters individual cell tracks based on criteria defined in filter_par. Cells are checked for length consistency, number of frames, and division consistency. If a cell passes all criteria, it is copied to a new DataFrame, otherwise the reason for skipping is recorded in reason_skipped.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing data of all cells
    cur_cell : pd.DataFrame 
        grouped by DataFrame containing data of single cell
    filter_par : dictionary
        dictionary with filter parameter
    reason_skipped : dictionary
        dictionary that tracks reason why cell was skipped 

    Returns
    -------
    pd.DataFrame or None
        If tracking passes all criteria output is a DataFrame containing paired data of both offspring cells of cur_cell, else a None is returned 
    """
    
    #columns to copy
    cols = ['uni_id', 'strain', 'movie_name', 'replicate', 'id_colony', 
            'id_par', 'frames', 'generation', 'age', 'fluo1','fluo2','length']
    
    #init output
    new_df = None
    
    #check if cell has parent
    has_p = cur_cell["id_par"].iloc[0] > -1
    if not has_p: reason_skipped['division not tracked'] += 1

    if has_p:
        #check if cell has been tracked for enough frames
        frames_ok = cur_cell.shape[0] >= filter_par['min_num_frm']
        if not frames_ok: reason_skipped['too few frames'] +=1

        if frames_ok:
            #check length change over time  
            max_frm = check_growth_crop(cur_cell['length'].values, filter_par['min_dl'], filter_par['max_dl']) 
            len_ok = max_frm > filter_par['min_num_frm']
            if not len_ok: reason_skipped['dL error'] +=1
            
            if len_ok:
                #check length parent
                par_id = cur_cell["uni_par_id"].iloc[0]
                
                #relative length of parent just before division compared to cell after division 
                par_len = df[df['uni_id']==par_id]['length'].iloc[-1]
                rel_par_len = par_len / cur_cell["length"].iloc[0]                
                div_ok = (rel_par_len > filter_par['min_par_len']) and rel_par_len < filter_par['max_par_len']
                
                if not div_ok: reason_skipped['bad division'] +=1
                                
                if div_ok:
                    #cell ok, process
                    reason_skipped['properly tracked'] +=1
        
                    #copy data frame   
                    new_df = cur_cell[cols].reset_index(drop=True)
                    
                    #add new fields to df
                    new_df['cdg'] =  new_df[filter_par['cdg_ch']] 
                    new_df['cdg_rel'] =  new_df[f'fluo1'] / new_df[f'fluo2'] 
                    new_df = new_df[:filter_par['max_num_frm']]

    return new_df
