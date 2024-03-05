import pygame as pg
import numpy as np

W, H = 900, 900

pg.init()

screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()

max_iters = 150


def julia(c):
    # Create arrays of x and y coordinates
    x_coords = np.linspace(-1.5, 1.5, W)
    y_coords = np.linspace(-1.5, 1.5, H)

    # Create meshgrid of x and y coordinates
    X, Y = np.meshgrid(x_coords, y_coords)

    # Initialize Z array
    Z = X + 1j * Y

    # Initialize iterations array
    iters = np.zeros_like(Z, dtype=int)

    for i in range(max_iters):
        Z = Z**2 + c
        mask = np.abs(Z) > 2
        iters[mask & (iters == 0)] = (
            i  # Update iterations for points that have not yet diverged
        )
        Z[mask] = np.nan  # Set diverged points to NaN to avoid further iterations

    iters[iters == 0] = (
        max_iters  # Set iterations for points that have not diverged to max_iters
    )

    # Normalize 'iters' to the range [0, 255]
    iters_normalized = (iters / max_iters) * 255

    # Invert the normalized values
    iters_inverted = 255 - iters_normalized

    # Convert to integers
    iters_inverted = iters_inverted.astype(int)

    count = 0

    X = np.interp(X, [-1.5, 1.5], [0, W])
    Y = np.interp(Y, [-1.5, 1.5], [0, H])

    # Update pixel values
    for x, y, it in zip(X.flatten(), Y.flatten(), iters_inverted.flatten()):
        # if count % 100 ==0 :
        #     print(int(x),int(y), (it,it,it))
        screen.set_at((int(x), int(y)), (it, it, it))
        count += 1


running = True

ans = ""

while ans not in ("manual", "cursor"):
    ans = input("Manual input or cursor updating (*slow*)? ").lower()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if ans == "cursor":
        mp = pg.mouse.get_pos()

        c = complex(
            np.interp(mp[0], [0, W], [-1.5, 1.5]), np.interp(mp[1], [0, H], [-1.5, 1.5])
        )

        julia(c)
        pg.display.flip()

    else:
        # Handle user input for a new set
        new_set = input("New set ? (y/n): ").lower()
        if new_set == "y":
            x = float(input(r"cₓ : "))
            y = float(input(r"cᵧ : "))
            c = complex(x, y)
            julia(c)
            pg.display.flip()
        elif new_set == "n":
            running = False

    clock.tick(60)

pg.quit()
