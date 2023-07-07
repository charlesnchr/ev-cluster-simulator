""" ----------------------------------------
* Creation Time : Fri Jul  7 11:59:25 2023
* Author : Charles N. Christensen
* Github : github.com/charlesnchr
----------------------------------------"""

import skimage
import skimage.draw
import skimage.io
import skimage.transform
import numpy as np
import matplotlib.pyplot as plt
import os
import streamlit as st


def generate_ev_image(N, d_min, d_max, r_min, r_max, cluster_probability):
    plt.figure(figsize=(20, 20))

    skipped = 0

    for n in range(1):
        I = np.zeros((1024, 1024))

        for i in range(N):
            x = np.random.randint(0, 1024)
            y = np.random.randint(0, 1024)

            rows, cols = np.where(I == 0.8)

            d = np.random.randint(d_min, d_max)

            if np.random.rand() > 1 - cluster_probability and len(rows) > 0:
                ri = np.random.randint(0, len(rows))
                rr = rows[ri]
                rc = cols[ri]

                # which neighbour ?
                rn = np.random.randint(0, 8)
                if rn == 0:
                    x, y = rr + d, rc + d
                elif rn == 1:
                    x, y = rr + 0, rc + d
                elif rn == 2:
                    x, y = rr + d, rc + 0
                elif rn == 3:
                    x, y = rr - d, rc - d
                elif rn == 4:
                    x, y = rr + 0, rc - d
                elif rn == 5:
                    x, y = rr - d, rc + 0
                elif rn == 6:
                    x, y = rr + d, rc - d
                elif rn == 7:
                    x, y = rr - d, rc + d

            # close to any neighbours?
            useposition = True

            for c in range(y - int(d - 1), y + int(d + 1)):
                for r in range(x - int(d - 1), x + int(d - 1)):
                    if r >= 1024 or c >= 1024 or r < 0 or c < 0:
                        continue
                    if I[r, c] == 0.8:
                        useposition = False

            if not useposition:
                skipped += 1
                continue

            r = np.random.randint(r_min, r_max)

            if x + r >= 1024 or y + r >= 1024 or x - r < 0 or y - r < 0:
                skipped += 1
                continue

            cr, cc = skimage.draw.disk((x, y), r)

            I[cr, cc] = 0.8

    return I


if __name__ == "__main__":
    # streamlit input for plotting parameters
    N = st.sidebar.slider("Number of beads", 0, 1000, 100)
    d_min = st.sidebar.slider("Minimum distance between beads", 0, 100, 10)
    d_max = st.sidebar.slider("Maximum distance between beads", 0, 100, 11)
    r_min = st.sidebar.slider("Minimum radius of beads", 0, 100, 10)
    r_max = st.sidebar.slider("Maximum radius of beads", 0, 100, 11)
    cluster_probability = st.sidebar.slider("Cluster probability", 0.0, 1.0, 0.5)

    I = generate_ev_image(N, d_min, d_max, r_min, r_max, cluster_probability)

    fig = plt.figure(figsize=(20, 20))
    plt.imshow(I, cmap="gray")
    st.pyplot(fig)
