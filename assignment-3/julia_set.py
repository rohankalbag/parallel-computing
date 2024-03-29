# Rohan Rajesh Kalbag
# Roll: 20D170033


from argparse import ArgumentParser
import matplotlib.pyplot as plt
import numpy as np


def command_line_fetcher():
    # function to fetch command line arguments
    parser = ArgumentParser(description="julia assignment ae6102")

    parser.add_argument('-x', '--x-pixels',
                        type=int, required=True, help="x axis pixels")

    parser.add_argument('-n', '--niter',
                        type=int, default=100, required=True,
                        help="number of iterations")

    parser.add_argument('-o', "--output", required=True,
                        help="file name for output to be printed")

    # extra argument to visualize plot using matplotlib
    parser.add_argument('--vis', action='store_true', help="visualize")
    return parser.parse_args()


def evaluate_julia(x_pixels, y_pixels, niter):
    # set result to be niter-1 for all entries
    result = np.ones((x_pixels, y_pixels))*(niter - 1)
    x, y = np.mgrid[-2:2:x_pixels*1j, -1.5:1.5:y_pixels*1j]
    Z = x + 1j*y
    # to keep track of entries that have diverged
    diverged = np.ones_like(result, dtype=bool)

    for i in range(niter):
        # find entries which are not diverged yet
        not_diverged = ~ diverged
        # perform the operation for this subset
        Z[not_diverged] = Z[not_diverged]**2 + (-0.8 + 0.156*1j)
        # find new diverged entries
        diverged = np.abs(Z) > 2
        # update the result array
        result[diverged & (result == niter - 1)] = i

    return result


if __name__ == "__main__":
    args = command_line_fetcher()
    x_pixels = args.x_pixels
    y_pixels = (x_pixels*3)//4
    niter = args.niter
    filename = args.output
    result = evaluate_julia(x_pixels, y_pixels, niter)
    np.savez(filename, result)

    # visualize the result
    if args.vis:
        plt.figure(figsize=(16, 12))
        plt.imshow(result.T, extent=[-2, 2, -1.5, 1.5])
        plt.show()
