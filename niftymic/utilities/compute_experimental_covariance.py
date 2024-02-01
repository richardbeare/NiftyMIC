import numpy as np
import SimpleITK as sitk

def computeExpCov(fname):
    im = sitk.ReadImage(fname)
    sp = np.array(im.GetSpacing())
    
    var = ((np.sqrt(2)*sp)**2)/(8*np.log(2))
    print("Using covariance: ", var)
    return var
