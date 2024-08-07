#!/bin/bash

# 查找监听端口3000的进程ID
PID=$(lsof -t -i:3000)

# 如果找到了进程ID，则终止该进程
if [ ! -z "$PID" ]; then
  echo "Killing process on port 3000 with PID: $PID"
  kill -9 $PID
else
  echo "No process found on port 3000."
fi