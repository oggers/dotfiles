#!/bin/bash

infocmp > /tmp/terminfo
scp /tmp/terminfo $1:/tmp
ssh $1 "tic -x /tmp/terminfo; rm /tmp/terminfo"
rm /tmp/terminfo
