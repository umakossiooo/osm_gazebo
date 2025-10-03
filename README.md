# OSM to Gazebo World Generator

This tool converts OpenStreetMap (OSM) data into simulation-ready Gazebo SDF world files. It downloads map data from a specified bounding box and generates 3D worlds suitable for robotics simulation.

## Features

- Download OSM data for any geographic region
- Generate Gazebo SDF world files with roads, buildings, and models
- Create PNG images of the mapped area
- Support for different road types with proper widths
- Interactive mode for coordinate selection
- Stage world file generation for ROS navigation

## Installation

### Prerequisites

Make sure you have Python 3 and pip installed on your system:

```bash
sudo apt update
sudo apt install python3-pip python3-full python3-venv
```

### Step 1: Clone the Repository

```bash
git clone https://github.com/l0g1x/gazebo_osm.git
cd gazebo_osm
```

### Step 2: Create and Activate Virtual Environment

```bash
# Create a virtual environment
python3 -m venv ~/venvs/gazebo_env

# Activate the virtual environment
source ~/venvs/gazebo_env/bin/activate
```

### Step 3: Install Required Python Packages

#### Core Dependencies (Required)
```bash
# Essential packages for OSM processing and world generation
pip install numpy lxml matplotlib
pip install opencv-python
pip install osmapi
```

#### Optional Dependencies

**For enhanced map image generation (optional but recommended):**
```bash
# Install Mapnik for advanced map rendering
sudo apt-get install libmapnik-dev python3-mapnik
pip install mapnik
```

**For testing and development:**
```bash
pip install pep8  # For code style checking
```

## Required Python Modules

The following modules are used in this project:

### Standard Library Modules
- `sys` - System-specific parameters and functions
- `os` - Operating system interface
- `math` - Mathematical functions
- `argparse` - Command-line argument parsing
- `urllib.request` & `urllib.error` - URL handling modules

### Third-Party Dependencies

#### Essential Dependencies
- **`numpy`** - Numerical computing library for array operations and mathematical functions
- **`lxml`** - XML processing library for parsing OSM data
- **`matplotlib`** - Plotting library for visualization
- **`opencv-python` (cv2)** - Computer vision library for image processing and road visualization
- **`osmapi`** - OpenStreetMap API client for data download

#### Optional Dependencies
- **`mapnik`** - Map rendering library for generating detailed map images (optional, enhances image quality)

## User Manual: How to Convert a Map

### Step-by-Step Guide to Convert Any Location to Gazebo World

#### Method 1: Using Interactive Mode (Recommended for Beginners)

1. **Start the interactive mode:**
   ```bash
   source ~/venvs/gazebo_env/bin/activate  # Activate virtual environment
   cd gazebo_osm
   python gz_osm.py --interactive --roads
   ```

2. **Enter coordinates when prompted:**
   - The program will ask for starting coordinates [lon lat]
   - Then ending coordinates [lon lat]
   - Example: For a area in San Francisco:
     - Starting: `-122.0129 37.3596`
     - Ending: `-122.0102 37.3614`

3. **Choose to view the area:** Press Y to confirm the selected area

4. **Wait for processing:** The tool will:
   - Download OSM data from OpenStreetMap
   - Process roads and convert coordinates
   - Generate the SDF file
   - Create a PNG image of the area

#### Method 2: Direct Coordinate Input

If you know the exact coordinates of your desired area:

```bash
python gz_osm.py --roads --boundingbox [MinLon] [MinLat] [MaxLon] [MaxLat]
```

**Example for Central Park, New York:**
```bash
python gz_osm.py --roads --boundingbox -73.9732 40.7644 -73.9489 40.7829
```

#### Method 3: Using an Existing OSM File

If you already have an OSM file:

```bash
python gz_osm.py --roads --inputOsmFile your_map.osm
```

### How to Find Coordinates for Your Desired Location

