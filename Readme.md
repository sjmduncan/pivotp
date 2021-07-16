# Pivotp

Pivot point calibration for a 3D stylus. The goal is to estimate the position, ${\bf t}_s$, of the pointy end of a stylus relative to the origin of the local coordinate system of a tracked device. The local coordinate space is defined by a ${\bf R}$ and translation ${\bf t}$.

A convenient way to do the calibration is to poke the pointy end of the stylus into a small divot so that the tip does not move, and rotate the whole thing around the pivot point, ${\bf t}_p$, making $N$ observations of ${\bf R}$ and ${\bf t}$ with different rotation angles. Then the results can be arranged into a system of linear equations:

$${\bf R}_i{\bf t}_s + {\bf t}_i = {\bf t}_p$$

$${\bf R}_i{\bf t}_s - {\bf t}_p = -{\bf t}_i$$

$$\left[\begin{matrix}
    {\bf R}_1 & -{\bf I} \\
    ... & ... \\
    {\bf R}_N & -{\bf I}
\end{matrix}\right]
\left[\begin{matrix}
    {\bf t}_s\\
    {\bf t}_p
\end{matrix}\right] =
\left[\begin{matrix}
    -{\bf t}_1\\
    ...\\
    -{\bf t}_N
\end{matrix}\right]$$

In the last form (${\bf I}$ is the 3x3 identity matrix) the least-squares optimisation of this linear system produces estimates of both ${\bf t}_s$ and ${\bf t}_p$.
