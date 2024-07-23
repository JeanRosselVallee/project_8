nohup jupyter notebook --no-browser  --ip=0.0.0.0 --port=5555 &
sleep 1
jupyter notebook list
echo "Process & Listening Port :"
ps aux | grep "jupy" | grep -v "grep" | awk '{print $2, $15, $19}'
ss -tuln | grep 5555

