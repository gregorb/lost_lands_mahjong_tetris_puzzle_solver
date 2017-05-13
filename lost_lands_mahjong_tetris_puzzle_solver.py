#!/usr/bin/env python3


# 8x8 grid is represented as 64x1 array
# using brute force to solve the puzzle

def print_grid(grid):
	for line in range(8):
		print(grid[line * 8 : (line + 1) * 8])
	print()

def print_grid_exploded(grid):
	# zoom: x(8,4)
	zX = 6
	zY = 4
	out = '.' * ((8*zX) * (8*zY))
	for y in range(8):
		for x in range(8):
			for yy in range(zY):
				for xx in range(zX):
					if (
						((yy == 0) and ((y == 0) or (grid[x + 8*(y-1)] != grid[x + 8*y])))
						or
						((xx == 0) and ((x == 0) or (grid[(x-1) + 8*y] != grid[x + 8*y])))
						or
						((xx == 0) and (yy == 0) and (grid[(x-1) + 8*(y-1)] != grid[x + 8*y]))
					):
						out = str_assign(out, x*zX+xx + (8*zX)*(y*zY+yy), ' ')
					else:
						out = str_assign(out, x*zX+xx + (8*zX)*(y*zY+yy), grid[x + 8*y])
	for line in range(1, 8*4):  #1st line is always blank, we can skip it
		print(out[line * 8*zX : (line + 1) * 8*zX])
	print()

def str_assign(str, pos, char):
	return str[:pos] + char + str[pos + 1:]


def print_blocks(blocks):
	blankLine = ' ' * len(blocks) * 5;
	outLines = [blankLine, blankLine, blankLine]
	xPosition = 0
	for block in blocks:
		for dot in block:
			outLines[dot[1]] = str_assign(outLines[dot[1]], xPosition + dot[0], '#')
		xPosition += 5
	for y in range(3):
		print(outLines[y])
	print()


def new_puzzle(puzzle_name):
	if puzzle_name == 'tie_fighter':
		return (
			'........' +
			'....###.' +
			'......#.' +
			'....#.#.' +
			'.#.#....' +
			'.#......' +
			'.###....' +
			'........',
			[
				new_block('L'),     # L-shape
				new_block('L90'),   # L-shape rotated 90 deg. clockwise
				new_block('L180'),  # L-shape rotated 180 deg.
				new_block('L180'),  # L-shape rotated 90 deg. counter-clockwise
				new_block('plus'),  # "plus"-shape
				new_block('T'),     # T-shape
				new_block('L270'),
				new_block('J'),     # J-shape
				new_block('J180'),
				new_block('Qtr'),   # corner, top right
				new_block('Qtr'),
				new_block('Qbl'),
				new_block('1x1'),   # 1x1 block
				new_block('1x1'),
				new_block('S90')    # S-shape rotated 90 deg. clockwise
			] )
	elif puzzle_name == 'empty':
		return ('.' * 64, []);
	else:
		assert False, 'invalid block name: ' + block_name


def new_block(block_name):
	if block_name == '1x1':
		return [[0,0]]
	elif block_name == 'L':
		return [[0,0], [0,1], [0,2], [1,2]]
	elif block_name == 'L90':
		return [[0,0], [1,0], [2,0], [0,1]]
	elif block_name == 'L180':
		return [[0,0], [1,0], [1,1], [1,2]]
	elif block_name == 'L270':
		return [[2,0], [0,1], [1,1], [2,1]]
	elif block_name == 'T':
		return [[0,0], [1,0], [2,0], [1,1]]
	elif block_name == 'T90':
		assert False, 'block not yet implemented: ' + block_name
	elif block_name == 'T180':
		assert False, 'block not yet implemented: ' + block_name
	elif block_name == 'T270':
		assert False, 'block not yet implemented: ' + block_name
	elif block_name == 'J':
		return [[1,0], [1,1], [0,2], [1,2]]
	elif block_name == 'J90':
		assert False, 'block not yet implemented: ' + block_name
	elif block_name == 'J180':
		return [[0,0], [1,0], [0,1], [0,2]]
	elif block_name == 'J270':
		assert False, 'block not yet implemented: ' + block_name
	elif block_name == 'Qtr':
		return [[0,0], [1,0], [1,1]]
	elif block_name == 'Qtl':
		assert False, 'block not yet implemented: ' + block_name
	elif block_name == 'Qbl':
		return [[0,0], [0,1], [1,1]]
	elif block_name == 'Qbr':
		assert False, 'block not yet implemented: ' + block_name
	elif block_name == 'S':
		assert False, 'block not yet implemented: ' + block_name
	elif block_name == 'S90':
		return [[0,0], [0,1], [1,1], [1,2]]
	elif block_name == 'Z':
		assert False, 'block not yet implemented: ' + block_name
	elif block_name == 'Z90':
		assert False, 'block not yet implemented: ' + block_name
	elif block_name == 'plus':
		return [[1,0], [0,1], [1,1], [2,1], [1,2]]
	else:
		assert False, 'invalid block name: ' + block_name


def solver_place_block(grid, block, x, y, block_id):
	can_place = True
	for bit in block:
		xx = x + bit[0]
		yy = y + bit[1]
		if (xx >= 8) or (yy >= 8):
			can_place = False
			break
		if grid[xx + 8 * yy] != '.':
			can_place = False
			break
		grid = str_assign(grid, xx + 8 * yy, block_id)
	return (can_place, grid)


def solve_puzzle(grid, blocks, first_block_id = 'a'):
	if len(blocks) == 0:
		return (True, grid)

	# place first block, try solving for the rest
	for y in range(8):
		for x in range(8):
			(can_place, new_grid) = solver_place_block(grid, blocks[0], x, y, first_block_id)
			if can_place:
				#print_grid(new_grid)
				(solved, solved_grid) = solve_puzzle(new_grid, blocks[1:], chr(ord(first_block_id) + 1))
				if solved:
					return (True, solved_grid)

	# if we came this far, the puzzle is not solvable
	return (False, grid)


def main():
	print("Solving:")
	print()
	(grid, blocks) = new_puzzle('tie_fighter')
	#print_grid(grid)
	print_grid_exploded(grid)
	print("Blocks:")
	print()
	print_blocks(blocks)

	(solved, grid) = solve_puzzle(grid, blocks)

	print("SOLVED :-)" if solved else "NOT SOLVED :-(")
	print()
	print_grid_exploded(grid)


main()
