## Reconstruction of fine grid CFD solution from a coarse grid one

Certain problems, for instance, timestepping of the Navier-Stokes equation, can be very computationally expensive to solve with desirable accuracy. Normally this is ameliorated by using e.g. multigrid methods, which are, however, unusable with commercial solvers. Another alternative is to employ the method of Galerkin and, upon isolating the modes of some snapshot matrix of fine-grid solutions, compute further on coarse grid with projection onto said modes, providing enhancement of approximation and not impairing usability with commercial solvers. Therefore, we see that a linear operator (projection) can well-approximate an operator which maps a coarse-grid solution to a fine-grid solution exactly. It is natural to ask whether this could be improved by using nonlinear operators. For this task two methods are salient: SINDy (sparse identification of nonlinear dynamics), which is in essence regression on functional basis, and employment of generative networks. Study of these is the goal.  Explanation in more detail: The first method under consideration (aside from the Galerkin approximation that is used purely as a proven benchmark to test against) entails constructing a library of candidate functions of the input data (solution on a coarse grid with interpolation on intermediate fine-grid points) and doing regularised (to promote sparsity) regression on those with the goal of reconstructing a fine-grid solution. An alike method was successfully used to capture nonlinear dynamics in data and even reconstruct parameterised PDEs, so the method appears feasible.  The second method under consideration entails collecting solutions on coarse and fine grids (this time without the strict need to interpolate the coarse-grid one) and training a GAN to reconstruct the latter from the former. Of particular interest is examining if it would be enough to supply individual time snapshots instead of snapshot matrices.  These two are planned to be tested on a number of problems concerned with nonlinear dynamics against each other and a benchmark Galerkin approximation (third paper in references)




https://img.shields.io/static/v1?label=<LABEL>&message=<MESSAGE>&color=<COLOR>
