# DEA-CalVal-Phase2

This repo contains workflows that are relevant to the DEA Calibration/Validation
project, utilising new UAS (Unmanned Aerial System, aka drone) technology to
conduct field campaigns, starting in March 2020.

The drone-mounted hardware includes the
<A HREF="https://www.oceaninsight.com/products/spectrometers/general-purpose-spectrometer/flame-series/flame-uv-vis/">
Flame UV-VIS spectrometer
</A>
and the
<A HREF="https://spectralevolution.com/products/hardware/field-portable-spectroradiometers-for-remote-sensing/rs-3500/">
Spectral Evolution SR-3500
</A>
.<P>

The FLAME directory includes calibration data that were independently measured by
<A HREF="http://www.terraluma.net">
Terraluma
</A>
in the CALIBRATION directory. Output csv files are stored in the CSV directory.
The MISC directory contains miscellaneous information, including image
registration python scripts based on
<A HREF="https://github.com/keflavich/image_registration">
this repo
</A>
, which can be used to check the relative positioning (ie. registration) of
drone- and satellite-based imagery. Output png files can be found in the PNG
directory. Source code for the workflows is found in the SRC directory.
Flame workflows are found in the WORKFLOWS directory. <P>
