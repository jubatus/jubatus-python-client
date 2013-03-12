#!/bin/bash -ue

JUBATUS_DIR="jubatus-generate"
JUBATUS_BRANCH="master"
CLIENT_DIR="$(cd $(dirname ${0}) && echo ${PWD})"

[ $# -eq 0 ] || JUBATUS_BRANCH="${1}"

rm -rf "${JUBATUS_DIR}"
git clone https://github.com/jubatus/jubatus.git "${JUBATUS_DIR}"
pushd "${JUBATUS_DIR}"
git checkout "${JUBATUS_BRANCH}"
popd

# Python

capitalize() {
  echo "$(echo ${1:0:1} | tr 'a-z' 'A-Z')${1:1}"
}

rm -rf "${CLIENT_DIR}/jubatus"
SERVICE_LIST=()
pushd "${JUBATUS_DIR}/src/server"
for IDL in *.idl; do
  NAMESPACE="$(basename "${IDL}" ".idl")"
  SERVICE_LIST[${#SERVICE_LIST[@]}]="${NAMESPACE}"
  mpidl python "${IDL}" -o "${CLIENT_DIR}/jubatus"
done
popd

find "${CLIENT_DIR}/jubatus" -name "server.tmpl.py" -delete


for PATCH in $(find "${CLIENT_DIR}/patch" -maxdepth 1 -name "*.patch"); do
  patch --no-backup-if-mismatch -p1 < "${PATCH}"
done

cat << _EOF_ > "${CLIENT_DIR}/jubatus/__init__.py"
__all__ = [$(
  for SERVICE in ${SERVICE_LIST[@]}; do
    echo -n '"'${SERVICE}'", ';
  done
)]

$(for SERVICE in ${SERVICE_LIST[@]}; do
  echo "from jubatus.${SERVICE}.client import ${SERVICE} as $(capitalize "${SERVICE}")";
done)
_EOF_

rm -rf "${JUBATUS_DIR}"
