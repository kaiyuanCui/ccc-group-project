cd bom_data/
zip -r bom_data.zip .
mv bom_data.zip ../

cd ..
fission package update --sourcearchive ./bom_data.zip\
  --env python-39\
  --name bom-data\
  --buildcmd './build.sh'
  
