sh -c 'echo "deb http://packages.ros.org/ros/ubuntu trusty main" > /etc/apt/sources.list.d/ros-latest.list'
apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
apt-get update
apt-get install ros-indigo-ros-base
apt-get install ros-indigo-rosbridge-suite ros-indigo-rosserial-server

apt-get install nginx avahi-daemon wireless-tools
apt-get install iw crda wireless-regdb

echo "source /opt/ros/indigo/setup.bash" >> .bashrc

apt-get install python-pip
pip install virtualenv
cd /opt/
virtualenv hbrain
cd hbrain/
source bin/activate
mkdir project
cd project/
apt-get install git
git clone https://github.com/dotbot-io/webapp
mv webapp/ hbrain_server
cd hbrain_server/
git checkout develop
pip install -r requirements.txt

### Wifi Management

apt-get install wpasupplicant
rm /etc/network/interfaces
ln -s /opt/hbrain/hbrain-ci/ext/interfaces /etc/network/interfaces

crontab -l > mycron
echo "@reboot /opt/hbrain/hbrain-ci/ext/autowifi.bash >> /var/log/wifi_auto.log" >> mycron
crontab mycron
rm mycron
update-rc.d cron defaults


echo "[Service]" >> /lib/systemd/system/networking.service.d/network-pre.conf
echo "TimeoutStartSec=1" >> /lib/systemd/system/networking.service.d/network-pre.conf


### WebSheel from

curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
source ~/.bashrc
nvm --version
nvm install v6
npm install pm2 -g
pm2 install pm2-webshell

### ros camera
cd /opt/hbrain-ros/src
git clone https://github.com/RobotWebTools/web_video_server
git clone https://github.com/fpasteau/raspicam_node.git

apt-get install ros-indigo-camera-info-manager ros-indigo-async-web-server-cpp ros-indigo-compressed-image-transport ros-indigo-theora-image-transport
apt-get install rpi-update %% rpi-update


ln -s /usr/lib/arm-linux-gnueabihf/libopencv_calib3d.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_calib3d.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_contrib.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_contrib.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_core.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_core.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_features2d.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_features2d.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_flann.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_flann.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_gpu.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_gpu.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_highgui.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_highgui.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_imgproc.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_imgproc.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_legacy.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_legacy.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_ml.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_ml.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_objdetect.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_objdetect.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_ocl.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_ocl.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_photo.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_photo.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_stitching.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_stitching.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_superres.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_superres.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_ts.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_ts.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_video.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_video.so.2.4.8
ln -s /usr/lib/arm-linux-gnueabihf/libopencv_videostab.so.2.4.9 /usr/lib/arm-linux-gnueabihf/libopencv_videostab.so.2.4.8