#### Option 1: Using OpenStreetMap Website
1. Go to [openstreetmap.org](https://www.openstreetmap.org)
2. Navigate to your desired location
3. Click "Export" button
4. Select "Manually select a different area"
5. Draw a rectangle around your area of interest
6. Note the coordinates shown: Left, Bottom, Right, Top
7. Convert to format: `Left Bottom Right Top`

#### Option 2: Using Google Maps
1. Go to [maps.google.com](https://maps.google.com)
2. Right-click on the top-left corner of your desired area
3. Click "What's here?" to get coordinates
4. Repeat for bottom-right corner
5. Format as: `MinLon MinLat MaxLon MaxLat`

#### Option 3: Using Bounding Box Tool
1. Visit [boundingbox.klokantech.com](http://boundingbox.klokantech.com/)
2. Search for your location
3. Draw a rectangle around the area
4. Copy the coordinates in CSV format
5. Rearrange to: `MinLon MinLat MaxLon MaxLat`

### Complete Example: Converting Times Square to Gazebo

Let's convert Times Square area to a Gazebo world:

1. **Find coordinates:**
   - Times Square area: `-73.9876 40.7589 -73.9857 40.7589`

2. **Run the conversion:**
   ```bash
   # Activate environment
   source ~/venvs/gazebo_env/bin/activate
   
   # Navigate to project
   cd gazebo_osm
   
   # Convert with roads, buildings, and models
   python gz_osm.py --displayAll --boundingbox -73.9876 40.7589 -73.9857 40.7614 --directory ./times_square/ --name times_square
   ```

3. **Output files created:**
   - `times_square/outFile.sdf` - Gazebo world file
   - `times_square/map.osm` - Downloaded OSM data
   - `times_square/times_square.png` - Map visualization

4. **Load in Gazebo:**
   ```bash
   gazebo times_square/outFile.sdf
   ```

### Advanced Usage Examples

#### Generate a Complete City Block
```bash
# Download and convert with all features
python gz_osm.py --displayAll --boundingbox -74.0059 40.7589 -74.0020 40.7614 --directory ./city_block/ --name manhattan_block
```

#### Create High-Detail Road Network
```bash
# Focus on roads with lane markings
python gz_osm.py --roads --lanes --boundingbox -122.4194 37.7749 -122.4094 37.7849 --directory ./sf_roads/ --name san_francisco
```

#### Generate Stage World for ROS Navigation
```bash
# Create world compatible with ROS Stage simulator
python gz_osm.py --roads --stage --boundingbox -71.0589 42.3601 -71.0489 42.3701 --directory ./boston_stage/ --name boston_nav
```

#### Use Existing OSM File
```bash
# If you have a custom .osm file
python gz_osm.py --roads --buildings --inputOsmFile my_custom_map.osm --directory ./custom_world/
```

### Understanding the Output

After conversion, you'll get several files:

1. **`outFile.sdf`** - Main Gazebo world file
   - Contains 3D road geometry
   - Includes buildings and models
   - Ready to load in Gazebo

2. **`map.osm`** - Raw OpenStreetMap data
   - XML format with geographic data
   - Can be edited manually if needed

3. **`[name].png`** - Visual map image
   - Bird's eye view of the converted area
   - Useful for verification and documentation

4. **Stage files** (if `--stage` used):
   - `[name].world` - Stage simulator world
   - `[name].yaml` - Configuration file

### Tips for Better Results

1. **Choose appropriate area size:**
   - Too large: Long download time, complex world
   - Too small: May miss important road connections
   - Recommended: 0.01-0.05 degree bounding box

2. **Select areas with good OSM data:**
   - Urban areas usually have better data
   - Check OSM website first to ensure roads are mapped

3. **Use appropriate flags:**
   - `--roads` for navigation scenarios
   - `--buildings` for urban simulation
   - `--models` for realistic environments
   - `--displayAll` for complete scenes

4. **Coordinate format reminder:**
   - Format: `MinLongitude MinLatitude MaxLongitude MaxLatitude`
   - Longitude: East/West (-180 to +180)
   - Latitude: North/South (-90 to +90)

## Basic Usage Examples

### Quick Start
```bash
python gz_osm.py --roads
```

### Interactive Mode
```bash
python gz_osm.py --interactive --roads
```

### Custom Bounding Box
```bash
python gz_osm.py --roads --boundingbox -122.0129 37.3596 -122.0102 37.3614
```

### Generate with Buildings and Models
```bash
python gz_osm.py --displayAll
```

### Output to Specific Directory
```bash
python gz_osm.py --roads --directory ./output/
```

### Generate Stage World Files
```bash
python gz_osm.py --roads --stage --name my_world
```

## Command Line Options

- `-f, --outFile`: Output SDF file name (default: outFile.sdf)
- `-o, --osmFile`: Name of the OSM file generated (default: map.osm)
- `-O, --inputOsmFile`: Use existing OSM file instead of downloading
- `--stage`: Generate Stage world files for ROS
- `--name`: Name for stage output (default: osm-map)
- `-i, --imageFile`: Generate PNG image of the area
- `-d, --directory`: Output directory (default: ./)
- `-l, --lanes`: Export image with lane markings
- `-B, --boundingbox`: Specify bounding box coordinates
- `-r, --roads`: Display roads in the world
- `-m, --models`: Display models (traffic signs, etc.)
- `-b, --buildings`: Display buildings
- `-a, --displayAll`: Display roads, models, and buildings
- `--interactive`: Start interactive coordinate selection mode
- `-dbg, --debug`: Enable debug mode

## File Structure

```
gazebo_osm/
├── gz_osm.py                  # Main executable script
├── source/                    # Source modules
│   ├── dict2sdf.py           # SDF file generation
│   ├── osm2dict.py           # OSM data processing
│   ├── getOsmFile.py         # OSM data download
│   ├── getMapImage.py        # Map image generation
│   ├── laneBoundaries.py     # Lane visualization
│   ├── roadSmoothing.py      # Road smoothing algorithms
│   ├── catmull_rom_spline.py # Spline interpolation
│   ├── createStageFiles.py   # Stage world generation
│   └── dp.py                 # Douglas-Peucker algorithm
├── testFiles/                # Unit tests
├── templates/                # Template files
└── README.md
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure you've activated the virtual environment and installed all required packages.

2. **Mapnik Import Error**: Mapnik is optional. The tool will work without it, but image quality may be reduced.

3. **Network Issues**: If OSM download fails, check your internet connection and try again.

4. **Permission Errors**: Make sure you have write permissions in the output directory.

### Python Version Compatibility

This project requires Python 3.6 or higher. It has been updated from Python 2 to Python 3 syntax.

## Contributing

Feel free to submit issues and enhancement requests. Pull requests are welcome!

## License

This project is open source. Please check the original repository for license information.

## Credits

- Original author: Tashwin Khurana
- Updated for Python 3 compatibility
- OpenStreetMap data © OpenStreetMap contributors