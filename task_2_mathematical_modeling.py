import os
import numpy as np
from typing import Callable
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def plot_solution(Nx: int, Nt: int, dx: float, dt: float, D: float, grid_u: np.ndarray) -> None:
    """Drawing a heatmap and animation of the solution to the diffusion equation.

    Parameters
    ----------
    Nx : int
        Number of grid nodes by x.
    Nt : int
        Number of grid nodes by time.
    dx : float
        x-step.
    dt : float
        Time step.
    D : float
        Diffusion coefficient.
    grid_u : ndarray
        Solution of the diffusion equation.

    Returns
    -------
    None
    """
    parameters = "Nx_{}_Nt_{}_dt_{}_D_{}".format(Nx, Nt, dt, D)
    heatmap_filename = os.path.join('data', 'task_2', 'results', "heatmap_{}.png".format(parameters))
    animation_filename = os.path.join('data', 'task_2', 'results', "animation_{}.png".format(parameters))
    
    x = np.linspace(0, dx * Nx, Nx)
    t = np.linspace(0, dt * Nt, Nt)

    heatmap_fig, heatmap_ax = plt.subplots()
    heatmap_ax.pcolormesh(x, t, grid_u, shading="gouraud")
    heatmap_ax.set_title("Diffusion equation solution heatmap")
    heatmap_ax.set_xlabel("x")
    heatmap_ax.set_ylabel("t")
    heatmap_fig.savefig(heatmap_filename)

    animation_fig = plt.figure()
    animation_ax = plt.axes(xlim=(0, 2 * np.pi), ylim=(np.min(grid_u), np.max(grid_u)))
    line, = animation_ax.plot(x, grid_u[0])
    animation = FuncAnimation(animation_fig, lambda y: line.set_ydata(grid_u[y]), Nt, interval=100)
    plt.title("Diffusion equation solution animation")
    plt.xlabel("x")
    plt.ylabel("u(x, t)")
    animation.save(animation_filename)


def solve(Nx: int, Nt: int, dt: float, D: float, u_0: Callable, F: Callable, plot: bool = True) -> np.ndarray:
    """Solution of the diffusion equation on a ring.

    Parameters
    ----------
    Nx : int
        Number of grid nodes by x.
    Nt : int
        Number of grid nodes by time.
    dt : float
        Time step.
    D : float
        Diffusion coefficient.
    u_0 : Callable
        Given function.
    F : Callable
        Given function.
    plot : bool, default=True
        Plotting flag.

    Returns
    -------
    grid_u : ndarray
        Solution of the diffusion equation.
    """
    dx = 2 * np.pi / Nx
    x = np.linspace(0, dx * Nx, Nx)
    lambdas = np.array([4 * D / dx ** 2 * np.sin(k * dx / 4) ** 2 for k in range(Nx)])
    grid_u = np.empty((Nt, Nx))
    u = grid_u[0] = u_0(x)
    fourier_coefficients = np.fft.fft(u)
    for m in range(1, Nt):
        F_previous, F_current = F(u, (m - 1) * dt), F(u, m * dt)
        phi = np.fft.fft(F_previous + F_current)
        fourier_coefficients = ((2 - dt * lambdas) * fourier_coefficients + dt * phi) / (2 + dt * lambdas)
        u = np.fft.ifft(fourier_coefficients)
        grid_u[m] = u.real

    if plot:
        plot_solution(Nx, Nt, dx, dt, D, grid_u)

    return grid_u


solve(
    Nx=101,
    Nt=501,
    dt=0.1,
    D=0.001,
    u_0=lambda x: np.sin(5 * x),
    F=lambda u, t: np.sin(0.1 * u + t),
)
