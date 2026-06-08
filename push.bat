@echo off
cd /d "F:\qgis\Full process"
git add .
git commit -m "添加地形图图层和海拔控件"
git push origin main
pause