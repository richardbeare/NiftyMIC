## \file Wwo2DImage.py
#  \brief Class generated to handle a single 2D image.
# 
#  \author Michael Ebner
#  \date June 2015

import nibabel as nib           # nifti files
import numpy as np
import copy


class TwoDImage:

    def __init__(self, dir_nifti, nifti_filename):
        self._dir_nifti = dir_nifti
        self._nifti_filename = nifti_filename
        self._img_nifti = nib.load(dir_nifti + nifti_filename + ".nii.gz")

        self._affine = self._img_nifti.affine
        self._data = self._img_nifti.get_data()
        self._header = self._img_nifti.header


    def get_shape(self):
        return self._img_nifti.get_data().shape


    def get_dir(self):
        return self._dir_nifti


    def get_filename(self):
        return self._nifti_filename


    def get_header(self):
        return self._header


    def get_data(self):
        return self._data


    def get_affine(self):
        return self._affine



    def set_affine(self, affine):
        try:
            if (affine.shape != (4, 4)):
                raise ValueError("Affine transformation non-compliant")

            self._affine = affine

            nifti = nib.Nifti1Image(self._data, affine=self._affine, header=self._header)
            nib.save(nifti, self._dir_nifti + self._nifti_filename + ".nii.gz") 
            print("Affine transformation of image " + self._nifti_filename + " successfully updated")

        except ValueError as err:
            print(err.args)

    def set_data(self, array):
        try:
            if (array.size != self._data.size):
                raise ValueError("Dimension mismatch of data array")

            self._data = array

            nifti = nib.Nifti1Image(self._data, affine=None, header=self._header)
            nib.save(nifti, self._dir_nifti + self._nifti_filename + ".nii.gz") 
            print("Data array of image " + self._nifti_filename + " successfully updated")          

        except ValueError as err:
            print(err.args)