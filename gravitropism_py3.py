#!/usr/bin/env python3

import argparse
import math
import numpy as np
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description='This is a gravitropism plotting script.')
    parser.add_argument('-i','--input', help='Input file name', required=True)
    parser.add_argument('-T','--title', help='Output file prefix', required=True)
    parser.add_argument('-s','--plotline', help='Plot separator lines (T/F)', required=True)
    args = parser.parse_args()

    radie: float = 3
    scaleup: float = 10
    infile: str = args.input
    datalabel: str = args.title
    lineplot: bool = args.plotline == 'T'

    # Read and convert data
    with open(infile, 'r') as f:
        indata = f.readline().strip().split()
        degree_data = np.array([float(i) for i in indata], dtype=np.float32)

    xydeg2 = np.array([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360], dtype=np.float32)
    xydeg = -((xydeg2 / 360) * 2 * math.pi)[1:] + (math.pi / 12)

    histdata, _ = np.histogram(degree_data, xydeg2)
    mult = histdata / np.sum(histdata)
    ndir = len(mult)
    small_deg = (2 * math.pi / ndir) / 2

    # Plotting
    plt.axis(xmin=-10, xmax=10, ymin=-10, ymax=10)
    an = np.linspace(0, 2 * math.pi, 100)
    plt.plot(radie * np.cos(an), radie * np.sin(an), 'k')

    xylabel = xydeg2[1:].astype(int)
    xylabel[xylabel == 360] = 0

    for i in range(ndir):
        if lineplot:
            plt.plot(
                [(radie - 0.4) * np.cos(xydeg[i] - small_deg), (radie + 0.4) * np.cos(xydeg[i] - small_deg)],
                [(radie - 0.4) * np.sin(xydeg[i] - small_deg), (radie + 0.4) * np.sin(xydeg[i] - small_deg)],
                'k'
            )

        plt.text((radie * 0.7) * np.cos(xydeg[i] - (math.pi / 12)),
                 (radie * 0.7) * np.sin(xydeg[i] - (math.pi / 12)), str(xylabel[i]), ha='center', va='center', size='small')

        if mult[i] != 0:
            plt.plot(
                [(radie + 0.2) * np.cos(xydeg[i]), radie * np.cos(xydeg[i]) + np.cos(xydeg[i]) * scaleup * mult[i]],
                [(radie + 0.2) * np.sin(xydeg[i]), radie * np.sin(xydeg[i]) + np.sin(xydeg[i]) * scaleup * mult[i]],
                'k', linewidth=15
            )

            plt.text((1 + radie) * np.cos(xydeg[i]) + np.cos(xydeg[i]) * scaleup * mult[i],
                     (1 + radie) * np.sin(xydeg[i]) + np.sin(xydeg[i]) * scaleup * mult[i], f"{round(mult[i] * 100)}", color='r',
                     ha='center', va='center')

    plt.text(0, 0, datalabel, ha='center', size='large')
    plt.axis(xmin=-20, xmax=20, ymin=-20, ymax=20)
    plt.axis('scaled')
    plt.axis('off')
    plt.savefig(f"{datalabel}.pdf")

if __name__ == "__main__":
    main()


