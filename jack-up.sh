#!/usr/bin/env bash
pulseaudio --kill
jack_control start
jack_control exit
pulseaudio --start
#pasuspender qjackctl