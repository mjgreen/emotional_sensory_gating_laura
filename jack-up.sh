#!/usr/bin/env bash
pulseaudio --kill
sudo jack_control start
sudo jack_control status
sudo jack_control exit
pulseaudio --start
pasuspender qjackctl
