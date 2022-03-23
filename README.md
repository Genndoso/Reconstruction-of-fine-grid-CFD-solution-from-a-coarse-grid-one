

<p float="center">
  <img src="https://github.com/Genndoso/Reconstruction-of-fine-grid-CFD-solution-from-a-coarse-grid-one/blob/main/Images/photo_2022-03-22_22-28-12.jpg?raw=true" alt="Sublime's custom image" width=300/>
  <img src="https://github.com/Genndoso/Reconstruction-of-fine-grid-CFD-solution-from-a-coarse-grid-one/blob/main/Images/Screenshot_10.png" alt="Sublime's custom image" width=300 /> 
  <img src="https://github.com/Genndoso/Reconstruction-of-fine-grid-CFD-solution-from-a-coarse-grid-one/blob/main/Images/photo_2022-03-22_22-24-39.jpg" alt="Sublime's custom image" width=300 />
</p>

# Reconstruction of fine grid computational fluid dynamic (CFD) solution from a coarse grid one
____
Certain problems, for instance, timestepping of the Navier-Stokes equation, can be very computationally expensive to solve with desirable accuracy. Normally this is ameliorated by using e.g. multigrid methods, which are, however, unusable with commercial solvers. Another alternative is to employ the method of Galerkin and, upon isolating the modes of some snapshot matrix of fine-grid solutions, compute further on coarse grid with projection onto said modes, providing enhancement of approximation and not impairing usability with commercial solvers.  For this task two methods are salient: SINDy (sparse identification of nonlinear dynamics), which is in essence regression on functional basis, and employment of generative networks and autoencoders


# Data 

We have considered three problems which we will now state in the language of magnetohydrodynamics, as they are all of MHD or amagnetic hydrodynamic nature


