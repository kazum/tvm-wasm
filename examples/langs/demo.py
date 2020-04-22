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

from wasmtime import Store, Module

wasm_file = '../../libtvmwasm.wasm'

store = Store()
module = Module.from_file(store, wasm_file)

for i, e in enumerate(module.exports()):
    if e.type().func_type():
        t = e.type().func_type()
        print("{}: {}, params={}, results={}".format(i, e.name(), t.params(), t.results()))
    elif e.type().memory_type():
        t = e.type().memory_type()
        print("{}: {}, limits=[{}, {}]".format(i, e.name(), t.limits().min, t.limits().max))
    elif e.type().table_type():
        t = e.type().table_type()
        print("{}: {}".format(i, e.name())
    elif e.type().global_type():
        t = e.type().global_type()
        print("{}: {}, content={}, mutable={}".format(i, e.name(), t.content(), t.mutable()))
