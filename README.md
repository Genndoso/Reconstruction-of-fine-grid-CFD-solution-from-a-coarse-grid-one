<p align="center">

![alt text](https://github.com/Genndoso/Reconstruction-of-fine-grid-CFD-solution-from-a-coarse-grid-one/blob/main/photo_2022-03-22_22-28-12.jpg)

</p>


# Reconstruction of fine grid CFD solution from a coarse grid one
____
Certain problems, for instance, timestepping of the Navier-Stokes equation, can be very computationally expensive to solve with desirable accuracy. Normally this is ameliorated by using e.g. multigrid methods, which are, however, unusable with commercial solvers. Another alternative is to employ the method of Galerkin and, upon isolating the modes of some snapshot matrix of fine-grid solutions, compute further on coarse grid with projection onto said modes, providing enhancement of approximation and not impairing usability with commercial solvers.  For this task two methods are salient: SINDy (sparse identification of nonlinear dynamics), which is in essence regression on functional basis, and employment of generative networks and autoencoders


# Data 

We have considered three problems which we will now state in the language of magnetohydrodynamics, as they are all of MHD or amagnetic hydrodynamic nature

__ 
[Cylindric dataset](https://cgl.ethz.ch/research/visualization/data.php). Simulation of a viscous 2D flow around a cylinder. The fluid was injected to the left of a channel bounded by solid walls with a slip boundary condition. The simulation was done with Gerris flow solver and was resampled onto a regular grid. In the original simulation, the unstructured grid was adaptively discretized based on the vorticity. Over the course of the simulation, the characteristic von-Karman vortex street is forming. The image on the side shows a later time step, in which the street is fully formed. The vortices move with almost constant speed, except directly in the wake of the obstacle, where they accelerate.


# Algorithm and models

## Autoencoder
Autoencoderis a special architecture of artificial neural networks that provides unsupervised learning using the backpropagation method
In our case we feed results obtained on the coarse mesh as an input to the autoencoder and results of on the fine mesh as the output. This way we try to build operator which maps results from the coarse mesh to the fine one.

Structure of our encoder is the following: as an input and output we provide RGB pictures, which are represented as width*height*3 neurons. The whole net is a simple MLP (width*height*3 -- 1536 -- 153 -- 70 -- 153 -- 1536 --width*height*3) structure with LeakyReLU activations and Dropouts on each layer. 100 epochs was used for training. Adam optimizer and learning rate scheduler was implemented. Training was based on MSE loss.


![alt text](https://github.com/Genndoso/Reconstruction-of-fine-grid-CFD-solution-from-a-coarse-grid-one/blob/main/1_44eDEuZBEsmG_TCAKRI3Kw%402x.png)

Performance of Autoencoder


## DCGAN
Generative adversarial networks is one of the most popular models of machine learning for the last several years.
Generative networks existed before GANs but the “adversarial” part actually adds a lot of value and new perspectives. The novelty comes from the fact that in this framework we train two models at the same time: the Generative and the discriminative ones. The Generative model tries to capture the data distribution, while the Discriminator model one estimates a probability that some content was generated by the Generative model, and did not come from the actual data. The Generative model then tries to fool the Discriminator model, by maximising the probability that it makes a mistake.
To construct GAN from to construct fine grid from low resolution coarse grid we tried to implement U-net architecture for generator part and feed-forward convolution network (CNN) for discriminator part.

![alt text](https://github.com/Genndoso/Reconstruction-of-fine-grid-CFD-solution-from-a-coarse-grid-one/blob/main/u-net_training_image_segmentation_models_in_pytorch_header.png)



# Results
To estimate results of our fine grid approximation we used the following metric:


Algorithm | Cylindric dataset | Orszag-Tang dataset 
:---| :-----------------------:|-------------:
SINDi | 11111 | 0000|
DCGAN | 11111 | 0000|
Autoencoder | 11111 | 0000|

