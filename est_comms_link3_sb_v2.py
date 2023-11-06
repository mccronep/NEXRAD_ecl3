#!/usr/bin/python3

### ------------------------------------------------------------------------------------------------------
### PYTHON 3 VERSION
### ====== = =======
### This program is a shortcut script to establish a communications (comms) link in an ORPG# account using 
### the nbtcp command to generate Level-III products, after the MRPG has been successfully configured and 
### started. Note that the user MUST of course already be logged in to a valid ORPG# account, and the files 
### $HOME/cfg/comms_link.conf and $HOME/cfg/tcp.conf MUST be already configured for the appropriate port number 
### prior to starting the MRPG and running this script. Also ensure that a valid RPS listing (.dat file) of 
### Level-III radar products to be created is available in the $HOME/cfg directory. DO NOT run this program in a 
### given ORPG# account if a playback is already in progress, only run this script BEFORE starting a playback.
###
### Note that it is HIGHLY recommended that this script be run using the "wrapper" ecl (BASH) script (located in 
### the 'CSH' Scripts directory) from the $HOME ORPG# directory using a DIFFERENT terminal window than that 
### running the RPG software / playback.
###
### Created by: Stephen Castleberry (stephen.castleberry@noaa.gov) - ROC/CIMMS - 02/2016
### 
### Converted to Python 3 by Paul McCrone paul.mccrone@noaa.gov - ROC/FRB - 09/2023 
###                          This adds subprocess to run nbtcp. Changes how we run nbtcp.
###                          THIS IS NOT THE ORIGINAL ECL.
### ------------------------------------------------------------------------------------------------------


# Import the needed libraries.
#from Tkinter import Tk
try:
    # Python version 3.X:
    from tkinter import Tk
except: 
    print("Error with import 1")

try:
    import sys
    import os
    import subprocess as sp
    #import tkFileDialog as tkf    #####----- tkFileDialog was only in python 2 . Python 3 uses filedialog
    from tkinter import filedialog as tkf
except: 
    print("Error with import 2")

# Set constants / adaptable parameters.
n_args = 1
user_spec = 'orpg'
cfg_dirSpec = 'cfg'
commsl_fileSpec = 'comms_link.conf'
tcp_fileSpec = 'tcp.conf'
rad_site_fileSpec = 'site_info.dea'
commsl_lineSpec = 'cm_tcp'
tcp_port_lineSpec = 'rpga1'
site_id_lineSpec = 'rpg_name'
core_nbtcp_dirSpec = '/src/cpc102/tsk060'
override_cmd_dir = '/import/apps/scastleberry/Scripts/RPG/cpc102.tsk060'
override_cmd_msg_fnames = ['awips_rps.msg','rpccds_rps.msg']
override_cmd_spec = override_cmd_dir + '/nbtcp'
default_cmd_spec = 'nbtcp'

# Show explanatory usage text.
if len(sys.argv) == 1:
        print("\n")
        print("""This Python 3 program is a shortcut script to establish a communications (comms) link in an ORPG# account using
the nbtcp command to generate Level-III products, after the MRPG has been successfully configured and
started. Note that the user MUST of course already be logged in to a valid ORPG# account, and the files
$HOME/cfg/comms_link.conf and $HOME/cfg/tcp.conf MUST be already configured for the appropriate port number
prior to starting the MRPG and running this script. Also ensure that a valid RPS listing (.dat file) of
Level-III radar products to be created is available in the $HOME/cfg directory. DO NOT run this program in a
given ORPG# account if a playback is already in progress, only run this script BEFORE starting a playback.\n""")
        print("""Note that it is HIGHLY recommended that this script be run using the "wrapper" ecl (BASH) script (located
in the 'CSH' Scripts directory, one directory hierarchy level up from this script's directory) from the $HOME ORPG# directory
using a DIFFERENT terminal window than that running the RPG software / playback.\n""")
        print("EXECUTION METHOD:\n\n")
        print("For the Python script alone (From this script's directory):\n")
        print("./est_comms_link.py Override_CMD_Flag-[OPTIONAL] Output_Dir\n")
        print("When using the external BASH wrapper program (PREFERRED METHOD, from any directory):\n")
        print("ecl Override_CMD_Flag-[OPTIONAL] Output_Dir\n")
        print("""To use the ecl shortcut script from any directory, ensure it is soft-linked in your personal bin directory by first entering:
ln -s /import/apps/scastleberry/Scripts/CSH/ecl ~/bin/. from the command line and ensure your ~/bin directory is appended to the current ORPG# account's PATH variable.\n\n""")
        print("""Override_CMD_Flag is an OPTIONAL switch that can be set to have the RPG use an alternative nbtcp executable in establishing the comms link.
If set, this program will use an nbtcp execubable file located at: """+ override_cmd_dir+ """ which is a modified version of the baseline nbtcp
software from RPG Build 18 (v1.259) that contains support for SPD (Supplemental Precipitation Data, Prod.82) and MET (Meteorological Signal, Prod.346) Level-III products.
If the alternate command is used, the .msg files: """+ ', '.join(override_cmd_msg_fnames)+ """ from the same directory will also be copied to the ORPG# account's
~"""+ core_nbtcp_dirSpec+ """ directory and will replace the existing .msg files with the same names there to enable support for the MET product.
Valid Options: 1 (for YES), 0 (for NO, Use Default), or OMIT this parameter to also use the default command\n""")
        print("""Output_Dir is the full path to the output directory where the Level-III data files will be stored.
Valid Options: /full_path_to_output_directory_location (if the path is known or does not yet exist), 0 (to browse for and select the output directory)\n""")
        print("\n")

        sys.exit()

