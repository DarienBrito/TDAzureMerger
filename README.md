# TDAzureMerger
A TouchDesigner component for merging point clouds from Kinect Azure devices using the Open3D library.

## Overview
TDAzureMerger is a tool designed to combine point clouds captured by multiple Kinect Azure devices into a single, cohesive point cloud. Built on the robust [Open3D library](http://www.open3d.org/) (version 0.19.0), it integrates seamlessly with TouchDesigner for real-time 3D data processing. This tool is ideal for applications requiring high-fidelity point cloud data from multiple perspectives.

## Usage
To see TDAzureMerger in action, check out this instructional video:  
[Watch on Vimeo](https://vimeo.com/501525725)

The component is designed for straightforward integration into TouchDesigner projects. It processes point cloud data from Kinect Azure devices, aligning and merging them based on overlapping regions. Refer to the video for a step-by-step guide on setup and usage.

## Features
- **Point Cloud Merging**: Combines data from multiple Kinect Azure devices into a unified point cloud.
- **Open3D Integration**: Leverages Open3D (v0.19.0) for robust point cloud processing.
- **TouchDesigner Compatibility**: Optimized for Python 3.11, the default Python version in the latest TouchDesigner builds.
- **Real-Time Processing**: Suitable for interactive installations and live performances.

## Limitations
The current version of TDAzureMerger has some constraints:
- **Overlap Requirement**: Works best when Kinect devices have significant overlap and are positioned at similar angles (less than 90 degrees apart). It struggles with configurations where cameras face each other directly.
- **Calibration Workaround**: Support for arbitrary Kinect positions (using intermediate calibration matrices) is under development and not yet included in this version.
- **Future Updates**: Enhanced calibration and general-purpose functionality are planned for future releases.

For scenarios requiring non-overlapping or opposing camera setups, stay tuned for updates addressing these challenges.

## Installation
To use TDAzureMerger, you need Open3D (v0.19.0) installed for Python 3.11, which is the Python version supported by the latest TouchDesigner builds. Follow these steps:

### Prerequisites
- Ensure your local Python installation is version **3.11** to avoid compatibility issues.
- Install TouchDesigner (latest build recommended).
- Familiarize yourself with Python integration in TouchDesigner: [Python in TouchDesigner](https://derivative.ca/UserGuide/Python).

### Installing Open3D
There are two methods to install Open3D:

#### Option 1: Install via pip (Recommended)
Run the following command in a terminal with Python 3.11:
```
pip install open3d==0.19.0
```

#### Option 2: Install via Conda
If you prefer Conda, use:
```
conda install -c open3d-admin -c conda-forge open3d=0.19.0
```

#### Option 3: Manual Installation (Not Recommended)
Download Open3D (v0.19.0) from the [Open3D documentation](http://www.open3d.org/docs/release/getting_started.html) and copy the library to TouchDesigner’s site-packages folder, typically located at:
```
C:\Program Files\Derivative\TouchDesigner\bin\Lib\site-packages
```

#### Verify Installation
Test your Open3D installation by running:
```
python -c "import open3d as o3d; print(o3d.__version__)"
```
Ensure the output shows `0.19.0`.

### Troubleshooting
- If you encounter issues, verify that your Python version is 3.11.
- Ensure Open3D is installed in the Python environment used by TouchDesigner.
- For additional help, consult the [TouchDesigner Python Guide](https://derivative.ca/UserGuide/Python).

## Support
For updates, tips, and community interaction, follow me on:  
- [Instagram](https://www.instagram.com/darien.brito/)  
- [Twitter](https://twitter.com/DarienBrito)  

To support further development of TDAzureMerger and related projects, consider subscribing on:  
- [Patreon](https://www.patreon.com/c/darienbrito)

## Contributing
Feedback and contributions are welcome! If you encounter issues or have suggestions, please submit them via the project’s repository (link to be added in future updates) or contact me directly.

## About the Author
Developed by Darien Brito, 2025.  
This tool is part of ongoing efforts to enhance real-time 3D processing in creative applications.
