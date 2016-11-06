## \file PythonHelper.py
#  \brief
#
#  \author Michael Ebner (michael.ebner.14@ucl.ac.uk)
#  \date Nov 2016


## Import libraries
# import os                       # used to execute terminal commands in python
# import sys
# import itk
# import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

## Import modules
# import utilities.SimpleITKHelper as sitkh

##-----------------------------------------------------------------------------
# \brief      Wait for <ENTER> to proceed the execution
# \date       2016-11-06 15:41:43+0000
#
def pause():
    programPause = raw_input("Press the <ENTER> key to continue ...")


##-----------------------------------------------------------------------------
# \brief      Plot 3D numpy array slice by slice next to each other
# \date       2016-11-06 01:39:28+0000
#
# All slices in the x-y-plane are plotted. The number of slices is given by the
# dimension in the z-axis.
#
# \param      nda3D_zyx  3D numpy data array in format (z,y,x) as it is given
#                        after sitk.GetArrayFromImage for instance
# \param      title      The title
# \param      cmap       Color map "Greys_r", "jet", etc.
#
def plot_3D_array_slice_by_slice(nda3D_zyx, title="image", cmap="Greys_r"):

    shape = nda3D_zyx.shape
    N_slices = shape[0]

    ## Define the grid to arrange the slices
    grid = _get_grid_size(N_slices)

    ## Plot figure
    fig = plt.figure(1)
    ctr = 1
    for i in range(0, N_slices):
        
        plt.subplot(grid[0], grid[1], ctr)
        plt.imshow(nda3D_zyx[i,:,:], cmap=cmap)
        plt.title(title+"_"+str(i))
        plt.axis('off')
        
        ctr += 1

    print("Slices of " + title + " are shown in separate window.")
    plt.show(block=False)


##-----------------------------------------------------------------------------
# \brief      Plot list of 2D numpy arrays next to each other
# \date       2016-11-06 02:02:36+0000
#
# \param      nda2D_list  List of 2D numpy data arrays
# \param      title       The title
# \param      cmap        The cmap
#
def plot_2D_array_list(nda2D_list, title="image", cmap="Greys_r"):

    shape = nda2D_list[0].shape
    N_slices = len(nda2D_list)

    if type(title) is not list:
        title = [title]

    ## Define the grid to arrange the slices
    grid = _get_grid_size(N_slices)

    ## Plot figure
    fig = plt.figure(1)
    ctr = 1
    for i in range(0, N_slices):
        
        plt.subplot(grid[0], grid[1], ctr)
        plt.imshow(nda2D_list[i], cmap=cmap)
        if len(title) is N_slices:
            plt.title(title[i])
        else:
            plt.title(title[0]+"_"+str(i))
        plt.axis('off')
        
        ctr += 1

    print("Slices of data arrays are shown in separate window.")
    plt.show(block=False)


##-----------------------------------------------------------------------------
# \brief      Gets the grid size given a number of 2D images
# \date       2016-11-06 02:02:20+0000
#
# \param      N_slices  The n slices
#
# \return     The grid size.
#
def _get_grid_size(N_slices):

    if N_slices > 40:
        raise ValueError("Too many slices to print")

    ## Define the view grid to arrange the slices
    if N_slices < 5:
        grid = (1, N_slices)
    elif N_slices > 4 and N_slices < 9:
        grid = (2, np.ceil(N_slices/2.).astype('int'))
    elif N_slices > 8 and N_slices < 13:
        grid = (3, np.ceil(N_slices/3.).astype('int'))
    elif N_slices > 12 and N_slices < 22:
        grid = (3, np.ceil(N_slices/3.).astype('int'))
    elif N_slices > 21 and N_slices < 29:
        grid = (4, np.ceil(N_slices/4.).astype('int'))
    else:
        grid = (5, np.ceil(N_slices/5.).astype('int'))

    return grid