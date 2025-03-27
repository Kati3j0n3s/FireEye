import Adafruit_BMP.BMP085 as BMP085
import adafruit_gps
import board
import busio
import cv2 as cv
from datetime import datetime
import logging
import numpy as np
import os
import RPi.GPIO as GPIO
import serial
import sqlite3
import time
import traceback