#!/bin/bash

# how to call this script:
# bash recon.sh SLI3000 10
#				^subj	^MPRAGE series number
# tkp@mit.edu

source /software/common/bin/fss 5.3.0
export SUBJECTS_DIR="/mindhive/xnat/surfaces/CASL"

mkdir -p /mindhive/xnat/surfaces/CASL/${1}/mri/orig/
mri_convert \
	/mindhive/xnat/data/CASL/${1}/`printf %03d ${2}`*MPRAGE*.nii* \
	/mindhive/xnat/surfaces/CASL/${1}/mri/orig/001.mgz
echo "recon-all -autorecon-all -subjid ${1}" | qsub -V -N ${1} \
		-e /gablab/p/CASL/Analysis/convert_recon/recon-logs/ \
		-o /gablab/p/CASL/Analysis/convert_recon/recon-logs/ \
		-q recon
