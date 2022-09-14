# Additions by me

https://www.mouser.com/datasheet/2/963/Google_03292019_G650-04023-01-1549729.pdf

I added 4 python files to help me get the missing humidity and the light.

- temperature_humidity_hdc2080.py - This just gets the temperature and the humidity from the hdc2080 chip - address - 0x40
- pressure_bmp20.py - This just gets the pressure from the bmp280 chip - address - 0x76 \* - this would work inconsistantly sometimes giving me an in use issue.
- my_enviro_board.py - this was basically derived from board.py with tweaked overrides to use the "from coral.enviro.board import EnviroBoard" pip module
- my_enviro_demo.py - this was basically derived from enviro_demo.py but tweaked to use my_enviro_board.py and write to an influxdb.
