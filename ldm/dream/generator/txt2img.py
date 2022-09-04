'''
ldm.dream.generator.txt2img inherits from ldm.dream.generator
'''

import torch
import numpy as  np
from ldm.dream.generator.base import Generator

class Txt2Img(Generator):
    def __init__(self,model):
        super().__init__(model)
    
    @torch.no_grad()
    def image_iterator(self,prompt,sampler,steps,cfg_scale,ddim_eta,
                       conditioning,width,height,step_callback=None,**kwargs):
        """
        Returns a function returning an image derived from the prompt and the initial image
        Return value depends on the seed at the time you call it
        kwargs are 'width' and 'height'
        """
        uc, c   = conditioning

        def make_image(x_T):
            shape = [
                self.latent_channels,
                height // self.downsampling_factor,
                width  // self.downsampling_factor,
            ]
            samples, _ = sampler.sample(
                batch_size                   = 1,
                S                            = steps,
                x_T                          = x_T,
                conditioning                 = c,
                shape                        = shape,
                verbose                      = False,
                unconditional_guidance_scale = cfg_scale,
                unconditional_conditioning   = uc,
                eta                          = ddim_eta,
                img_callback                 = step_callback
            )
            return self.sample_to_image(samples)

        return make_image