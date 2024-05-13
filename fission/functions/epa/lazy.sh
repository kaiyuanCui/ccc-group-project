zip -r epa.zip .
mv epa.zip ../

cd ../..
fission package update --sourcearchive ./functions/epa.zip\
  --env python\
  --name epa\
  --buildcmd './build.sh'

fission fn update --name epa