elif len(sys.argv) != n_args + 1 and len(sys.argv) != n_args + 2:
        print("\n")
        print("ERROR: Incorrect number of input arguments. Program requires either "+ str(n_args)+ " or "+ str(n_args+1)+ ", but recieved "+ str(len(sys.argv)-1)+ ".\n")
        sys.exit()

# Load input parameters.
if len(sys.argv) == n_args + 1:
        override_cmd_flag = '0'
        output_dir = sys.argv[1]
else:
        override_cmd_flag = sys.argv[1]
        output_dir = sys.argv[2]

# Ensure the user is actually logged into an ORPG account.
user_obj = sp.Popen('whoami',stdout=sp.PIPE)
user = user_obj.stdout.read()
#user = user.strip(b'\n')    ### P.McCrone commneted this out. 9/13/2023

user = 'orpg2'
user = os.environ.get("USER")


if user_spec not in user:
        print("\n")
        print("ERROR: Not logged in to a valid ORPG account.\n")
        print("Current user is: "+ user+ "\n")
        print("Program execution terminated!\n")
        sys.exit()
# Get the home ORPG# directory.
home_dir = os.environ['HOME']

# Get the ORPG number.
user_arr = user.split(user_spec)
orpg_num = user_arr[1]

# Validate the input.
if output_dir != '0':
        if not os.path.isdir(output_dir):
                try:
                        os.makedirs(output_dir)
                except OSError:
                        print("\n")
                        print("ERROR: Unable to create directory: "+ output_dir+ " - Incorrect Permissions.\n")
                        print("Program execution terminated!\n")
                        sys.exit()
        elif not os.access(output_dir,os.W_OK):
                print("\n")
                print("ERROR: The current user: "+ user+ " is unable to write to directory: "+ output_dir+ " - Incorrect Permissions.\n")
                print("Program execution terminated!\n")
                sys.exit()
else:
        Tk().withdraw()
        output_dir = tkf.askdirectory(title='Select Level-III Products Output Directory',initialdir=home_dir)

        if output_dir == ():
                print("\n")
                print("Program execution cancelled.\n")
                sys.exit()

if output_dir[-1] != '/':
        output_dir = output_dir + '/'

while override_cmd_flag != '0' and override_cmd_flag != '1':
        print("\n")
        print("ERROR: "+ str(override_cmd_flag)+ " is not a valid value for the default nbtcp command override option.\n")
        print("The valid options are: 1 (for YES, Override) or 0 (for NO, Use Default)\n")
        override_cmd_flag = raw_input("Enter a valid option for the default nbtcp command override option:\n")

override_cmd_flag = int(override_cmd_flag)

# Set the TCP configuration file and site info file paths, and ensure the files actually exist.
cfg_dir = home_dir+ '/'+ cfg_dirSpec
commsl_fp = cfg_dir+ '/'+ commsl_fileSpec
tcp_fp = cfg_dir+ '/'+ tcp_fileSpec
rad_site_fp = cfg_dir+ '/'+ rad_site_fileSpec

