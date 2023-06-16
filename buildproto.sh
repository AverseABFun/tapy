#!/bin/bash
protoc/bin/protoc -I=./txtadv_nightly/multiplayer --python_betterproto_out=./txtadv_nightly/multiplayer/taw_proto/ ./txtadv_nightly/multiplayer/taw.proto