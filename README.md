# NEXRAD_ecl3
# -------------------------------------------------------------------------------------------------
# PYTHON 3 VERSION
# ====== = =======
# This program is a shortcut script to establish a communications (comms) link in an ORPG# account using the nbtcp command to generate Level-III products, after the MRPG has been successfully configured and started. Note that the user MUST of course already be logged in to a valid ORPG# account, and the files $HOME/cfg/comms_link.conf and $HOME/cfg/tcp.conf MUST be already configured for the appropriate port number prior to starting the MRPG and running this script. Also ensure that a valid RPS listing (.dat file) of Level-III radar products to be created is available in the $HOME/cfg directory. DO NOT run this program in a given ORPG# account if a playback is already in progress, only run this script BEFORE starting a playback.
#
# Note that it is HIGHLY recommended that this script be run using the "wrapper" ecl (BASH) script (located in the 'CSH' Scripts directory) from the $HOME ORPG# directory using a DIFFERENT terminal window than that running the RPG software / playback.
#
# Created by: Stephen Castleberry (stephen.castleberry@noaa.gov) - ROC/CIMMS - 02/2016
# 
# Converted to Python 3 by Paul McCrone paul.mccrone@noaa.gov - ROC/FRB - 09/2023 
#                          Only those changes needed for python 3 were made. No changes to the logic.
#                          The logic for determining the user name now uses os, not subprocess.
#                          THIS IS THE ORIGNAL ECL WITH ALL THE ORIGINAL FUNCTIONS, except in Python 3.
# -------------------------------------------------------------------------------------------------
