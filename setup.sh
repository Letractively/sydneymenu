echo "Welcome using sydney-scent project ..."

uname -a

echo "Checking Django Version ..."
python djv.py
if [ $? -gt 0 ]; then
  echo "Fail: Django 1.3+ required ...";
  exit 1;
fi

echo "Clean folders ..."
rm -rf pybb
rm -rf django*
rm -rf res.tar.gz
rm -rf res
rm -rf ./adult/res
echo " === Done ==="
echo "Getting pyBB ..." 
hg clone https://bitbucket.org/lorien/pybb
if [ $? -gt 0 ]; then
  echo " === Can not clone pybb, check your network and mecrial installation!"
  exit 1
fi
echo " === Done ==="

echo "Getting django-common"
hg clone https://bitbucket.org/lorien/django-common
if [ $? -gt 0 ]; then
  echo " === Can not clone django-common, check your network and mecrial installation!"
  exit 1
fi
echo " === Done ==="

echo "Getting Res Folder"
wget http://sydneymenu.googlecode.com/files/res.tar.gz
if [ $? -gt 0 ]; then
  echo "Can not get res folder, check your internet connection ...";
  exit 1;
fi
tar -xf res.tar.gz
echo " === Done ==="

echo "Making Symbolic Links"
cd ./main
rm -f pybb
rm -f common
ln -s ../pybb/pybb ./
ln -s ../django-common/common ./
ln -s ../res ./

echo "Synchronize DB"
python manage.py syncdb

cd ..

echo "Initialize DB"
python dbinit.py setup

echo "All done! Enjoy your sydneymenu"
