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

from wasmtime import Store, Module, FuncType, MemoryType, TableType, GlobalType

wasm_file = '../../libtvmwasm.wasm'

store = Store()
module = Module.from_file(store, wasm_file)

for i, e in enumerate(module.exports):
    if isinstance(e.type, FuncType):
        print("{}: {}, params={}, results={}".format(i, e.name, e.type.params, e.type.results))
    elif isinstance(e.type, MemoryType):
        print("{}: {}, limits=[{}, {}]".format(i, e.name, e.type.limits.min, e.type.limits.max))
    elif isinstance(e.type, TableType):
        print("{}: {}".format(i, e.name))
    elif isinstance(e.type, GlobalType):
        print("{}: {}, content={}, mutable={}".format(i, e.name, e.type.content, e.type.mutable))
