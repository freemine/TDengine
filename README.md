<p align="center">
  <a href="https://tdengine.com" target="_blank">
  <img
    src="docs/assets/tdengine.svg"
    alt="TDengine"
    width="500"
  />
  </a>
</p>

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/taosdata/tdengine/taosd-ci-build.yml)](https://github.com/taosdata/TDengine/actions/workflows/taosd-ci-build.yml)
[![Coverage Status](https://coveralls.io/repos/github/taosdata/TDengine/badge.svg?branch=3.0)](https://coveralls.io/github/taosdata/TDengine?branch=3.0)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/taosdata/tdengine)
<br />
![GitHub Release](https://img.shields.io/github/v/release/taosdata/tdengine)
![GitHub License](https://img.shields.io/github/license/taosdata/tdengine)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/4201/badge)](https://bestpractices.coreinfrastructure.org/projects/4201)
<br />
[![Twitter Follow](https://img.shields.io/twitter/follow/tdenginedb?label=TDengine&style=social)](https://twitter.com/tdenginedb)
[![YouTube Channel](https://img.shields.io/badge/Subscribe_@tdengine--white?logo=youtube&style=social)](https://www.youtube.com/@tdengine)
[![Discord Community](https://img.shields.io/badge/Join_Discord--white?logo=discord&style=social)](https://discord.com/invite/VZdSuUg4pS)
[![LinkedIn](https://img.shields.io/badge/Follow_LinkedIn--white?logo=linkedin&style=social)](https://www.linkedin.com/company/tdengine)
[![StackOverflow](https://img.shields.io/badge/Ask_StackOverflow--white?logo=stackoverflow&style=social&logoColor=orange)](https://stackoverflow.com/questions/tagged/tdengine)

English | [简体中文](README-CN.md) | [TDengine Cloud](https://cloud.tdengine.com) | [Learn more about TSDB](https://tdengine.com/tsdb/)

# Table of Contents

1. [Introduction](#1-introduction)
1. [Documentation](#2-documentation)
1. [Prerequisites](#3-prerequisites)
    - [3.1 Prerequisites On Linux](#31-on-linux)
    - [3.2 Prerequisites On macOS](#32-on-macos)
    - [3.3 Prerequisites On Windows](#33-on-windows) 
    - [3.4 Clone the repo](#34-clone-the-repo) 
1. [Building](#4-building)
    - [4.1 Build on Linux](#41-build-on-linux)
    - [4.2 Build on macOS](#42-build-on-macos)
    - [4.3 Build On Windows](#43-build-on-windows) 
1. [Packaging](#5-packaging)
1. [Installation](#6-installation)
    - [6.1 Install on Linux](#61-install-on-linux)
    - [6.2 Install on macOS](#62-install-on-macos)
    - [6.3 Install on Windows](#63-install-on-windows)
1. [Running](#7-running)
    - [7.1 Run TDengine on Linux](#71-run-tdengine-on-linux)
    - [7.2 Run TDengine on macOS](#72-run-tdengine-on-macos)
    - [7.3 Run TDengine on Windows](#73-run-tdengine-on-windows)
1. [Testing](#8-testing)
1. [Releasing](#9-releasing)
1. [Workflow](#10-workflow)
1. [Coverage](#11-coverage)
1. [Contributing](#12-contributing)

# 1. Introduction

TDengine is an open source, high-performance, cloud native [time-series database](https://tdengine.com/tsdb/) optimized for Internet of Things (IoT), Connected Cars, and Industrial IoT. It enables efficient, real-time data ingestion, processing, and monitoring of TB and even PB scale data per day, generated by billions of sensors and data collectors. TDengine differentiates itself from other time-series databases with the following advantages:

- **[High Performance](https://tdengine.com/tdengine/high-performance-time-series-database/)**: TDengine is the only time-series database to solve the high cardinality issue to support billions of data collection points while out performing other time-series databases for data ingestion, querying and data compression.

- **[Simplified Solution](https://tdengine.com/tdengine/simplified-time-series-data-solution/)**: Through built-in caching, stream processing and data subscription features, TDengine provides a simplified solution for time-series data processing. It reduces system design complexity and operation costs significantly.

- **[Cloud Native](https://tdengine.com/tdengine/cloud-native-time-series-database/)**: Through native distributed design, sharding and partitioning, separation of compute and storage, RAFT, support for kubernetes deployment and full observability, TDengine is a cloud native Time-Series Database and can be deployed on public, private or hybrid clouds.

- **[Ease of Use](https://tdengine.com/tdengine/easy-time-series-data-platform/)**: For administrators, TDengine significantly reduces the effort to deploy and maintain. For developers, it provides a simple interface, simplified solution and seamless integrations for third party tools. For data users, it gives easy data access.

- **[Easy Data Analytics](https://tdengine.com/tdengine/time-series-data-analytics-made-easy/)**: Through super tables, storage and compute separation, data partitioning by time interval, pre-computation and other means, TDengine makes it easy to explore, format, and get access to data in a highly efficient way.

- **[Open Source](https://tdengine.com/tdengine/open-source-time-series-database/)**: TDengine’s core modules, including cluster feature, are all available under open source licenses. It has gathered 19.9k stars on GitHub. There is an active developer community, and over 139k running instances worldwide.

For a full list of TDengine competitive advantages, please [check here](https://tdengine.com/tdengine/). The easiest way to experience TDengine is through [TDengine Cloud](https://cloud.tdengine.com).

# 2. Documentation

For user manual, system design and architecture, please refer to [TDengine Documentation](https://docs.tdengine.com) ([TDengine 文档](https://docs.taosdata.com))

# 3. Prerequisites

## 3.1 On Linux

<details>

<summary>Install required tools on Linux</summary>

### For Ubuntu 18.04、20.04、22.04

```bash
sudo apt-get udpate
sudo apt-get install -y gcc cmake build-essential git libjansson-dev \
  libsnappy-dev liblzma-dev zlib1g-dev pkg-config
```

### For CentOS 8

```bash
sudo yum update
yum install -y epel-release gcc gcc-c++ make cmake git perl dnf-plugins-core 
yum config-manager --set-enabled powertools
yum install -y zlib-static xz-devel snappy-devel jansson-devel pkgconfig libatomic-static libstdc++-static 
```

</details>

## 3.2 On macOS

<details>

<summary>Install required tools on macOS</summary>

Please intall the dependencies with [brew](https://brew.sh/).

```bash
brew install argp-standalone gflags pkgconfig
```

</details>

## 3.3 On Windows

<details>

<summary>Install required tools on Windows</summary>

Work in Progress.

</details>

## 3.4 Clone the repo

<details>

<summary>Clone the repo</summary>

Clone the repository to the target machine:

```bash
git clone https://github.com/taosdata/TDengine.git
cd TDengine
```


> **NOTE:**
> TDengine Connectors can be found in following repositories: [JDBC Connector](https://github.com/taosdata/taos-connector-jdbc), [Go Connector](https://github.com/taosdata/driver-go), [Python Connector](https://github.com/taosdata/taos-connector-python), [Node.js Connector](https://github.com/taosdata/taos-connector-node), [C# Connector](https://github.com/taosdata/taos-connector-dotnet), [Rust Connector](https://github.com/taosdata/taos-connector-rust).

</details>

# 4. Building

At the moment, TDengine server supports running on Linux/Windows/MacOS systems. Any application can also choose the RESTful interface provided by taosAdapter to connect the taosd service. TDengine supports X64/ARM64 CPU, and it will support MIPS64, Alpha64, ARM32, RISC-V and other CPU architectures in the future. Right now we don't support build with cross-compiling environment.

You can choose to install through source code, [container](https://docs.tdengine.com/get-started/deploy-in-docker/), [installation package](https://docs.tdengine.com/get-started/deploy-from-package/) or [Kubernetes](https://docs.tdengine.com/operations-and-maintenance/deploy-your-cluster/#kubernetes-deployment). This quick guide only applies to install from source.

TDengine provide a few useful tools such as taosBenchmark (was named taosdemo) and taosdump. They were part of TDengine. By default, TDengine compiling does not include taosTools. You can use `cmake .. -DBUILD_TOOLS=true` to make them be compiled with TDengine.

To build TDengine, use [CMake](https://cmake.org/) 3.13.0 or higher versions in the project directory.

## 4.1 Build on Linux

<details>

<summary>Detailed steps to build on Linux</summary>

You can run the bash script `build.sh` to build both TDengine and taosTools including taosBenchmark and taosdump as below:

```bash
./build.sh
```

It equals to execute following commands:

```bash
mkdir debug && cd debug
cmake .. -DBUILD_TOOLS=true -DBUILD_CONTRIB=true
make
```

You can use Jemalloc as memory allocator instead of glibc:

```bash
cmake .. -DJEMALLOC_ENABLED=true
```

TDengine build script can auto-detect the host machine's architecture on x86, x86-64, arm64 platform.
You can also specify architecture manually by CPUTYPE option:

```bash
cmake .. -DCPUTYPE=aarch64 && cmake --build .
```

</details>

## 4.2 Build on macOS

<details>

<summary>Detailed steps to build on macOS</summary>

Please install XCode command line tools and cmake. Verified with XCode 11.4+ on Catalina and Big Sur.

```shell
mkdir debug && cd debug
cmake .. && cmake --build .
```

</details>

## 4.3 Build on Windows

<details>

<summary>Detailed steps to build on Windows</summary>

If you use the Visual Studio 2013, please open a command window by executing "cmd.exe".
Please specify "amd64" for 64 bits Windows or specify "x86" for 32 bits Windows when you execute vcvarsall.bat.

```cmd
mkdir debug && cd debug
"C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" < amd64 | x86 >
cmake .. -G "NMake Makefiles"
nmake
```

If you use the Visual Studio 2019 or 2017:

please open a command window by executing "cmd.exe".
Please specify "x64" for 64 bits Windows or specify "x86" for 32 bits Windows when you execute vcvarsall.bat.

```cmd
mkdir debug && cd debug
"c:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" < x64 | x86 >
cmake .. -G "NMake Makefiles"
nmake
```

Or, you can simply open a command window by clicking Windows Start -> "Visual Studio < 2019 | 2017 >" folder -> "x64 Native Tools Command Prompt for VS < 2019 | 2017 >" or "x86 Native Tools Command Prompt for VS < 2019 | 2017 >" depends what architecture your Windows is, then execute commands as follows:

```cmd
mkdir debug && cd debug
cmake .. -G "NMake Makefiles"
nmake
```
</details>

# 5. Packaging

[Placeholder]

# 6. Installation

## 6.1 Install on Linux

<details>

<summary>Detailed steps to install on Linux</summary>

After building successfully, TDengine can be installed by:

```bash
sudo make install
```

Installing from source code will also configure service management for TDengine. Users can also choose to [install from packages](https://docs.tdengine.com/get-started/deploy-from-package/) for it.

</details>

## 6.2 Install on macOS

<details>

<summary>Detailed steps to install on macOS</summary>

After building successfully, TDengine can be installed by:

```bash
sudo make install
```

</details>

## 6.3 Install on Windows

<details>

<summary>Detailed steps to install on windows</summary>

After building successfully, TDengine can be installed by:

```cmd
nmake install
```

</details>

# 7. Running

## 7.1 Run TDengine on Linux

<details>

<summary>Detailed steps to run on Linux</summary>

To start the service after installation on linux, in a terminal, use:

```bash
sudo systemctl start taosd
```

Then users can use the TDengine CLI to connect the TDengine server. In a terminal, use:

```bash
taos
```

If TDengine CLI connects the server successfully, welcome messages and version info are printed. Otherwise, an error message is shown.

If you don't want to run TDengine as a service, you can run it in current shell. For example, to quickly start a TDengine server after building, run the command below in terminal: (We take Linux as an example, command on Windows will be `taosd.exe`)

```bash
./build/bin/taosd -c test/cfg
```

In another terminal, use the TDengine CLI to connect the server:

```bash
./build/bin/taos -c test/cfg
```

Option `-c test/cfg` specifies the system configuration file directory.

</details>

## 7.2 Run TDengine on macOS

<details>

<summary>Detailed steps to run on macOS</summary>

To start the service after installation on macOS, double-click the /applications/TDengine to start the program, or in a terminal, use:

```bash
sudo launchctl start com.tdengine.taosd
```

Then users can use the TDengine CLI to connect the TDengine server. In a terminal, use:

```bash
taos
```

If TDengine CLI connects the server successfully, welcome messages and version info are printed. Otherwise, an error message is shown.

</details>


## 7.3 Run TDengine on Windows

<details>

<summary>Detailed steps to run on windows</summary>

You can start TDengine server on Windows platform with below commands:

```cmd
.\build\bin\taosd.exe -c test\cfg
```

In another terminal, use the TDengine CLI to connect the server:

```cmd
.\build\bin\taos.exe -c test\cfg
```

option "-c test/cfg" specifies the system configuration file directory.

</details>

# 8. Testing

For how to run different types of tests on TDengine, please see [Testing TDengine](./tests/README.md).

# 9. Releasing

For the complete list of TDengine Releases, please see [Releases](https://github.com/taosdata/TDengine/releases).

# 10. Workflow

TDengine build check workflow can be found in this [Github Action](https://github.com/taosdata/TDengine/actions/workflows/taosd-ci-build.yml).

# 11. Coverage

Latest TDengine test coverage report can be found on [coveralls.io](https://coveralls.io/github/taosdata/TDengine)

<details>

<summary> how to run the coverage report locally. </summary>
To create the test coverage report (in HTML format) locally, please run following commands:

```bash
cd tests
bash setup-lcov.sh -v 1.16 && ./run_local_coverage.sh -b main -c task 
# on main branch and run cases in longtimeruning_cases.task 
# for more infomation about options please refer to ./run_local_coverage.sh -h
```
> **NOTE:**
> Please note that the -b and -i options will recompile TDengine with the -DCOVER=true option, which may take a amount of time.

</details>

# 12. Contributing

Please follow the [contribution guidelines](CONTRIBUTING.md) to contribute to TDengine.
