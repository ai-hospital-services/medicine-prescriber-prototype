#!/bin/bash
###########################################################################
#Script Name  : entrypoint.sh
#Description  : Acts as an entrypoint for the api container image to act
#               as an api or a migration job
#Args         : $1 - runtime behavior indicator -
#               'api', 'migrate' or 'migrateThenApi'
#             : $* - remaining args are passed through to the 'api' command
###########################################################################

function api() {
    FLASK_DEBUG=${FLASK_DEBUG} python -m api.app "$@"
}
function migrate() {
    # TODO: migrate
    echo ""
}

mode=$1
shift
case ${mode} in
api)
    api "$@"
    ;;
migrate)
    migrate
    ;;
migrateThenApi)
    migrate && api "$@"
    ;;
*)
    echo "Usage api | migrate | migrateThenApi"
    exit 1
    ;;
esac
