```
docker compose build
sudo systemctl stop systemd-resolved
docker compose up
```
```
sudo systemctl restart systemd-resolved
sudo lsof -i:53
```
