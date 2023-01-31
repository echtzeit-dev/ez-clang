FROM ubuntu:20.04
LABEL maintainer="weliveindetail <stefan.graenitz@gmail.com>"

ARG VERSION=0.0.6

# Tools we need at setup and runtime
# Note: PlatformIO has no toolchain packages for arm-linux-gnueabihf (yet)
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
        ca-certificates wget make libtinfo5 python3 python3-pip python3-dev \
        build-essential gcc-arm-linux-gnueabihf g++-arm-linux-gnueabihf \
        qemu-system-arm && \
    apt clean autoclean && apt autoremove --yes
RUN pip3 install -U platformio && \
    platformio platform install atmelsam \
        --with-package framework-arduino-sam \
        --with-package toolchain-gccarmnoneeabi \
        --with-package uploader && \
    platformio system prune --force

RUN mkdir -p /usr/lib/ez-clang/$VERSION

# Install Python device configuration layer
RUN wget -q -O /tmp/ez-clang-pycfg.tar.gz \
    https://github.com/echtzeit-dev/ez-clang-pycfg/archive/refs/tags/v$VERSION.tar.gz && \
    tar zxf /tmp/ez-clang-pycfg.tar.gz -C /tmp && \
    mv /tmp/ez-clang-pycfg-$VERSION /usr/lib/ez-clang/$VERSION/pycfg && \
    cd /usr/lib/ez-clang/$VERSION/pycfg && \
    python3 -m pip install -e .share && \
    python3 -m pip install -r requirements.txt && \
    rm -rf /tmp/*

# Build and install standard libraries and extra packages
RUN wget -q -O /tmp/ez-clang-libs.tar.gz \
    https://github.com/echtzeit-dev/ez-clang-libs/archive/refs/tags/v$VERSION.tar.gz && \
    tar zxf /tmp/ez-clang-libs.tar.gz -C /tmp && \
    cd /tmp/ez-clang-libs-$VERSION && \
    ./build.sh && \
    mkdir -p /usr/lib/ez-clang/$VERSION/packages && \
    mv .packages/toolchain-clang-arm /usr/lib/ez-clang/$VERSION/packages/. && \
    mv .packages/framework-arduino-sam /usr/lib/ez-clang/$VERSION/packages/. && \
    mkdir -p /usr/lib/ez-clang/$VERSION/stdlib && \
    mv due /usr/lib/ez-clang/$VERSION/stdlib/. && \
    cd / && rm -rf /tmp/*

## Build and install Arduino firmwares
RUN wget -q -O /tmp/ez-clang-arduino.tar.gz \
    https://github.com/echtzeit-dev/ez-clang-arduino/archive/refs/tags/v$VERSION.tar.gz && \
    tar zxf /tmp/ez-clang-arduino.tar.gz -C /tmp && \
    cd /tmp/ez-clang-arduino-$VERSION && \
    LLVM_BIN=/usr/lib/ez-clang/$VERSION/packages/toolchain-clang-arm/bin platformio run && \
    platformio package install --tool tool-bossac && \
    platformio package install --tool tool-teensy && \
    rm .pio/build/due/firmware.*.bak && \
    mkdir -p /usr/lib/ez-clang/$VERSION/firmware/due && \
    mkdir -p /usr/lib/ez-clang/$VERSION/firmware/adafruit_metro_m0 && \
    mkdir -p /usr/lib/ez-clang/$VERSION/firmware/teensylc && \
    mv .pio/build/due/firmware.* /usr/lib/ez-clang/$VERSION/firmware/due/. && \
    mv .pio/build/adafruit_metro_m0/firmware.* /usr/lib/ez-clang/$VERSION/firmware/adafruit_metro_m0/. && \
    mv .pio/build/teensylc/firmware.* /usr/lib/ez-clang/$VERSION/firmware/teensylc/. && \
    cd / && rm -rf /tmp/*

# Build and install QEMU firmwares
RUN wget -q -O /tmp/ez-clang-qemu.tar.gz \
    https://github.com/echtzeit-dev/ez-clang-qemu/archive/refs/tags/v$VERSION.tar.gz && \
    tar zxf /tmp/ez-clang-qemu.tar.gz -C /tmp && \
    cd /tmp/ez-clang-qemu-$VERSION && \
    export PATH=$PATH:$HOME/.platformio/packages/toolchain-gccarmnoneeabi/bin && \
    ./lm3s811_debug.sh && \
    ./lm3s811_release.sh && \
    ./lm3s811_install.sh && \
    cd / && rm -rf /tmp/*

# Build and install Linux-based remote hosts
# Note: We installed arm-linux-gnueabihf packages upfront
#       (permanently, as we need stdlib headers at runtime)
# Note: So far testing focused on debug builds, so let's stick with it for now
RUN wget -q -O /tmp/ez-clang-linux.tar.gz \
    https://github.com/echtzeit-dev/ez-clang-linux/archive/refs/tags/v$VERSION.tar.gz && \
    tar zxf /tmp/ez-clang-linux.tar.gz -C /tmp && \
    apt update && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
        cmake ninja-build && \
    mkdir -p /tmp/ez-clang-linux-$VERSION/build && \
    cd /tmp/ez-clang-linux-$VERSION/build && \
    CC=arm-linux-gnueabihf-gcc CXX=arm-linux-gnueabihf-g++ cmake -GNinja -DCMAKE_BUILD_TYPE=Debug .. && \
    ninja ez-clang-linux-socket && \
    mkdir -p /usr/lib/ez-clang/0.0.6/raspi32 && \
    mv ez-clang-linux-socket /usr/lib/ez-clang/$VERSION/raspi32/. && \
    apt remove --yes cmake ninja-build && apt clean autoclean && apt autoremove --yes && \
    cd / && rm -rf /tmp/*

# Install llvm-symbolizer for readable crash dumps
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install --yes --no-install-recommends \
        gpg-agent lsb-release software-properties-common && \
    wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - && \
    add-apt-repository 'deb http://apt.llvm.org/focal/ llvm-toolchain-focal-13 main' && \
    apt update && DEBIAN_FRONTEND=noninteractive apt install --yes --no-install-recommends llvm-13 && \
    apt remove --yes gpg-agent lsb-release software-properties-common && apt clean autoclean && apt autoremove --yes && \
    ln -s /usr/bin/llvm-symbolizer-13 /usr/bin/llvm-symbolizer

# Wire up clang resource directory. The REPL version in 0.0.6 was forked from
# mainline LLVM at db9c2d775130a110ada89decff7002c64cdd3364, which is closer to
# release 13.0.0 than it is to 14.0.0 (the major version, however, was bumped to
# 14.0.0 already).
RUN mkdir -p /usr/lib/clang && \
    ln -s /usr/lib/ez-clang/$VERSION/packages/toolchain-clang-arm/lib/clang/13.0.0/include /usr/lib/clang/14.0.0

# Add resources bundled with this Dockerfile
COPY .ez_clang_history $HOME/.ez_clang_history

# Download and symlink the actual release binary
RUN wget -q -O /usr/bin/ez-clang-$VERSION \
    https://github.com/echtzeit-dev/ez-clang/releases/download/v$VERSION/ez-clang-$VERSION-x86_64-pc-linux-gnu && \
    chmod +x /usr/bin/ez-clang-$VERSION && \
    ln -s /usr/bin/ez-clang-$VERSION /usr/bin/ez-clang

ENTRYPOINT ["/usr/bin/ez-clang"]
