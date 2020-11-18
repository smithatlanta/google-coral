#!/usr/bin/python3 -u

import time
import argparse
import smbus
import os
import re
import threading
import signal
import traceback
from dataclasses import dataclass
from collections import deque

def bitExtract(number, anzahl, position): 
    return (((1 << anzahl) - 1) & (number >> (position))); 

def setBitAt(wert, position):
	return wert | (1<<position)
	
def tauscheBytes(wert):
	return int.from_bytes(wert.to_bytes(2,'big'),byteorder='little')
	
def read_word_data_swapped(bus,address,register):
	return tauscheBytes(bus.read_word_data(address,register))

def write_word_data_swapped(bus,address,register,data):
	bus.write_word_data(address,register,tauscheBytes(data))
	
	
def signal_handler(sig, frame):
	os._exit(0)
	
def init_Sensor(bus,address):
	config=read_word_data_swapped(bus,address,0x01)
	config=setBitAt(config,10) #auf kontinuierlich setzen
	write_word_data_swapped(bus,address,0x01,config)
	
		
def round_lux(lux):
	if args.round is not None:
		if args.round == 0:
			lux=int(round(lux,args.round))
		else:
			lux=round(lux,args.round)
	else:
		lux=round(lux,2) #to prevent floating point issues like Lux: 42.800000000000004 sensor output is generally only 2 decimal places
	return lux

def get_lux(bus,address):
	wert=read_word_data_swapped(bus,address,0x00)
	exponent= bitExtract(wert,4,12) 
	mantisse= bitExtract(wert,12,0)
	lsb_size = 0.01 * pow(2,exponent)
	lux=lsb_size * mantisse
	return lux
	

@dataclass
class Measurement:
	lux: float
	lux2: float = None
	timestamp: int = 0

