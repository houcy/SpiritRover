OpenCV Installed from Source via the following instructions:

    sudo apt-get update
    sudo apt-get upgrade
    sudo rpi-update
    sudo reboot
    sudo apt-get install build-essential git cmake pkg-config \
      libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev \
      libavcodec-dev libavformat-dev libswscale-dev \
      libv4l-dev libxvidcore-dev libx264-dev libgtk2.0-dev \
      libatlas-base-dev gfortran python2.7-dev python3-dev python-pip \
      python-numpy python-scipy python-picamera
    
    
    cd ~
    git clone https://github.com/opencv/opencv.git
    cd opencv
    git checkout 3.4.0
    cd ~
    git clone https://github.com/opencv/opencv_contrib.git
    cd opencv_contrib
    git checkout 3.4.0
    
    
    cd ~/opencv
    mkdir build
    cd build
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
     -D CMAKE_INSTALL_PREFIX=/usr/local \
     -D INSTALL_C_EXAMPLES=OFF \
     -D INSTALL_PYTHON_EXAMPLES=ON \
     -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
     -D BUILD_EXAMPLES=ON ..
    make -j3 
    sudo make install
    sudo ldconfig


Other tools I've found useful:

http://abyz.me.uk/rpi/pigpio/piscope.html


