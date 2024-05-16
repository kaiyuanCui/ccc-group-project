cd api/
zip -r api.zip .
mv api.zip ../

cd ..
fission package update --force --sourcearchive ./api.zip\
  --env python-39\
  --name api\
  --buildcmd './build.sh'
