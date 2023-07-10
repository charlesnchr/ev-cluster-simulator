""" ----------------------------------------
* Creation Time : Fri Jul  7 11:59:25 2023
* Author : Charles N. Christensen
* Github : github.com/charlesnchr
----------------------------------------"""

from skimage import io, exposure
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.signal import convolve2d
import pandas as pd


def generate_uniform_coordinates(N, size=(1024, 1024)):
    """Generate uniformly distributed coordinates."""
    coordinates = []
    for i in range(N):
        x = np.random.randint(0, size)
        y = np.random.randint(0, size)
        coordinates.append((x, y))
    return coordinates


def generate_cluster_coordinates(
    coordinates, N_cluster_range, sigma, size=(1024, 1024)
):
    """Generate a new set of coordinates clustered around the original coordinates."""
    clustered_coordinates = []

    for coord in coordinates:
        # generate gaussian distributed points around each coordinate
        N_cluster_size = np.random.randint(N_cluster_range[0], N_cluster_range[1])
        cluster = np.random.normal(loc=coord, scale=sigma, size=(N_cluster_size, 2))

        # Clip the values so they fall within the image boundaries
        cluster[:, 0] = np.clip(cluster[:, 0], 0, size[0] - 1)
        cluster[:, 1] = np.clip(cluster[:, 1], 0, size[1] - 1)
        cluster = cluster.astype(int)

        clustered_coordinates.extend(cluster.tolist())

    return np.array(clustered_coordinates)


def generate_gaussian(size, psf_sigma=1, center=None):
    """Generate a 2D Gaussian kernel."""
    x = np.arange(0, size, 1, float)
    y = x[:, np.newaxis]
    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]
    G = np.exp(-((x - x0) ** 2 + (y - y0) ** 2) / (2 * psf_sigma**2))

    # normalize
    return G / G.sum()


def render_image(coordinates, r, psf_sigma, size, show_kernel=False):
    """Render coordinates onto an image canvas."""
    I = np.zeros(size)

    # to make the peak perfectly centered
    kernel_dim = 2 * r + 1

    for x, y in coordinates:
        gaussian = generate_gaussian(kernel_dim, psf_sigma=psf_sigma, center=None)

        if show_kernel:
            return gaussian

        if (
            x + r + 1 >= size[0]
            or y + r + 1 >= size[1]
            or x - r - 1 < 0
            or y - r - 1 < 0
        ):
            continue

        I[x - r : x + r + 1, y - r : y + r + 1] += gaussian

    return I


if __name__ == "__main__":
    N = st.sidebar.slider("Number of clusters", 0, 1000, 100)
    N_cluster = st.sidebar.slider("Localisations per cluster", 5, 50, (10, 20))
    cluster_sigma = st.sidebar.slider("Cluster spread (sigma)", 0.0, 20.0, 10.0)

    psf_sigma = st.sidebar.slider("Rendering sigma (PSF)", 0.0, 8.0, 3.0)
    kernel_radius = st.sidebar.slider(
        "Kernel radius (image dimension half-axis)", 0, 15, 8
    )
    show_kernel = st.sidebar.checkbox("Show kernel", value=False)
    img_dim_x = st.sidebar.slider("Image X Dimension", 256, 2048, 1024)
    img_dim_y = st.sidebar.slider("Image Y Dimension", 256, 2048, 1024)

    coordinates = generate_uniform_coordinates(N, size=max(img_dim_x, img_dim_y))
    coordinates = generate_cluster_coordinates(
        coordinates, N_cluster, cluster_sigma, (img_dim_x, img_dim_y)
    )

    I = render_image(
        coordinates,
        kernel_radius,
        psf_sigma=psf_sigma,
        size=(img_dim_x, img_dim_y),
        show_kernel=show_kernel,
    )

    st.title("EV cluster simulator")
    st.text(
        f"Image details:\n\tshape: {I.shape}, dtype: {I.dtype}, max: {I.max():.2f}, min: {I.min():.2f}"
    )

    # rescale
    p1, p2 = np.percentile(I, (0, 99.5))
    I_plot = exposure.rescale_intensity(I, in_range=(p1, p2))

    fig = plt.figure(figsize=(20, 20))
    plt.imshow(I_plot, cmap="gray")
    st.pyplot(fig)

    # Create dataframe
    coordinates_df = pd.DataFrame(coordinates, columns=["X", "Y"])

    # Convert DataFrame to CSV
    csv = coordinates_df.to_csv(index=False)

    # Download button
    st.download_button(
        label="Download coordinates as CSV",
        data=csv,
        file_name="coordinates.csv",
        mime="text/csv",
    )
