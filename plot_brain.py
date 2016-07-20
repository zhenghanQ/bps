#gui qt
from surfer import Brain, io, utils
import numpy as np
from scipy.stats import scoreatpercentile
import os
import math
import nipype.interfaces.fsl as fsl
import nipype.interfaces.freesurfer as fs
from mayavi import mlab
datadir="/gablab/p/CASL/Results/Imaging/tone/groups"
os.environ["SUBJECTS_DIR"] = "/home/tkp/projects/inflated-brains"
surfsubj="fsaverage"

def write_label(vertices,filename):
	if os.path.isfile(filename):
		os.remove(filename)
	outfile = open(filename,'wt')
	print>>outfile, '#!ascii label  , from subject MNI_152_T1_1mm vox2ras=TkReg '
	print>>outfile, len(vertices[0])
	for i in vertices[0]:
		print>>outfile, i
	outfile.close()

def set_mylights(fig_object,mylights):
	for i in range(0,len(mylights)):
		fig_object.scene.light_manager.lights[i].azimuth = mylights[i][0]
		fig_object.scene.light_manager.lights[i].elevation = mylights[i][1]
		fig_object.scene.light_manager.lights[i].intensity = mylights[i][2]

lights = {}
lights['lh'] =   [[-45.0, 45.0, 1.0], [-60.0, -30.0, 0.6], [60.0, 0.0, 0.75], [0.0, 0.0, 1.0]]
lights['rh'] =   [[45.0, 45.0, 1.0], [60.0, -30.0, 0.6], [-60.0, 0.0, 0.75], [0.0, 0.0, 1.0]]

fig6a = "/gablab/p/CASL/Results/Imaging/resting/zqi/conn_CASL_pre_post_training13o/results/secondlevel/ANALYSIS_01/All(0).postspe(1)/pre-training(-1).post-training(1)/anat_func_lifg/results.img"
fig6b = "/gablab/p/CASL/Results/Imaging/resting/zqi/conn_CASL_pre_post_training13o/results/secondlevel/ANALYSIS_01.SUBJECT_EFFECTS_All(0.0).finalall(1.0).CONDITIONS_pre-training(-1.0).post-training(1.0)./anat_func_lifg_1_1./results.img"
fig6balt = "/gablab/p/CASL/Results/Imaging/resting/zqi/conn_CASL_pre_post_training13o/results/secondlevel/ANALYSIS_01.SUBJECT_EFFECTS_All(0.0).finalall(1.0).CONDITIONS_pre-training(-1.0).post-training(1.0)./anat_func_lifg/results.img"
fig6d = "/gablab/p/CASL/Results/Imaging/resting/zqi/conn_CASL_pre_post_training13o/results/secondlevel/ANALYSIS_01/3mohsk_all(0).3mohsk(1)/pre-training(-1).post-training(1)/anat_func_lifg_1_1/results.img"

def drawContrast(infile,outname):
	for hemi in ["rh"]:
		# load data
		volpos = io.project_volume_data(infile,
						             hemi,
						             subject_id=surfsubj,
						             smooth_fwhm=4.0,
						             projmeth="dist",
						             projsum="max",
						             projarg=[-6,6,0.1],
						             surf="pial")
		"""
		volneg = io.project_volume_data(rsfcfile_neg,
						             hemi,
						             subject_id=surfsubj,
						             smooth_fwhm=4.0,
						             projmeth="dist",
						             projsum="max",
						             projarg=[-6,6,0.1],
						             surf="white")
		volneg=volneg*-1
		ccvol=volpos+volneg
		"""

		# load brain
		my_fig = mlab.figure(figure="new_fig1", size=(800,800))
		brain = Brain("fsaverage",hemi,"inflated",curv=True,size=[800,800],background="white",cortex=(("gist_yarg",-1.5,3.5,False)),figure=my_fig)
		set_mylights(my_fig,lights[hemi])

		if outname == "fig6b":
			# create label
			labIFG = volpos
			labIFG[labIFG < 2.0739] = 0
			write_label(np.asarray(np.nonzero(labIFG)),"fig6prep/roi_IFG.label")
			#brain.add_label("fig6prep/roi_IFG.label",borders=False,color="red",alpha=0.125)			
			brain.add_label("fig6prep/roi_IFG.label",borders=2,color="#e7298a",alpha=1)		

		if outname == "fig6d":
			# create label
			labAG = io.project_volume_data("/gablab/p/CASL/Results/Imaging/resting/zqi/conn_CASL_pre_post_training13o/results/secondlevel/ANALYSIS_01/3mohsk_all(0).3mohsk(1)/pre-training(-1).post-training(1)/anat_func_lifg_1_1/roi_AG.nii.gz",
								         hemi,
								         subject_id=surfsubj,
								         smooth_fwhm=4.0,
								         projmeth="dist",
								         projsum="max",
								         projarg=[-6,6,0.1],
								         surf="pial")
			labAG[labAG < 0.33] = 0
			write_label(np.asarray(np.nonzero(labAG)),"fig6prep/roi_AG.label")
			labSTGMTG = io.project_volume_data("/gablab/p/CASL/Results/Imaging/resting/zqi/conn_CASL_pre_post_training13o/results/secondlevel/ANALYSIS_01/3mohsk_all(0).3mohsk(1)/pre-training(-1).post-training(1)/anat_func_lifg_1_1/roi_STGMTG.nii.gz",
								         hemi,
								         subject_id=surfsubj,
								         smooth_fwhm=4.0,
								         projmeth="dist",
								         projsum="max",
								         projarg=[-6,6,0.1],
								         surf="pial")
			labSTGMTG[labSTGMTG < 0.66] = 0
			write_label(np.asarray(np.nonzero(labSTGMTG)),"fig6prep/roi_STGMTG.label")
			#brain.add_label("fig6prep/roi_AG.label",borders=False,color="black",alpha=0.125)
			brain.add_label("fig6prep/roi_AG.label",borders=2,color="#1b9e77",alpha=1)
			#brain.add_label("fig6prep/roi_STGMTG.label",borders=False,color="blue",alpha=0.125)
			brain.add_label("fig6prep/roi_STGMTG.label",borders=2,color="#7570b3",alpha=1)


		brain.add_overlay(volpos,
							min=2.0739, #p = 0.025 2-tailed
							max=5.0216, #p = 0.000025, 2-tailed
							sign="abs",
							name=outname,
							hemi=hemi)

		brain.show_view('lat')
		brain.save_image("fig6prep/%s.tiff"%(outname))
		brain.close()

#drawContrast(fig6a,"fig6a")
drawContrast(fig6b,"fig6b")
#drawContrast(fig6d,"fig6d")

#drawContrast(fig6balt,"fig6balt")
