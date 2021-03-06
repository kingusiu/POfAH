config = {

    'image_size' : 54,
    'beta' : 0.1,
    'min_pixel' : 0.0,
    'max_pixel' : 1866.1377,
    'mass_cut' : 1100.0,
    'result_key' : 'results',

    # input and output directories

    #'input_dir' : '/eos/user/k/kiwoznia/data/VAE_data/VAE_check/images',
    'input_dir' : 'data/events',
    #'input_dir' : 'data/images',
    'fig_dir' : 'fig',
    #'result_dir' : '/eos/user/k/kiwoznia/data/VAE_data/outputs/results',
    'result_dir' : '/eos/home-k/kiwoznia/dev/autoencoder_for_anomaly/convolutional_VAE/results',
    'tensorboard_dir' : 'tensorboard',
    'model_dir' : 'models',
    'analysis_base_dir': '/eos/home-k/kiwoznia/data/VAE_results/bump_hunt_results',
    'model_analysis_base_dir': '/eos/home-k/kiwoznia/data/VAE_results/model_analysis'
}