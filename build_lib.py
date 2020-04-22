#!/usr/bin/env python3
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import argparse
import subprocess
import os
from tvm import relay
import onnx

def build_lib(model_file, opt_level):
    """Compiles the pre-trained model with TVM"""

    onnx_model = onnx.load(model_file)
    shape_dict = {}
    for input in onnx_model.graph.input:
        shape_dict[input.name] = \
          [dim.dim_value for dim in input.type.tensor_type.shape.dim]
    net, params = relay.frontend.from_onnx(onnx_model, shape_dict)
    target = 'llvm -target=wasm32-unknown-unknown --system-lib'

    # compile the model
    with relay.build_config(opt_level=opt_level):
        graph, lib, params = relay.build_module.build(net, target, params=params)

    # save the model artifacts
    lib.save('tvmwasm.o')
    lib.export_library('libtvmwasm.wasm', cc="/usr/lib/llvm-9/bin/clang++",
                           options=[
                               "--target=wasm32-wasm",
                               "-Wl,--no-entry",
                               "-Wl,--export-dynamic",
                               "tvm/rust/target/wasm32-unknown-unknown/release/libtvm_runtime.a",
                               "-nostdlib"
                           ])
    ar = os.environ.get("AR", "ar")
    cmds = [ar, 'rcs', 'libtvmwasm.a', 'tvmwasm.o']
    subprocess.run(cmds)

    with open("tvmwasm.json", "w") as fo:
        fo.write(graph)

    with open("tvmwasm.params", "wb") as fo:
        params_bytes = relay.save_param_dict(params)
        fo.write(params_bytes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resnet build example')
    aa = parser.add_argument
    aa('model_file', type=str,
           help='model file')
    aa('-O', '--opt-level', type=int, default=0,
           help='level of optimization. 0 is unoptimized and 3 is the highest level')
    args = parser.parse_args()

    build_lib(args.model_file, args.opt_level)