if not os.path.isfile(commsl_fp):
        print("\n")
        print("ERROR: File: "+ commsl_fp+ " not present in directory: "+ cfg_dir+ "\n")
        print("Program execution terminated!\n")
        sys.exit()

if not os.path.isfile(tcp_fp):
        print("\n")
        print("ERROR: File: "+ tcp_fileSpec+ " not present in directory: "+ cfg_dir+ "\n")
        print("Program execution terminated!\n")
        sys.exit()

if not os.path.isfile(rad_site_fp):
        print("\n")
        print("ERROR: File: "+ rad_site_fileSpec+ " not present in directory: "+ cfg_dir+ "\n")
        print("Program execution terminated!\n")
        sys.exit()

# Acquire the active comms link number.
commsl_f = open(commsl_fp,'r')
commsl_d = commsl_f.readlines()
commsl_f.close()

commsl_d_f = []
for i in commsl_d:
        if commsl_lineSpec in i and '#' not in i:
                commsl_d_f.append(i)

if not commsl_d_f:
        print("\n")
        print("ERROR: Comms link line specification "+ commsl_lineSpec+ " not present in file: "+ commsl_fp+ "\n")
        print("Program execution terminated!\n")
        sys.exit()

active_flag = 0
for i in commsl_d_f:
        if commsl_lineSpec in i and commsl_lineSpec+'_' not in i:
                commsl_l = i
                active_flag = 1
                break

if active_flag == 0:
        print("\n")
        print("ERROR: No active comms link number in file: "+ commsl_fp+ "\n")
        print("Program execution terminated!\n")
        sys.exit()

commsl_a = commsl_l.split(' ')
commsl_a = [i for i in commsl_a if i != '' and i != '\n']
commsl_num = commsl_a[0]


# Acquire the active TCP port number.
tcp_f = open(tcp_fp,'r')
tcp_d = tcp_f.readlines()
tcp_f.close()

active_flag = 0
for i in tcp_d:
        if tcp_port_lineSpec in i:
                tcp_a = i.split(' ')
                tcp_a = [i for i in tcp_a if i != '' and i != '\n']
                if tcp_a[0] == commsl_num:
                        port_lnum = tcp_a[0]
                        port_num = tcp_a[2]
                        active_flag = 1
                        break

if active_flag == 1:
        print("\n")
        print("Port Number: "+port_num+" TCP Link Number: "+commsl_num+"\n")
if active_flag == 0:
        print("\n")
        print("ERROR: No active TCP port number in file: "+ tcp_fp+ "\n")
        print("Program execution terminated!\n")
        sys.exit()

#tcp_a = tcp_l.split(' ')
#tcp_a = [i for i in tcp_a if i != '' and i != '\n']
#port_lnum = tcp_a[0]
#port_num = tcp_a[2]

# Verify that the comms link number and TCP port link number are compatible.
if commsl_num != port_lnum:
        print("\n")
        print("ERROR: The active comms link number: "+ commsl_num+ " does not match the active TCP port link number: "+ port_lnum+ "\n")
        print("Program execution terminated!\n")
        sys.exit()

# Make backup copies of the comms link and TCP port files.
os.system('cp '+ commsl_fp+ ' '+ commsl_fp+ '.orpg'+ orpg_num+ '.restore')
os.system('cp '+ tcp_fp+ ' '+ tcp_fp+ '.orpg'+ orpg_num+ '.restore')

# Acquire the current radar site.
rad_site_f = open(rad_site_fp,'r')
rad_site_d = rad_site_f.readlines()
rad_site_f.close()

site_flag = 0
for i in rad_site_d:
        if site_id_lineSpec in i:
                rad_site_l = i
                site_flag = 1
                break

if site_flag == 0:
        print("\n")
        print("ERROR: No site ID information in file: "+ rad_site_fp+ "\n")
        print("Program execution terminated!\n")
        sys.exit()

rad_site_l = rad_site_l.strip('\n')
rad_site_a = rad_site_l.split('\t')
rad_site = rad_site_a[-1]


