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

for DIR in "${CLIENT_DIR}/jubatus/"*; do
  if [ "$(basename "${DIR}")" != "common" ]; then
    rm -rf $DIR
  fi
done
SERVICE_LIST=()
pushd "${JUBATUS_DIR}/jubatus/server/server"
for IDL in *.idl; do
  NAMESPACE="$(basename "${IDL}" ".idl")"
  SERVICE_LIST[${#SERVICE_LIST[@]}]="${NAMESPACE}"
  jenerator -l python "${IDL}" -o "${CLIENT_DIR}/jubatus"
done
popd

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
