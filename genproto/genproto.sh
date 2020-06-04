echo off
echo "Converting protocol buffers using betterproto"

echo You need: pip install "betterproto[compiler]"
echo   see  https://github.com/danielgtaylor/python-betterproto

protoc -I . --python_betterproto_out=..\synerex_harmovis\proto nodeapi\nodeapi.proto 
protoc -I . --python_betterproto_out=..\synerex_harmovis\proto api\synerex.proto 
protoc -I . --python_betterproto_out=..\synerex_harmovis\proto proto\geography\geography.proto
