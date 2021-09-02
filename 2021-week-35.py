# Preppin' Data 2021 Week 35
import pandas as pd
import numpy as np

# Load data
pictures_df = pd.read_excel('unprepped_data\\PD 2021 Wk 35 Input.xlsx', sheet_name='Pictures')
frames_df = pd.read_excel('unprepped_data\\PD 2021 Wk 35 Input.xlsx', sheet_name='Frames')

# Split up the sizes of the pictures and the frames into lengths and widths
#  - Remember an inch is 2.54cm

# Split picture length and width from size and remove whitespace
pictures_df[['length', 'width']] = pictures_df['Size'].str.split('x|2$',expand=True)
pictures_df['width'] = np.where(pictures_df['width'] == '', pictures_df['length'], pictures_df['width'])
pictures_df['length'] = pictures_df['length'].str.strip()
pictures_df['width'] = pictures_df['width'].str.strip()

# convert length and widths to numeric (all cm so no conversion needed)
pictures_df['width'] = pd.to_numeric(pictures_df['width'].str.replace('"|cm','',regex = True), errors='coerce')
pictures_df['length'] = pd.to_numeric(pictures_df['length'].str.replace('"|cm','',regex = True), errors='coerce')

# Split frame length and width from size and remove whitespace
frames_df[['length', 'width']] = frames_df['Size'].str.split('x|2$',expand=True)
frames_df['width'] = np.where(frames_df['width'] == '', frames_df['length'], frames_df['width'])
frames_df['length'] = frames_df['length'].str.strip()
frames_df['width'] = frames_df['width'].str.strip()

# remove units and convert to numeric
frames_df['unit'] = np.where(frames_df['width'].str.contains('"', regex = False),'inch','cm')
frames_df['width'] = pd.to_numeric(frames_df['width'].str.replace('"|cm','',regex = True), errors='coerce')
frames_df['length'] = pd.to_numeric(frames_df['length'].str.replace('"|cm','',regex = True), errors='coerce')

# convert inch to cm for frames
frames_df['width'] = np.where(frames_df['unit'] == 'inch', frames_df['width']*2.54, frames_df['width'])
frames_df['length'] = np.where(frames_df['unit'] == 'inch', frames_df['length']*2.54, frames_df['length'])
frames_df['unit'] = 'cm'

# Frames can always be rotated, so make sure you know which is the min/max side
frames_df['max_side'] = np.where(frames_df['width'] > frames_df['length'],frames_df['width'],frames_df['length'])
frames_df['min_side'] = np.where(frames_df['width'] > frames_df['length'],frames_df['length'],frames_df['width'])

# See which pictures fit into which frames
# Work out the area of the frame vs the area of the picture and choose the frame with the smallest excess

# calculate areas
frames_df['frame_area'] = frames_df['max_side'] * frames_df['min_side']
pictures_df['picture_area'] = pictures_df['length'] * pictures_df['width']

# clean up frames_df before cross join
del frames_df['length']
del frames_df['width']
del frames_df['unit']

# Cross join data frames as any frame could fit a picture
pictures_and_frames = pictures_df.merge(frames_df, how='cross')

# Find frames bigger than or equal to the size of the pictures
pictures_and_frames['frame_fit'] = np.where(
    (
    (pictures_and_frames['length'] <= pictures_and_frames['max_side']) & 
    (pictures_and_frames['width'] <= pictures_and_frames['min_side'])
    ) | (
    (pictures_and_frames['width'] <= pictures_and_frames['max_side']) & 
    (pictures_and_frames['length'] <= pictures_and_frames['min_side'])
    )
    ,'fits','does not fit')

# filter for frames that fit
pictures_and_frames = pictures_and_frames.loc[pictures_and_frames['frame_fit'] == 'fits']

# calculate the excess space, ranking by the smallest excess area and filter
pictures_and_frames['excess_space'] = pictures_and_frames['frame_area'] - pictures_and_frames['picture_area']
pictures_and_frames['excess_space_rank'] = pictures_and_frames.groupby('Picture')['excess_space'].rank(ascending=True)
pictures_and_frames = pictures_and_frames.loc[pictures_and_frames['excess_space_rank'] == 1]

# Add picture max and min sides
pictures_and_frames['Max Side'] = np.where(pictures_and_frames['width'] > pictures_and_frames['length'],pictures_and_frames['width'],pictures_and_frames['length'])
pictures_and_frames['Min Side'] = np.where(pictures_and_frames['width'] > pictures_and_frames['length'],pictures_and_frames['length'],pictures_and_frames['width'])

# Output the data
# clean up and reach dataset  
pictures_and_frames = pictures_and_frames[['Picture','Size_y','Max Side','Min Side']]
pictures_and_frames = pictures_and_frames.rename(columns={'Size_y':'Frame'})

# Write to csv
pictures_and_frames.to_csv('prepped_data\\PD 2021 Wk 35 Output.csv', index=False)

print("data prepped!")
