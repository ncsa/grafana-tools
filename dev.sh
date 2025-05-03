DEBUG=1

[[ "$DEBUG" -eq 1 ]] && set -x

set -x

DOCKER=/usr/bin/docker
PATH=.
IMGNAME=grafana_api
TAG=dev

${DOCKER} buildx build \
  -f ${PATH}/Dockerfile \
  -t "${IMGNAME}:${TAG}" \
  ${PATH}

# -e JIRA_SERVER=jira.ncsa.illinois.edu \
# -e JIRA_PROJECT=SVCPLAN \
${DOCKER} run -it \
--mount type=bind,src=$HOME,dst=/home \
--entrypoint "/bin/bash" \
${IMGNAME}:${TAG}
