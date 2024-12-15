world_map = [
	'                                                                  ',
	'                                                                  ',
	'                                                                  ',
	' X   X  X    xXXXXXXXXXs                   XX   X                 ',
	' X XXX      X         XX                XXXX    XX                ',
	'  L       c                                 XXXXX                 ',
	'          X       c            t   X                            G ',
	'     Xc XXXXXX  XXXXs    XXXXXXXXXXX  XX                       XXX',
	'XP t     X XX X  X XXX      X XX  XX  XXX  XXXXXXXXs  XXXXXX      ',
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