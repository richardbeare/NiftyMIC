##-----------------------------------------------------------------------------
## \file TestParameterNormalization.py
#  \brief  Class containing unit tests for module ParameterNormalization
# 
#  \author Michael Ebner (michael.ebner.14@ucl.ac.uk)
#  \date Nov 2016


## Import libraries 
import SimpleITK as sitk
import itk
import numpy as np
import unittest
import sys
from scipy.ndimage import imread

## Import modules
import base.Stack as st
import utilities.ParameterNormalization as pn
import utilities.SimpleITKHelper as sitkh
import registration.IntraStackRegistration as inplanereg


## Concept of unit testing for python used in here is based on
#  http://pythontesting.net/framework/unittest/unittest-introduction/
#  Retrieved: Aug 6, 2015
class TestParameterNormalization(unittest.TestCase):

    ## Specify input data
    dir_test_data = "../../../test-data/"

    accuracy = 6

    def setUp(self):        
        pass

    
    def test_parameter_normalization(self):

        use_verbose = 0

        filename_stack = "FetalBrain_reconstruction_3stacks_myAlg"
        filename_stack_corrupted = "FetalBrain_reconstruction_3stacks_myAlg_corrupted_inplane"

        stack_sitk = sitk.ReadImage(self.dir_test_data + filename_stack + ".nii.gz")
        stack_corrupted_sitk = sitk.ReadImage(self.dir_test_data + filename_stack_corrupted + ".nii.gz")

        stack_corrupted = st.Stack.from_sitk_image(stack_corrupted_sitk, "stack_corrupted")
        stack = st.Stack.from_sitk_image(sitk.Resample(stack_sitk, stack_corrupted.sitk),"stack")

        # sitkh.show_stacks([stack, stack_corrupted])

        inplane_registration = inplanereg.IntraStackRegistration(stack_corrupted, stack)
        inplane_registration.set_initializer_type("moments")
        inplane_registration.set_intensity_correction_type("affine")
        inplane_registration.set_transform_type("rigid")
        inplane_registration._run_registration_pipeline_initialization()
        parameters = inplane_registration.get_parameters()

        ## Normalization routine
        parameters_tmp = np.array(parameters)
        parameter_normalization = pn.ParameterNormalization(parameters_tmp)
        parameter_normalization.compute_normalization_coefficients()

        coefficients = parameter_normalization.get_normalization_coefficients()


        ## Check correct normalization
        parameters_tmp = parameter_normalization.normalize_parameters(parameters_tmp)
        
        if use_verbose:
            print("Normalization:")
        for i in range(0, parameters_tmp.shape[1]):
            mean = np.mean(parameters_tmp[:,i])
            std = np.std(parameters_tmp[:,i])

            if use_verbose:
                print("\tmean = %.4f" %(mean))
                print("\tstd = %.4f" %(std))

            ## Check mean
            self.assertEqual(np.round(
                abs(mean)
            , decimals = self.accuracy), 0)

            ## Check standard deviation
            if abs(std) > 1e-8:
                self.assertEqual(np.round(
                    abs(std - 1)
                , decimals = self.accuracy), 0)


        ## Check correct normalization
        parameters_tmp = parameter_normalization.denormalize_parameters(parameters_tmp)
        if use_verbose:
            print("\nDenormalization:")
        for i in range(0, parameters_tmp.shape[1]):
            mean = np.mean(parameters_tmp[:,i])
            std = np.std(parameters_tmp[:,i])

            if use_verbose:
                print("\tmean = %.4f" %(mean))
                print("\tstd = %.4f" %(std))

            ## Check mean
            self.assertEqual(np.round(
                abs(mean-coefficients[0,i])
            , decimals = self.accuracy), 0)

            ## Check standard deviation
            if abs(std) > 1e-8:
                self.assertEqual(np.round(
                    abs(std - coefficients[1,i])
                , decimals = self.accuracy), 0)

            ## Check parameter values
            self.assertEqual(np.round(
                np.linalg.norm(parameters_tmp-parameters)
            , decimals = self.accuracy), 0)

