@echo off
cd /d "F:\qgis\Full process"
git add .
git commit -m "回退版本"
git push origin main
pause