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

You need to have a working version of the open3D library in TouchDesigner. This build has been updated to work with version 0.19.0. You may go to this website and download the corresponding open3D version for **python 3.11, which is the currently supported python build in TouchDesigner**. There are two ways to install open3D for work within TD. One of them is to download a build from here [Open3D docs](http://www.open3d.org/docs/release/getting_started.html), which you can then use by copying it to your TouchDesigner site packages folder (not recommended), usually in a path like this:

```
C:\Program Files\Derivative\TouchDesigner\bin\Lib\site-packages
```

Or you can also try the easier and recommended way, which is installing via pip or conda:

```
# Install Open3D stable release with pip
$ pip install open3d

# Install Open3D stable release with Conda
$ conda install -c open3d-admin -c conda-forge open3d

# Test the installation
$ python -c "import open3d as o3d; print(o3d)"
```

Remember that this tool was built with version 0.19.0 of the library, for python 3.11 (the one in use current TD build), so **to install via pip, your local python install must be version 3.11, otherwise there may be incompatibilities**. Please make sure you have this setup correctly before submiting an issue.

If you are not familiar with how Python works in TD, please refer to this article first: [Python in TouchDesigner](https://derivative.ca/UserGuide/Python)

# Support

You can follow me on:

[Instagram](https://www.instagram.com/darien.brito/) |
[Twitter](https://twitter.com/DarienBrito)

If you would like to go one step further with your support, you can subscribe here:
[Patreon](https://www.patreon.com/c/darienbrito)

Best,
Darien

Darien Brito, 2025