[Cylindric dataset](https://cgl.ethz.ch/research/visualization/data.php). Simulation of a viscous 2D flow around a cylinder. The fluid was injected to the left of a channel bounded by solid walls with a slip boundary condition. The simulation was done with Gerris flow solver and was resampled onto a regular grid. In the original simulation, the unstructured grid was adaptively discretized based on the vorticity. Over the course of the simulation, the characteristic von-Karman vortex street is forming. The image on the side shows a later time step, in which the street is fully formed. The vortices move with almost constant speed, except directly in the wake of the obstacle, where they accelerate.

The problem of [Orszag and Tang](https://www.astro.princeton.edu/~jstone/Athena/tests/orszag-tang/pagesource.html) is one of the benchmarks in computational magnetohydrodynamics and corresponds to the onset of supersonic turbulence. Both lone shocks and shock-shock interactions are present in the system's evolution, thereby offering rather rich dynamics. The problem was solved on square domain and defined time interval [0; 0.8] with 400 elements in either direction for fine and 200 - for coarse mesh. The parameter was chosen to be the specific heat ratio, varied between known values. Boundary conditions were employed: periodic on both axes, initial conditions specified below.


[Kelvin–Helmholtz instability in the presence of magnetic field](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/kelvin-helmholtz-instability) is also one of the known benchmarks in CMHD for reasons of the magnetic field’s smoothing effect on instabilities (Frank et al., 1996). As observed by Chandrasekhar, any magnetic field not perfectly normal to the direction of streaming has the effect equivalent to surface tension, which is known to inhibit instability development [chandrainstability]. Of especial interest is also the qualitative property of the problem that allows to judge the numerical diffusion effect of the scheme and discretisation, for it contributes significantly to suppression of instability. This therefore poses an additional problem of reconstructing possibly suppressed instability from smoothed coarse grid.


# Algorithm and models
## NIRB
The baseline algorithm hinges on the ideas of multigrid solution and Galerkin projection. It seeks the best linear approximation to the interpolation operator which sends the coarse-grid solution to the fine-grid one by means of making the residual orthogonal to all present fine-grid solutions. Naturally, this entails orthogonal projection. Further amelioration of condition number is performed by means of regularised least square problem from coarse-grid to fine-grid coefficients. More information about NIRB algorithm can be found [here](https://egrosjean.pages.math.cnrs.fr/media/PRESENTATION_GTT.pdf)

## SINDy
SINDy can be understood as abusing the Galerkin projection by piling on an indeterminate number of very distinct functions and projecting onto them, with the difference that SINDy necessarily demands parsimony of representation. We approximate the dynamic system under study (which we here understand as evolution in the space of discretisation steps) as a superposition of some candidate functions from a given library. Determination of the coefficients is achieved by solving LSQP from candidate functions defined on the coarse-grid approximation to fine-grid solution with sequential thresholding. More information about SINDy algorihm can be found [here](https://royalsocietypublishing.org/doi/10.1098/rspa.2020.0279)


## Autoencoder
Autoencoderis a special architecture of artificial neural networks that provides unsupervised learning using the backpropagation method
In our case we feed results obtained on the coarse mesh as an input to the autoencoder and results of on the fine mesh as the output. This way we try to build operator which maps results from the coarse mesh to the fine one.

Structure of our encoder is the following: as an input and output we provide RGB pictures, which are represented as width*height*3 neurons. The whole net is a simple MLP (width*height*3 -- 1536 -- 153 -- 70 -- 153 -- 1536 --width*height*3) structure with LeakyReLU activations and Dropouts on each layer. 100 epochs was used for training. Adam optimizer and learning rate scheduler was implemented. Training was based on MSE loss.


![alt text](https://github.com/Genndoso/Reconstruction-of-fine-grid-CFD-solution-from-a-coarse-grid-one/blob/main/Images/1_44eDEuZBEsmG_TCAKRI3Kw%402x.png)




## DCGAN
Generative adversarial networks is one of the most popular models of machine learning for the last several years.
Generative networks existed before GANs but the “adversarial” part actually adds a lot of value and new perspectives. The novelty comes from the fact that in this framework we train two models at the same time: the Generative and the discriminative ones. The Generative model tries to capture the data distribution, while the Discriminator model one estimates a probability that some content was generated by the Generative model, and did not come from the actual data. The Generative model then tries to fool the Discriminator model, by maximising the probability that it makes a mistake.
To construct GAN from to construct fine grid from low resolution coarse grid we tried to implement U-net architecture for generator part and feed-forward convolution network (CNN) for discriminator part.

<p align="center">
  <img src="https://github.com/Genndoso/Reconstruction-of-fine-grid-CFD-solution-from-a-coarse-grid-one/blob/main/Images/u-net_training_image_segmentation_models_in_pytorch_header.png?raw=true" alt="Sublime's custom image"/>
</p>







# Results

Graphical representation of working machine learning algorithms
Cylindrical dataset

Test | Prediction |  
:---| :--------------:|
![alt text](https://github.com/Genndoso/Reconstruction-of-fine-grid-CFD-solution-from-a-coarse-grid-one/blob/main/Images/Cylinder%20test%20.png)| ![alt text](https://github.com/Genndoso/Reconstruction-of-fine-grid-CFD-solution-from-a-coarse-grid-one/blob/main/Images/cylinder%20predicted.png)|

Orszag-Tang task
Test | Prediction |  
:---| :--------------:|
![alt text](https://github.com/Genndoso/Reconstruction-of-fine-grid-CFD-solution-from-a-coarse-grid-one/blob/main/Images/Encoder%20test.png)| ![alt text](https://github.com/Genndoso/Reconstruction-of-fine-grid-CFD-solution-from-a-coarse-grid-one/blob/main/Images/Encoder%20pred.png)|



To estimate results of our fine grid approximation we used the following metric:
1-norm of the residual, scaled by the 1-norm of the vectorised fine-grid solution
![image](https://user-images.githubusercontent.com/53058704/159635314-af8b7f61-36ed-40bc-a776-b8d570c39e9f.png)

Algorithm | Cylindric dataset | Orszag-Tang dataset  | Kelvin–Helmholtz instability
:---| :-----------------------:|-------------:|-------------:
SINDy | 0.0001 | 0.001|7E-5 |
NIRB | 0.178 | 0.262| 0.0005        |
NIRB-R | 0.0005 | 0.007|0.0001|
DCGAN | 0.0442 | 0.0734| 0.1154
Autoencoder | 0.047 | 0.073|  - |

# Reproducibility
PYNBs are run straightforwardly, once data is supplied. We do not link said data because it is excessively large and therefore has problems being transmitted. We do, however, supply the weights (prikrepi vesa). gen-4-anal.py is the file needed to perform NIRB and SINDy computations. It is uploaded in its NIRB configuration and needs to only be run (provided a great amount of RAM is present; the demands can exceed 30-40 GB). To change it into SINDy configuration, one needs to specify a function library, import STSL_SINDy from SINDy_func.py and run with desired parameters. Even greater demands of RAM are exercised; be warned that the solution is not computed quickly.


