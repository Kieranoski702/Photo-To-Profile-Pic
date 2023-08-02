# Photo to profile picture tool

### Note

I made this to save some work and it is very unlikely to ever help anyone else.
This can produce not great results but out of a sample of 300, 3 images
stretched and had to be fixed manually. Kept here in case someone needs it but
more just to keep all my scripts in one place (github)

### Usage

Basic usage of this tool is as follows

```
./photo_to_profile_pic.py -n [non circle photos directory] -c [circle photos directory] -o [output directory] -r [size to resize to]
```

The program will resize any photo in the circle photos directory to the resize
amount. It will resize and change photos in the non-circle directory to circle
images.

-n, -c and -r are all optional. -r will default to 100 (so 100x100 images).
Omitting -n or -c will simply not run the non circle or circle parts of the
program respectivly as there has been no directory specfied

#### Examples

##### Converting a normal photo to profile picture (circle) photo and resize

```bash
./photo_to_profile_pic.py -n non-circle/ -o outputs/ -r 200
```

##### Resizing a circle photo

```bash
./photo_to_profile_pic.py -n circle/ -o outputs/ -r 200
```

##### Both of the above

```bash
./photo_to_profile_pic.py -n non-circle/ -c circle/ -o outputs/ -r 200
```
