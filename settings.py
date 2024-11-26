world_map = [
	'                                                                  ',
	'                                                                  ',
	'                t  t                                              ',
	'        X    xXXXXXXXXXs                   XX   X                 ',
	' X   X      X         XX                XXXX tt XX                ',
	' XLXXX    c                                 XXXXX                 ',
	'          Xt    t c         t  t   X                            G ',
	'      c XXXXXX  XXXXs    XXXXXXXXXXX  XX              tt t     XXX',
	' P    X  X XX X  X XXXt     X XX  XX  XXX  XXXXXXXXs  XXXXXX      ',
	'XXXXXXX  X  X X  X  XXXXXXXXX XX  XX  XXX  XX XX XXXXXXX  X       ',
]

tile_size = 50
WIDTH, HEIGHT = 1000, len(world_map) * tile_size

"""
c - coin
g - power up (grzyb)
L - lucky block
G - Goomba
k - koopa
"""