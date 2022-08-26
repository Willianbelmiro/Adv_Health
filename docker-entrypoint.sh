#!/bin/bash

exec gunicorn -w 4 'website:create_app()'