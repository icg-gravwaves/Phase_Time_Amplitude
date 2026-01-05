#!/usr/bin/env python3
import argparse
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def parse_args():
    p = argparse.ArgumentParser(description="Combine plot images into a grid.")
    p.add_argument("--images", nargs="+", required=True)
    p.add_argument("--titles", nargs="*", default=None)
    p.add_argument("--output", default="combined_grid.png")
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    images = args.images
    n = len(images)

    # 1. Calculate grid dimensions
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)

    # 2. Get the aspect ratio of the first image to prevent gaps
    first_img = mpimg.imread(images[0])
    img_h, img_w = first_img.shape[:2]
    aspect_ratio = img_h / img_w

    # 3. Adjust figsize so the "canvas" matches the grid shape
    # This prevents the vertical/horizontal gaps between rows/cols
    fig_width = 5 * cols
    fig_height = (5 * rows) * aspect_ratio

    # 4. Use subplots_adjust for total control over spacing
    fig, axes = plt.subplots(rows, cols, figsize=(fig_width, fig_height))
    
    if n == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    for i, img_path in enumerate(images):
        img = mpimg.imread(img_path)
        axes[i].imshow(img)
        axes[i].axis("off")

        if args.titles and i < len(args.titles):
            axes[i].set_title(args.titles[i])

    # Hide unused slots
    for j in range(n, len(axes)):
        axes[j].axis("off")

    # 5. The "Magic" Trio to remove white space:
    # Use subplots_adjust to set spacing to zero
    plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
    
    # Save with high DPI for sharpness and 'tight' to crop edges
    plt.savefig(args.output, dpi=300, bbox_inches='tight', pad_inches=0)
    print(f"Saved: {args.output}")
