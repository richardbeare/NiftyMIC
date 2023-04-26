##
# \file setup.py
#
# Instructions:
# 1) Set environment variables with prefix NIFTYMIC_, e.g.
#   `export NIFTYMIC_ITK_DIR=path-to-ITK_NIFTYMIC-build`
#   to incorporate `-D ITK_DIR=path-to-ITK_NIFTYMIC-build` in `cmake` build.
# 2) `pip install -e .`
#   All python packages and command line tools are then installed during
#
# \author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
# \date       July 2017
#


import re
import os
import sys
from setuptools import setup, find_packages


about = {}
with open(os.path.join("niftymic", "__about__.py")) as fp:
    exec(fp.read(), about)


#with open("README.md", "r") as fh:
#    long_description = fh.read()

long_description="Removed - meant to be README.md"

def install_requires(fname="requirements.txt"):
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


setup(name='NiftyMIC',
      version=about["__version__"],
      description=about["__summary__"],
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/gift-surg/NiftyMIC',
      author=about["__author__"],
      author_email=about["__email__"],
      license=about["__license__"],
      packages=find_packages(),
      install_requires=install_requires(),
      # data_files=[(d, [os.path.join(d, f) for f in files])
      #             for d, folders, files
      #             in os.walk(os.path.join("data", "demo"))],
      zip_safe=False,
      keywords='development numericalsolver convexoptimisation',
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: Healthcare Industry',
          'Intended Audience :: Science/Research',

          'License :: OSI Approved :: BSD License',

          'Topic :: Software Development :: Build Tools',
          'Topic :: Scientific/Engineering :: Medical Science Apps.',

          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      entry_points={
          'console_scripts': [
              'niftymic_correct_bias_field = niftymic.application.correct_bias_field:main',
              'niftymic_reconstruct_volume = niftymic.application.reconstruct_volume:main',
              'niftymic_reconstruct_volume_RB = niftymic.application.reconstruct_volume_RB:main',
              'niftymic_reconstruct_volume_from_slices = niftymic.application.reconstruct_volume_from_slices:main',
              'niftymic_register_image = niftymic.application.register_image:main',
              'niftymic_multiply = niftymic.application.multiply:main',
              'niftymic_run_reconstruction_parameter_study = niftymic.application.run_reconstruction_parameter_study:main',
              'niftymic_run_reconstruction_pipeline = niftymic.application.run_reconstruction_pipeline:main',
              'niftymic_nifti2dicom = niftymic.application.nifti2dicom:main',
              'niftymic_show_reconstruction_parameter_study = nsol.application.show_parameter_study:main',
              'niftymic_segment_fetal_brains = niftymic.application.segment_fetal_brains:main',

              # rs-fMRI 
              'niftymic_rsfmri_estimate_motion = niftymic.application.rsfmri_estimate_motion:main',
              'niftymic_rsfmri_reconstruct_volume_from_slices = niftymic.application.rsfmri_reconstruct_volume_from_slices:main',
          ],
      },
      )
