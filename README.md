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

You need to have a working version of the open3D library in TouchDesigner. This build has been updated to work with version 0.16.0. You may go to this website and download the corresponding open3D version for **python 3.9, which is the currently supported python build in TouchDesigner**. There are two ways to install open3D for work within TD. One of them is to download a build from here [Open3D docs](http://www.open3d.org/docs/release/getting_started.html), which you can then use by copying it to your TouchDesigner site packages folder, usually in a path like this:

```
C:\Program Files\Derivative\TouchDesigner\bin\Lib\site-packages
```

You can also try the easier way, which is installing via pip or conda:

```
# Install Open3D stable release with pip
$ pip install open3d

# Install Open3D stable release with Conda
$ conda install -c open3d-admin -c conda-forge open3d

# Test the installation
$ python -c "import open3d as o3d; print(o3d)"
```

Remember that this tool was built with version 0.16.0 of the library, for python 3.9 (the one in use current TD build), so to install via pip, your local python install must be version 3.9, otherwise there may be incompatibilities. Please make sure you have this setup correctly before submiting an issue.

# Support

It helps me a lot if you can follow me on:

[Instagram](https://www.instagram.com/darien.brito/)
[Twitter](https://twitter.com/DarienBrito)

If you would like to go one step further with your support, I highly encourage you to make a donation to one of the following organizations. They are doing important and urgent work and need your donation more than I do:

[Refugees International](https://www.refugeesinternational.org/)
[Coalition of Rainforest Nations](https://www.rainforestcoalition.org/)
[Amazon Frontlines](https://amazonfrontlines.org/)
[Wikipedia](https://donate.wikimedia.org/w/index.php?title=Special:LandingPage&country=NL&uselang=en&utm_medium=spontaneous&utm_source=fr-redir&utm_campaign=spontaneous)

Sincerely,
Darien

Darien Brito, 2022
