# Golden Eagle

0. For all the details regarding this project visit the [wiki page](https://github.com/G-KUMAR/golden_eagle/wiki)

1. Instal Voxel Grid 
	sudo apt-get install ros-kinetic-voxel-grid

2. -ros-pkg/ : for px4 flow  - Run:  
	git submodule sync --recursive 
	git submodule update --init  --recursive

Finally- for optimization build using

 	catkin_make -DCMAKE_BUILD_TYPE=Release
