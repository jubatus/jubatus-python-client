#!/bin/bash -ue

BASE_DIR="$(cd $(dirname $0);pwd)"
WORK_DIR="${BASE_DIR}/work"

JUBATUS_BRANCH="master"
[ $# -eq 0 ] || JUBATUS_BRANCH="${1}"

clean() {
  rm -rf "${WORK_DIR}"
}

generate() {
  OUTPUT_DIR="${1}"; shift
  REPOSITORY="${1}"; shift
  BRANCH="${1}"; shift

  CLONE_DIR="${WORK_DIR}/clone"
  rm -rf "${CLONE_DIR}"
  git clone "${REPOSITORY}" "${CLONE_DIR}"
  pushd "${CLONE_DIR}/msgpack-idl"
  git checkout "${BRANCH}"
  cabal configure
  cabal build
  popd

  PATH="${CLONE_DIR}/msgpack-idl/dist/build/mpidl:${PATH}" "${BASE_DIR}/../generate.sh" "${JUBATUS_BRANCH}"
  mkdir -p "${OUTPUT_DIR}"
  mv "${BASE_DIR}/../jubatus" "${OUTPUT_DIR}/jubatus"
}

clean

rm -f "${BASE_DIR}"/*.patch

MPIDL_UPSTREAM_DIR="${WORK_DIR}/origin"
MPIDL_JUBATUS_DIR="${WORK_DIR}/for_jubatus"

generate "${MPIDL_UPSTREAM_DIR}" "https://github.com/msgpack/msgpack-haskell.git" "master"
generate "${MPIDL_JUBATUS_DIR}" "https://github.com/rimms/msgpack-haskell.git" "for_jubatus"

pushd "${WORK_DIR}"
# `diff` exits with 1 when the difference is detected
diff -uNr "${MPIDL_UPSTREAM_DIR#${WORK_DIR}/}" "${MPIDL_JUBATUS_DIR#${WORK_DIR}/}" > "${BASE_DIR}/msgpack-idl.patch" || [ $? = 1 ]
popd

clean
