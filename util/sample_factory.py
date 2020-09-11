import os
from collections import OrderedDict
import pathlib
import pofah.path_constants.sample_dict as sd
import pofah.jet_sample as js
import pofah.util.utility_fun as utfu


class SamplePathFactory():

    path_dict = {
        'default': sd.path_dict['base_dir_events'],
        'img': sd.path_dict['base_dir_images'],
        'img-54': os.path.join(sd.path_dict['base_dir_images'],'54px'),
        'particle': sd.path_dict['base_dir_events'],
        'img-local': sd.path_dict['base_dir_images_local'],
        'img-local-54': sd.path_dict['base_dir_images_local'],
        'particle-local': sd.path_dict['base_dir_events_local'],
    }

    def __init__(self, experiment, mode='default'):
        self.mode = mode
        self.input_dir = self.path_dict[self.mode]
        self.result_dir = experiment.result_dir
        if self.mode == 'img-local':
            self.init_img_local(experiment)
        if self.mode == 'img-local-54':
            self.init_img_local_54()
        if self.mode == 'img':
            self.init_img()
        if self.mode == 'img-54':
            self.init_img_54()
        if self.mode == 'particle-local':
            self.init_particle_local()
        if self.mode == 'particle':
            self.init_particle()


    def init_img(self, pix_suffix=None):
        self.qcd_file_path = os.path.join(self.input_dir,'qcd_sqrtshatTeV_13TeV_PU40_SIDEBAND_mjj_cut_concat_1.2M_pt_img.h5')
        self.sample_suffix = '_mjj_cut_concat_200K_pt_img.h5'

    def init_img_54(self):
        self.qcd_file_path = os.path.join(self.input_dir,'qcd_sqrtshatTeV_13TeV_PU40_SIDEBAND_mjj_cut_1.2M_pt_img_54px.h5')
        self.sample_suffix = '_mjj_cut_concat_200K_pt_img_54px.h5'

    def init_default(self):
        pass

    def init_img_local(self, experiment):
        self.qcd_file_path = os.path.join(self.input_dir,'qcd_sqrtshatTeV_13TeV_PU40_SIDEBAND_img_20K.h5')
        self.sample_suffix = '_mjj_cut_concat_10K_pt_img.h5'
        self.result_dir = os.path.join(sd.path_dict['base_dir_results_local'], experiment.run_dir)

    def init_img_local_54(self):
        self.qcd_file_path = os.path.join(self.input_dir, sd.path_dict['file_names']['qcdSide']+'_mjj_cut_20K_pt_img_54px.h5')
        self.sample_suffix = '_mjj_cut_10K_pt_img_54px.h5'

    def init_particle(self):
        self.qcd_file_path = os.path.join(self.input_dir, sd.path_dict['file_names']['qcdSide']+'_concat_1.5M.h5')
        self.sample_suffix = '_mjj_cut_concat_200K.h5'

    def init_particle_local(self):
        self.qcd_file_path = os.path.join(self.input_dir, 'background_small_concat_10K.h5')
        self.sample_suffix = '_concat_10K.h5'

    @property
    def qcd_path(self):
        return self.qcd_file_path

    @property
    def qcd_sig_path(self):
        if self.mode == 'particle':
            return os.path.join(self.input_dir, sd.path_dict['file_names']['qcdSig']+'_mjj_cut_concat_2M.h5')
        return os.path.join(self.input_dir,sd.path_dict['file_names']['qcdSig']+self.sample_suffix)
    

    def sample_path(self, id):
        if id == 'qcdSide':
            return self.qcd_path
        if id == 'qcdSig':
            return self.qcd_sig_path
        return os.path.join(self.input_dir,sd.path_dict['file_names'][id]+self.sample_suffix)

    def result_path(self,id):
        return os.path.join(self.result_dir,sd.path_dict['file_names'][id]+'.h5')


class SamplePathDirFactory():

    def __init__(self, path_dict):
        self.base_dir = path_dict['base_dir']
        self.sample_dir = path_dict['sample_dir']
        self.sample_file = path_dict['file_names']

    def update_base_path(self, repl_dict):
        self.base_dir = utfu.multi_replace(self.base_dir, repl_dict)
        return self

    def sample_dir_path(self, id):
        s_path = os.path.join(self.base_dir, self.sample_dir[id])
        pathlib.Path(s_path).mkdir(parents=True, exist_ok=True) # have to create result directory for each sample here, not optimal, TODO: fix
        return s_path

    def sample_file_path(self, id):
        return os.path.join(self.base_dir, self.sample_dir[id], self.sample_file[id]+'.h5')


##### utility functions

def read_data_to_jet_sample_dict(sample_ids, read_fun):
    data = OrderedDict()
    for sample_id in sample_ids:
        data[sample_id] = js.JetSample.from_input_file(sample_id, read_fun(sample_id))
    return data

def read_results_to_jet_sample_dict(sample_ids, experiment, mode='default'):
    paths = SamplePathFactory(experiment, mode=mode)
    return read_data_to_jet_sample_dict(sample_ids, paths.result_path)

def read_inputs_to_jet_sample_dict(sample_ids, experiment, mode='default'):
    paths = SamplePathFactory(experiment, mode=mode)  # 'default' datasample
    return read_data_to_jet_sample_dict(sample_ids, paths.sample_path)

def read_inputs_to_jet_sample_dict_from_dir(sample_ids, paths):
    data = OrderedDict()
    for sample_id in sample_ids:
        data[sample_id] = js.JetSample.from_input_dir(sample_id, paths.sample_dir_path(sample_id))
    return data
