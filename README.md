sudo docker run --rm -d \
  --network=host \
  --name prometheus\
  -v /home/ec2-user/DataCollection/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --web.enable-lifecycle