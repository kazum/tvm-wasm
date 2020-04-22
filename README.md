# tvm-wasm: Build pure WebAssembly from DL model

This repository contains
- a script to compile a pre-trained model into a DL
library in the pure WebAssembly format (no need for the emscripten layer)
- example Rust codes to use the generated library (e.g. WASI, waSCC, ...).

## Install

- Clone repo

  ```
  git clone --recursive https://github.com/kazum/tvm-wasm
  ```

- Setup TVM

  - Build

    LLVM 9.0 or later is required.

    ```
    mkdir tvm/build
    cd tvm/build
    cmake -DUSE_LLVM=/usr/bin/llvm-config-9 ..
    make -j8
    cd -
    ```

  - Install Python packages

    ```
    pip install cython
    cd tvm/python; python setup.py install; cd -
    cd tvm/topi/python; python setup.py install; cd -
    pip install onnx
    ```

  See https://tvm.apache.org/docs/install/from_source.html for details.

- Setup Rust

  - Add wasm32 targets

    ```
    rustup target add wasm32-unknown-unknown
    rustup target add wasm32-wasi
    ```

  - Build a static library for tvm runtime.

    ```
    cd tvm/rust/runtime; cargo build --target wasm32-unknown-unknown --release; cd -
    ```


## Build model

- Build DL library in the WebAssembly format.

  - Download model

    ```
    wget https://s3.amazonaws.com/onnx-model-zoo/resnet/resnet50v1/resnet50v1.onnx
    ```

  - Compile

    ```
    AR=llvm-ar-9 python build_lib.py -O3 resnet50v1.onnx
    ```

## Example: WASI

- Run inference from command line

  - Build
    ```
    $ cd examples/wasi
    $ cargo build --release
    ```

  - Run inference
    ```
    $ wget -O cat.png https://github.com/dmlc/mxnet.js/blob/master/data/cat.png?raw=true
    $ wasmtime target/wasm32-wasi/release/tvm-wasi.wasm --dir . cat.png
    original image dimensions: (256, 256)
    resized image dimensions: (224, 224)
    input image belongs to the class `tabby, tabby cat`
    ```

## Example: waSCC

- Run HTTP inference server

  - Build an actor to handle inference request
    ```
    $ cd examples/tvm-serving
    $ make release
    ```

  - Build a host with the wascc-host library

    Follow the tutorial in https://wascc.dev/tutorials/first-actor/create_host/

  - Send a inference request
    ```
    $ curl -s -T cat.png localhost:8081
    "tabby, tabby cat"
    ```
