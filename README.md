# TDAzureMerger
 A component to merge point clouds from the Kinect Azure devices
 
The method used here is based on the open3D library:
http://www.open3d.org/

This method is very fast and easy to use. Best of all is that it is fully automatic, so you don’t need any boards like chess patterns or charuco. The current version has however some limitations as it works really well for situations where you have enough overlap between kinects from a similar angle, but does not work when you have the kinects in angles bigger then 90 degrees, since it depends on overlapping data from similar pov's.

There are workarounds for that, as I have managed to do calibrate Kinects from any position by using intermediate matrices. That option however is not yet included in this version, since that needs more work to function as a general purpose solution. More updates to come later on!

# Installation

You need to have a working version of the open3D library in TouchDesigner.

You can pip install it:

```
# Install Open3D stable release with pip
$ pip install open3d

# Install Open3D stable release with Conda
$ conda install -c open3d-admin -c conda-forge open3d

# Test the installation
$ python -c "import open3d as o3d; print(o3d)"
```

# Version

Do note that this tool was built with version 0.11.0, so there may be incompatibilities with later versions of the library online (current version is 0.12.0) which I have not tested. This repository contains version 0.11.0, so you can use that if you run into trouble.

# Support

If you enjoy this or other of my open-source projects, you can [make a donation]
(https://darienbrito.com/support/)

Darien Brito, 2021
