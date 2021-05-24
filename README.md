# Gauss_fit_WITec
@author: dd

version: 1.1

Combines spectra from WITec X-Axis and Y-Axis txt files
and fits each spectra with two (or one) Gaussian functions.

Set initial values in gmodel.make_params(...).
Use gmodel.set_param_hint(...) for precise control of each Gaussian parameter.

Fitted parameters and statistics are saved to txt files.
