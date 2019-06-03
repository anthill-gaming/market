#!/usr/bin/env bash


# Setup postgres database
createuser -d anthill_log -U postgres
createdb -U anthill_log anthill_log
