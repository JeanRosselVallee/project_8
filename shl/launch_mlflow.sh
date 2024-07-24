source ~/project_8/my_env/bin/activate
pkill -f ":5677"
sleep 3
nohup mlflow models serve -m ~/project_8/data/model/ -p 5677 -h 0.0.0.0 --no-conda &
sleep 6
ps aux | grep "scoring_server" | grep -v "grep" | awk '{print $2, $15, $19}'
