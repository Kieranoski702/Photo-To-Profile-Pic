#!/usr/bin/python3
# -----------------------------------------------------------------------------
# photo_changer.py -- Script to change the size of photos to 100x100 pixels
#                     and make them into circles.
#
# July 2023, Kieran Fowlds
# -----------------------------------------------------------------------------

"""
Script to change the size of photos to 100x100 pixels and make them into
circles. The script takes two directories as input, one containing photos
that are already in a circle shape, and one containing photos that are not.
The script will then make them into circles if they are not already and resize the 
image to 100x100 pixels. The script will then save the photos to a specified 
output directory in both PNG and JPEG format.
"""

import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageOps


def process_images(non_circle_input_dir, circle_input_dir, output_dir):
    """
    Processes the images in the input directories and saves them to the output
    directory.

    :param non_circle_input_dir:
        The directory containing the non-circle images.

    :param circle_input_dir:
        The directory containing the circle images.

    :param output_dir:
        The directory to save the images to.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(circle_input_dir):
        input_path = os.path.join(circle_input_dir, filename)

        if not os.path.isfile(input_path):
            continue

        image = Image.open(input_path)
        image = image.resize((100, 100))

        save_image(image, output_dir, filename)

    for filename in os.listdir(non_circle_input_dir):
        input_path = os.path.join(non_circle_input_dir, filename)

        if not os.path.isfile(input_path):
            continue

        image = Image.open(input_path)
        image = crop_to_circle(image)
        image = image.resize((100, 100), resample=Image.BICUBIC)

        save_image(image, output_dir, filename)


def crop_to_circle(image):
    """
    Crops the image to a circle shape.

    :param image:
        The image to crop.

    :return:
        The cropped image.
    """
    size = min(image.size)
    background = Image.new("RGBA", image.size, (255, 255, 255, 0))
    mask = Image.new("RGBA", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=(255, 255, 255, 255))

    image = Image.composite(image, background, mask)
    image = image.crop((0, 0, size, size))
    return image


def save_image(image, output_dir, filename):
    """
    Saves the image to the output directory in both PNG and JPEG format.

    :param image:
        The image to save.

    :param output_dir:
        The directory to save the image to.

    :param filename:
        The name of the file to save the image as.
    """
    output_name = os.path.splitext(filename)[0]
    output_path_png = os.path.join(output_dir, f"{output_name}.png")
    image.save(output_path_png, format="PNG", compress_level=9)
    if "A" in image.mode:
        # Extract the alpha channel and invert it
        alpha = image.getchannel("A")
        alpha = ImageOps.invert(alpha)
        # Paste white onto image wherever it is transparent
        image.paste((255, 255, 255), mask=alpha)
        # Convert to RGB
        image = image.convert("RGB")
    output_path_jpg = os.path.join(output_dir, f"{output_name}.jpg")
    image.save(output_path_jpg, format="JPEG", quality=100)


def parse_args(argv):
    """
    Parses the command line arguments.

    :param argv:
        The command line arguments to parse.
    """
    parser = argparse.ArgumentParser(description="Process images.")
    parser.add_argument(
        "-n",
        "--non-circle-input-directory",
        type=str,
        help="The directory containing the non-circle images.",
    )
    parser.add_argument(
        "-c",
        "--circle-input-directory",
        type=str,
        help="The directory containing the circle images.",
    )
    parser.add_argument(
        "-o",
        "--output-directory",
        type=str,
        help="The directory to save the images to.",
    )
    return parser.parse_args(argv)


def main(argv):
    """
    Main function that runs the script.
    """
    args = parse_args(argv)

    process_images(
        args.non_circle_input_directory,
        args.circle_input_directory,
        args.output_directory,
    )


if __name__ == "__main__":
    main(sys.argv[1:])
