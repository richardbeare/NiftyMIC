##
# \file InputArparser.py
# \brief      Class holding a collection of possible arguments to parse for
#             scripts
#
# \author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
# \date       August 2017
#

import argparse

import pythonhelper.PythonHelper as ph
import inspect


##
# Class holding a collection of possible arguments to parse for scripts
# \date       2017-08-07 01:26:11+0100
#
class InputArgparser(object):

    def __init__(self,
                 description=None,
                 prog=None,
                 epilog="Author: Michael Ebner (michael.ebner.14@ucl.ac.uk)",
                 ):

        kwargs = {}
        if description is not None:
            kwargs['description'] = description
        if prog is not None:
            kwargs['prog'] = prog
        if epilog is not None:
            kwargs['epilog'] = epilog

        self._parser = argparse.ArgumentParser(**kwargs)

    def get_parser(self):
        return self._parser

    def parse_args(self):
        return self._parser.parse_args()

    def print_arguments(self, args, title="Input Parameters:"):
        ph.print_title(title)
        for arg in sorted(vars(args)):
            ph.print_info("%s: " % (arg), newline=False)
            print(getattr(args, arg))

    def add_filename(
        self,
        option_string="--filename",
        type=str,
        help="Path to NIfTI file (.nii or .nii.gz).",
        required=True,
    ):
        self._add_argument(dict(locals()))

    def add_filename_mask(
        self,
        option_string="--filename-mask",
        type=str,
        help="Path to NIfTI file mask (.nii or .nii.gz).",
        required=False,
    ):
        self._add_argument(dict(locals()))

    def add_dir_input(
        self,
        option_string="--dir-input",
        type=str,
        help="Input directory with NIfTI files (.nii or .nii.gz).",
        required=False,
        default=None,
    ):
        self._add_argument(dict(locals()))

    def add_filenames(
        self,
        option_string="--filenames",
        nargs="+",
        help="Filenames.",
        default="",
    ):
        self._add_argument(dict(locals()))

    def add_dir_output(
        self,
        option_string="--dir-output",
        type=str,
        help="Output directory.",
        default=None,
    ):
        self._add_argument(dict(locals()))

    def add_suffix_mask(
        self,
        option_string="--suffix-mask",
        type=str,
        help="Suffix used to associate a mask with an image. "
        "E.g. suffix_mask='_mask' means an existing "
        "image_i_mask.nii.gz represents the mask to "
        "image_i.nii.gz for all images image_i in the input "
        "directory.",
        default="_mask",
    ):
        self._add_argument(dict(locals()))

    def add_prefix_output(
        self,
        option_string="--prefix-output",
        type=str,
        help="Prefix for SRR output file name.",
        default="SRR_",
    ):
        self._add_argument(dict(locals()))

    def add_target_stack_index(
        self,
        option_string="--target-stack-index",
        type=int,
        help="Index according to alphabetical order of stacks (images) "
        "which defines physical space for SRR. First index is 0.",
        default=0,
    ):
        self._add_argument(dict(locals()))

    def add_sigma(
        self,
        option_string="--sigma",
        type=float,
        help="Standard deviation for Scattered Data Approximation approach "
        "to reconstruct first estimate of HR volume from all 3D input stacks.",
        default=0.9,
    ):
        self._add_argument(dict(locals()))

    def add_alpha(
        self,
        option_string="--alpha",
        type=float,
        help="Regularization parameter alpha to solve the Super-Resolution "
        "Reconstruction problem: SRR = argmin_x "
        "[0.5 * sum_k ||y_k - A_k x||^2 + alpha * R(x)].",
        default=0.03,
    ):
        self._add_argument(dict(locals()))

    def add_alpha_first(
        self,
        option_string="--alpha-first",
        type=float,
        help="Regularization parameter like 'alpha' but used for the first"
        "SRR step.",
        default=0.1,
    ):
        self._add_argument(dict(locals()))

    def add_reg_type(
        self,
        option_string="--reg-type",
        type=str,
        help="Type of regularization for SR algorithm. Either "
        "'TK0', 'TK1' or 'TV' for zeroth/first order Tikhonov "
        " or total variation regularization, respectively."
        "I.e. "
        "R(x) = ||x||_2^2 for 'TK0', "
        "R(x) = ||Dx||_2^2 for 'TK1', "
        "or "
        "R(x) = ||Dx||_1 for 'TV'. ",
        default="TK1",
    ):
        self._add_argument(dict(locals()))

    def add_iter_max(
        self,
        option_string="--iter-max",
        type=int,
        help="Number of maximum iterations for the numerical solver.",
        default=10,
    ):
        self._add_argument(dict(locals()))

    def add_iter_max_first(
        self,
        option_string="--iter-max-first",
        type=int,
        help="Number of maximum iterations for the numerical solver like "
        "'iter-max' but used for the first SRR step",
        default=5,
    ):
        self._add_argument(dict(locals()))

    def add_rho(
        self,
        option_string="--rho",
        type=float,
        help="Regularization parameter for augmented Lagrangian term for ADMM "
        "to solve the SR reconstruction problem in case TV regularization is "
        "chosen.",
        default=0.5,
    ):
        self._add_argument(dict(locals()))

    def add_admm_iterations(
        self,
        option_string="--admm-iterations",
        type=int,
        help="Number of ADMM iterations.",
        default=10,
    ):
        self._add_argument(dict(locals()))

    def add_minimizer(
        self,
        option_string="--minimizer",
        type=str,
        help="Coice of minimizer used for the inverse problem associated to "
        "the SRR. Possible choices are 'lsmr' or any solver in "
        "scipy.optimize.minimize like 'L-BFGS-B'. Note, in case of a chosen "
        "non-linear data loss only non-linear solvers like 'L-BFGS-B' are "
        "viable.",
        default="lsmr",
    ):
        self._add_argument(dict(locals()))

    def add_two_step_cycles(
        self,
        option_string="--two-step-cycles",
        type=int,
        help="Number of two-step-cycles, i.e. number of "
        "Slice-to-Volume Registration and Super-Resolution Reconstruction "
        "cycles",
        default=3,
    ):
        self._add_argument(dict(locals()))

    def add_data_loss(
        self,
        option_string="--data-loss",
        type=str,
        help="Loss function rho used for data term, i.e. rho((y_k - A_k x)^2) "
        "Possible choices are 'linear', 'soft_l1, 'huber', 'arctan' and "
        "'cauchy'.",
        default="linear",
    ):
        self._add_argument(dict(locals()))

    def add_dilation_radius(
        self,
        option_string="--dilation-radius",
        type=int,
        help="Dilation radius in number of voxels used for segmentation "
        "propagation from target stack in case masks are not provided for all "
        "images.",
        default=3,
    ):
        self._add_argument(dict(locals()))

    def add_extra_frame_target(
        self,
        option_string="--extra-frame-target",
        type=float,
        help="Increase chosen target space uniformly in each direction by "
        "extra frame given in mm.",
        default=0,
    ):
        self._add_argument(dict(locals()))

    def add_bias_field_correction(
        self,
        option_string="--bias-field-correction",
        type=int,
        help="Turn on/off bias field correction step during data "
        "preprocessing.",
        default=0,
    ):
        self._add_argument(dict(locals()))

    def add_intensity_correction(
        self,
        option_string="--intensity-correction",
        type=int,
        help="Turn on/off linear intensity correction step during data "
        "preprocessing.",
        default=0,
    ):
        self._add_argument(dict(locals()))

    def add_isotropic_resolution(
        self,
        option_string="--isotropic_resolution",
        type=int,
        help="Specify isotropic resolution for obtained SRR volume. Default "
        "resolution is specified by in-plane resolution of chosen target "
        "stack.",
        default=None,
    ):
        self._add_argument(dict(locals()))

    def add_log_script_execution(
        self,
        option_string="--log-script-execution",
        type=int,
        help="Turn on/off log for script execution.",
        default=0,
    ):
        self._add_argument(dict(locals()))

    def add_write_motion_correction(
        self,
        option_string="--write-motion-correction",
        type=int,
        help="Turn on/off functionality to write final result of motion "
        "correction. This includes the rigidly aligned stacks with their "
        "respective motion corrected individual slices and the overall "
        "transform applied to each individual slice.",
        default=0,
    ):
        self._add_argument(dict(locals()))

    def add_provide_comparison(
        self,
        option_string="--provide-comparison",
        type=int,
        help="Turn on/off functionality to create files "
        "allowing for a visual comparison between original "
        "data and the obtained SRR. A folder 'comparison' "
        "will be created in the output directory containing "
        "the obtained SRR along with the linearly resampled "
        "original data. An additional script "
        "'show_comparison.py' will be provided whose "
        "execution will open all images in ITK-Snap "
        "(http://www.itksnap.org/).",
        default=0,
    ):
        self._add_argument(dict(locals()))

    def add_verbose(
        self,
        option_string="--verbose",
        type=int,
        help="Turn on/off verbose output.",
        default=1,
    ):
        self._add_argument(dict(locals()))

    def add_stack_recon_range(
        self,
        option_string="--stack-recon-range",
        type=int,
        help="Number of components used for SRR.",
        default=15,
    ):
        self._add_argument(dict(locals()))

    ##
    # Adds an argument to argument parser.
    #
    # Rationale: Make interface as generic as possible so that function call
    # works regardless the name of the desired option
    # \date       2017-08-06 21:54:51+0100
    #
    # \param      self     The object
    # \param      allvars  all variables set at respective function call as
    #                      dictionary
    #
    def _add_argument(self, allvars):

        # Skip variable 'self'
        allvars.pop('self')

        # Get name of argument to add
        option_string = allvars.pop('option_string')

        # Build dictionary for additional, optional parameters
        kwargs = {}
        for key, value in allvars.iteritems():
            kwargs[key] = value

        # Add information on default value in case provided
        if 'default' in kwargs.keys():

            txt_default = " [default: %s]" % (str(kwargs['default']))

            # Case where 'required' key is given:
            if 'required' in kwargs.keys():

                # Only add information in case argument is not mandatory to
                # parse
                if kwargs['default'] is not None and not kwargs['required']:
                    kwargs['help'] += txt_default

            # Case where no such field was provided
            else:
                if kwargs['default'] is not None:
                    kwargs['help'] += txt_default

        # Add argument with its options
        self._parser.add_argument(option_string, **kwargs)
