FROM ubuntu:20.04
LABEL maintainer="weliveindetail <stefan.graenitz@gmail.com>"

ARG VERSION=0.0.5

# Tools we need at setup and runtime
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
        ca-certificates wget make libtinfo5 python3 python3-pip socat qemu-system-arm && \
    apt clean autoclean && apt autoremove --yes
RUN pip3 install -U platformio && \
    platformio platform install atmelsam \
        --with-package framework-arduino-sam \
        --with-package toolchain-gccarmnoneeabi && \
    platformio system prune --force

RUN mkdir -p /usr/lib/ez-clang/$VERSION

# Build and install built-in runtime libraries
RUN wget -q --show-progress -O /tmp/ez-clang-libs.tar.gz \
    https://github.com/echtzeit-dev/ez-clang-libs/archive/refs/tags/v$VERSION.tar.gz && \
    tar zxf /tmp/ez-clang-libs.tar.gz -C /tmp && \
    cd /tmp/ez-clang-libs-$VERSION && \
    ./build.sh && \
    mkdir -p /usr/lib/ez-clang/$VERSION/packages && \
    mv .packages/toolchain-clang-arm /usr/lib/ez-clang/$VERSION/packages/. && \
    mv .packages/framework-arduino-sam /usr/lib/ez-clang/$VERSION/packages/. && \
    mv due /usr/lib/ez-clang/$VERSION/. && \
    mv qemu /usr/lib/ez-clang/$VERSION/. && \
    cd / && rm -rf /tmp/*

# Build and install Arduino firmware
RUN wget -q --show-progress -O /tmp/ez-clang-arduino.tar.gz \
    https://github.com/echtzeit-dev/ez-clang-arduino/archive/refs/tags/v0.0.5.tar.gz && \
    tar zxf /tmp/ez-clang-arduino.tar.gz -C /tmp && \
    cd /tmp/ez-clang-arduino-$VERSION && \
    apt update && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends build-essential && \
    LLVM_BIN=/usr/lib/ez-clang/$VERSION/packages/toolchain-clang-arm/bin platformio run -e due && \
    apt remove --yes build-essential && apt clean autoclean && apt autoremove --yes && \
    rm .pio/build/due/firmware.*.bak && \
    mv .pio/build/due/firmware.* /usr/lib/ez-clang/$VERSION/due/. && \
    cd / && rm -rf /tmp/*

# Build and install QEMU firmware
RUN wget -q --show-progress -O /tmp/ez-clang-qemu.tar.gz \
    https://github.com/echtzeit-dev/ez-clang-qemu/archive/refs/tags/v0.0.5.tar.gz && \
    tar zxf /tmp/ez-clang-qemu.tar.gz -C /tmp && \
    cd /tmp/ez-clang-qemu-$VERSION && \
    PATH=$PATH:$HOME/.platformio/packages/toolchain-gccarmnoneeabi/bin ./build.sh && \
    mv bin/ez-clang-qemu.* /usr/lib/ez-clang/$VERSION/qemu/. && \
    cd / && rm -rf /tmp/*

# Install llvm-symbolizer for readable crash dumps
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install --yes --no-install-recommends \
        gpg-agent lsb-release software-properties-common && \
    wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - && \
    add-apt-repository 'deb http://apt.llvm.org/focal/ llvm-toolchain-focal-13 main' && \
    apt update && DEBIAN_FRONTEND=noninteractive apt install --yes --no-install-recommends llvm-13 && \
    apt remove --yes gpg-agent lsb-release software-properties-common && apt clean autoclean && apt autoremove --yes && \
    cd /

# Wire up clang resource directory. The REPL version in 0.0.5 was forked from
# mainline LLVM at db9c2d775130a110ada89decff7002c64cdd3364. While the Clang
# major version was 14 already, the commit is actually much closer to release
# 13.0.0 than it is to 14.0.0.
RUN mkdir -p /usr/lib/clang && \
    ln -s /usr/lib/ez-clang/$VERSION/packages/toolchain-clang-arm/lib/clang/13.0.0/include /usr/lib/clang/14.0.0

# Download release materials
RUN wget -q --show-progress -O /tmp/ez-clang.tar.gz \
    https://github.com/echtzeit-dev/ez-clang/archive/refs/tags/v$VERSION.tar.gz && \
    tar zxf /tmp/ez-clang.tar.gz -C /tmp && \
    cd /tmp/ez-clang-$VERSION/release/$VERSION && \
    mv share /usr/lib/ez-clang/$VERSION/. && \
    mv docker /usr/lib/ez-clang/$VERSION/. && \
    cd / && rm -rf /tmp/*

# Download the actual release binary
RUN wget -q --show-progress -O /usr/bin/ez-clang-$VERSION \
    https://github.com/echtzeit-dev/ez-clang/releases/download/v0.0.5/ez-clang-0.0.5-x86_64-pc-linux-gnu && \
    chmod +x /usr/bin/ez-clang-$VERSION

# The startup script has no access to $VERSION
RUN ln -s /usr/bin/ez-clang-$VERSION /usr/bin/ez-clang && \
    ln -s /usr/lib/ez-clang/$VERSION/docker/startup.sh /usr/bin/ez-clang-startup.sh && \
    ln -s /usr/lib/ez-clang/$VERSION/docker/ez_clang_history $HOME/.ez_clang_history

ENTRYPOINT ["/usr/bin/ez-clang-startup.sh"]
