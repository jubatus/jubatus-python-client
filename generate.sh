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
  python -c "print ''.join(map(str.capitalize, '${1}'.split('_')))"
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
  IDL_HASH=`git log -1 --format=%H -- ${IDL}`
  IDL_VER=`git describe ${IDL_HASH}`
  jenerator -l python "${IDL}" -o "${CLIENT_DIR}/jubatus" --idl-version ${IDL_VER}
done
popd

cat << _EOF_ > "${CLIENT_DIR}/jubatus/__init__.py"
__all__ = [$(
  for SERVICE in ${SERVICE_LIST[@]}; do
    echo -n '"'${SERVICE}'", ';
  done
)]

$(for SERVICE in ${SERVICE_LIST[@]}; do
  echo "from jubatus.${SERVICE}.client import $(capitalize "${SERVICE}")";
done)
_EOF_

rm -rf "${JUBATUS_DIR}"
