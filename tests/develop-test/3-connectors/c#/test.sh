#!/bin/bash
function stopTaosd {
  echo "Stop taosd"
  sudo systemctl stop taosd || echo 'no sudo or systemctl or stop fail'
  PID=`ps -ef|grep -w taosd | grep -v grep | awk '{print $2}'`
  while [ -n "$PID" ]
  do
    pkill -TERM -x taosd
    sleep 1
    PID=`ps -ef|grep -w taosd | grep -v grep | awk '{print $2}'`
  done
}
stopTaosd
rm -rf /var/lib/taos/*
rm -rf /var/log/taos/*
nohup taosd -c /etc/taos/ > /dev/null 2>&1 &
sleep 10
cd ../../
WKC=`pwd`
cd ${WKC}/src/connector/C#
dotnet test
# run example under Driver
cd ${WKC}/src/connector/C#/examples 
dotnet run

#dotnet run --project src/test/Cases/Cases.csproj

# run example with neuget package
cd ${WKC}/tests/examples/C#
dotnet run --project C#checker/C#checker.csproj
dotnet run --project TDengineTest/TDengineTest.csproj
dotnet run --project schemaless/schemaless.csproj
dotnet run --project jsonTag/jsonTag.csproj
dotnet run --project stmt/stmt.csproj

cd ${WKC}/tests/examples/C#/taosdemo
dotnet build -c Release
tree | true
./bin/Release/net5.0/taosdemo -c /etc/taos -y
