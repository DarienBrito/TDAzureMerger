# TDAzureMerger
 A component to merge point clouds from the Kinect Azure devices

The technique used here is based on the open3D library: http://www.open3d.org/

# Usage

You can see how to use the tool in the following video:
https://vimeo.com/501525725

# Limitations

The current version has however some limitations. It only works really well for situations where you have enough overlap between Kinects from a similar angle, but does not work when you have the Kinects in angles bigger than 90 degrees, since it depends on overlapping data from similar pov's (it won't work with cameras facing each other for instance)

There are workarounds for that. I have managed to calibrate Kinects from any position by using intermediate matrices in calibration. That option however is not yet included in this version, since that needs more work to function as a general-purpose solution. More updates to come later on.

# Installation

You need to have a working version of the open3D library in TouchDesigner. This repository contains version 0.11.0, so you can use that directly by copying it to your TouchDesigner site packages folder, usually in a path like this:

```
C:\Program Files\Derivative\TouchDesigner.2020.28110\bin\Lib\site-packages
```

You can also try pip or conda install:

```
# Install Open3D stable release with pip
$ pip install open3d

# Install Open3D stable release with Conda
$ conda install -c open3d-admin -c conda-forge open3d

# Test the installation
$ python -c "import open3d as o3d; print(o3d)"
```
Do note however that this tool was built with version 0.11.0, so there may be incompatibilities with later versions of the library online (current version is 0.12.0) which I have not tested. Safest is to simply use version 0.11.0 (the one provided with this package).

Darien Brito, 2021