# Verification print statements.
print("\n")
print("The current ORPG account is: ORPG"+ orpg_num+ "\n")
print("The active comms link number is: "+ commsl_num+ "\n")
print("The active TCP port number is: "+ port_num+ "\n")
print("The current radar site is: "+ rad_site+ "\n")
print("The selected Level-III products output directory is: "+ output_dir+ "\n")

# If needed, verify that the required files are available to use the override command, use the default command if not.
if override_cmd_flag == 0:
        cmd_spec = default_cmd_spec
else:
        override_success_flag = 1
        if not os.path.isfile(override_cmd_spec):
                print("Override executable command not found at location: "+ override_cmd_spec+ "\n")
                print("Using default executable command instead.\n")
                override_success_flag = 0
        else:
                orig_msg_files = []
                for i in override_cmd_msg_fnames:
                        orig_msg_file = home_dir+ core_nbtcp_dirSpec+ '/'+ i
                        override_msg_file = override_cmd_dir+ '/'+ i

                        if os.path.isfile(orig_msg_file) and os.path.isfile(override_msg_file):
                                orig_msg_files.append(orig_msg_file)
                                if not os.path.isfile(orig_msg_file+ '.orig'):
                                        os.system('mv '+ orig_msg_file+ ' '+ orig_msg_file+ '.orig')
                                os.system('cp -f '+ override_msg_file+ ' '+ orig_msg_file)
                        elif not os.path.isfile(orig_msg_file):
                                override_success_flag = 0
                                print("Original .msg file: "+ orig_msg_file+ " not available.\n")
                                print("Using default executable command instead.\n")
                                break
                        elif not os.path.isfile(override_msg_file):
                                override_success_flag = 0
                                print("Override .msg file: "+ override_msg_file+ " not available.\n")
                                print("Using default executable command instead.\n")
                                break

                if override_success_flag == 0:
                        # Restore the original .msg files if needed.
                        for i in orig_msg_files:
                                os.system('rm -f '+ i)
                                os.system('mv '+ i+ '.orig '+ i)

        if override_success_flag == 1:
                cmd_spec = override_cmd_spec
        else:
                cmd_spec = default_cmd_spec

# Attempt to establish the comms link on the active TCP port using the nbtcp command.
print("Establishing nbtcp comms link ...\n")

ecl_command = cmd_spec+ ' -p '+ port_num+ ' -A -s '+ rad_site+ ' -d '+ output_dir+ ' rpga1'
#os.system(ecl_command)

### Changes here for nbtcp.
dashp='-p'
dasha='-A'
dashs='-s'
dashd='-d'
rpgaa='rpga1'


popen_list=[cmd_spec, dashp, port_num, dasha, dashs,rad_site, dashd, output_dir, rpgaa]

rpsfile='qpetest_rps_list.ISDP_B22.dat'
creturn='\n'


#myinput='qpetest_rps_list.ISDP_B22.dat\n3\n1\n'
myinput=rpsfile+creturn+'3'+creturn+'1'+creturn

print("My input is:"+str(myinput))

mbytesvalue=myinput.encode('utf-8')

print("The bytes value of myinput is:")
print(mbytesvalue)

#p=sp.Popen([cmd_spec, '-p', port_num, '-A', '-s',rad_site, '-d', output_dir, 'rpga1'],stdout=sp.PIPE, stdin=sp.PIPE,stderr=sp.STDOUT)
#p.stdin.write(b'qpetest_rps_list.ISDP_B22.dat\n3\n1\n')

p=sp.Popen(popen_list,stdout=sp.PIPE, stdin=sp.PIPE,stderr=sp.STDOUT)
p.stdin.write(mbytesvalue)

psstdout = p.communicate()[0].decode('utf-8')
#psstdout = p.communicate(input=b'qpetest_rps_list.ISDP_B22.dat\n3\n1\n')[0]
print('')

#:

# didn't work
#p = sp.run([cmd_spec, ' -p ', port_num, ' -A ', ' -s ',rad_site, ' -d ', output_dir, ' rpga1'],stdout=sp.PIPE, input=myinput.encode('ascii'))
#print('Returncode is '+str(psstdout.decode()))
#print("The Returncode is: "+str(p.returncode))


print("\n")
print("nbtcp comms link (Port #: "+ port_num+ ") disconnected.\n")

print("Program Execution Complete.\n")
sys.exit()

