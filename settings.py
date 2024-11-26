world_map = [
	'                                                                  ',
	'                                                                  ',
	'                t  t                                              ',
	' X   X  X    xXXXXXXXXXs                   XX   X                 ',
	' XLXXX      X         XX                XXXX tt XX                ',
	'          c                                 XXXXX                 ',
	'        o Xt    t c         t  t   X                            G ',
	'      c XXXXXX  XXXXs    XXXXXXXXXXX  XX              tt t     XXX',
	'XP  k    X XX X  X XXXt     X XX  XX  XXX  XXXXXXXXs  XXXXXX      ',
	'XXXXXXXXXX  X X  X  XXXXXXXXX XX  XX  XXX  XX XX XXXXXXX  X       ',
]

tile_size = 50
WIDTH, HEIGHT = 1000, len(world_map) * tile_size

"""
c - coin
g - power up (grzyb)
L - lucky block
o - Goomba
k - koopa
"""