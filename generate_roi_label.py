#gui qt
from surfer import Brain, io, utils
import numpy as np
from scipy.stats import scoreatpercentile
import os
import math
import nipype.interfaces.fsl as fsl
import nipype.interfaces.freesurfer as fs
from mayavi import mlab
datadir="/gablab/p/bps/zqi_ytang/results/conn_sub80_0724/results/secondlevel"
os.environ["SUBJECTS_DIR"] = "/mindhive/xnat/surfaces/CASL"
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

roifile = "/gablab/p/bps/zqi_ytang/scripts/roi/IFG.nii"
def drawROI():
	for hemi in ["lh"]:
		# load data
		roivol = io.project_volume_data(roifile,
						             hemi,
						             subject_id=surfsubj,
						             smooth_fwhm=4.0,
						             projmeth="dist",
						             projsum="avg",
						             projarg=[0,6,0.1],
						             surf="white")
		# create label
		roivol = abs(roivol)
		roivol[roivol < 0.33] = 0
		#if max(roivol) < 1:
		#	brain.close()
		#	continue
		#else:
		write_label(np.asarray(np.nonzero(roivol)),"/gablab/p/bps/zqi_ytang/scripts/roi/surf-IFG.label")

		# load brain
		my_fig = mlab.figure(figure="new_fig1", size=(800,800))
		brain = Brain("fsaverage",hemi,"inflated",curv=True,size=[800,800],background="white",cortex=(("gist_yarg",-1.5,3.5,False)),figure=my_fig)
		set_mylights(my_fig,lights[hemi])

		#add label
		brain.add_label("/gablab/p/bps/zqi_ytang/scripts/roi/surf-IFG.label",borders=False,color="#ffff00",alpha=1)
		brain.add_label("/gablab/p/bps/zqi_ytang/scripts/roi/surf-IFG.label",borders=1,color="black",alpha=0.5)

		brain.show_view('lat')
		brain.save_image("/gablab/p/bps/zqi_ytang/scripts/roi/surf-IFG.tiff")
		brain.close()
drawROI()
