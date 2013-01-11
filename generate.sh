#!/bin/bash -ue

JUBATUS_DIR="jubatus-generate"
JUBATUS_BRANCH="master"
CLIENT_DIR="$(dirname "${0}")"

[ $# -eq 0 ] || JUBATUS_BRANCH="${1}"

rm -rf "${JUBATUS_DIR}"
git clone https://github.com/jubatus/jubatus.git "${JUBATUS_DIR}"
pushd "${JUBATUS_DIR}"
git checkout "${JUBATUS_BRANCH}"
popd

# Python
rm -rf "${CLIENT_DIR}/jubatus"
for IDL in "${JUBATUS_DIR}/src/server"/*.idl; do
  mpidl python "${IDL}" -o "${CLIENT_DIR}/jubatus"
done

find "${CLIENT_DIR}/jubatus" -name "server.tmpl.py" -delete
touch "${CLIENT_DIR}/jubatus/__init__.py"

rm -rf "${JUBATUS_DIR}"
