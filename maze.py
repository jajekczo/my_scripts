import random

class Cell:
    def __init__(self, x, y):
        self.walls = {"left": True, "right": True, "top": True, "bottom": True}
        self.isVisited = False
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y))

width = 4
height = 4

# maze init
maze = [[Cell(x, y) for y in range(height)] for x in range(width)]

stack = [(0,0)]


while len(stack) > 0:
    x, y = stack[-1]

    current = maze[x][y]
    current.isVisited = True

    available_neighbours = list()
    for i in [-1, 1]:
        if x + i >= 0 and x + i < width:
            if maze[x+i][y].isVisited == False:
                available_neighbours.append(maze[x+i][y])
                # print('appended neighbour: [' + str(x+i) + ', ' + str(y) +']')
        if y - i >= 0 and y - i < height:
            if maze[x][y-i].isVisited == False:
                available_neighbours.append(maze[x][y-i])
                # print('appended neighbour: [' + str(x) + ', ' + str(y-i) + ']')
    
    if len(available_neighbours) == 0:
        stack.pop()
        # print('going back')
    else:
        hop = random.choice(available_neighbours)
        # print('chosen: ' + str(hop))
        stack.append((hop.x, hop.y))
        if current.x - hop.x == 0:
            if current.y - hop.y == -1:
                current.walls['bottom'] = False
                hop.walls['top'] = False
            elif current.y - hop.y == 1:
                current.walls['top'] = False
                hop.walls['bottom'] = False
        if current.y - hop.y == 0:
            if current.x - hop.x == -1:
                current.walls['right'] = False
                hop.walls['left'] = False
            elif current.x - hop.x == 1:
                current.walls['left'] = False
                hop.walls['right'] = False


from PIL import Image

def make_maze(width, height, mazelist):

    size_x = width*3 + 1
    size_y = height*3 +1
    maze_png = Image.new('RGB', (size_x, size_y), color='white')

    pixels = maze_png.load()

    for x in range(width+1):
        for y in range(height+1):
            base_pix_pos = (x*3 + 1, y*3 +1)
            pixels[base_pix_pos[0]-1, base_pix_pos[1]-1] = (0, 0, 0)
            if x<width and y < height:
                if mazelist[x][y].walls['right'] == True:
                    pixels[base_pix_pos[0]+2, base_pix_pos[1]] = (0, 0, 0)
                    pixels[base_pix_pos[0]+2, base_pix_pos[1]+1] = (0, 0, 0)
                if mazelist[x][y].walls['bottom'] == True:
                    pixels[base_pix_pos[0], base_pix_pos[1]+2] = (0, 0, 0)
                    pixels[base_pix_pos[0]+1, base_pix_pos[1]+2] = (0, 0, 0)
                if mazelist[x][y].walls['left'] == True:
                    pixels[base_pix_pos[0]-1, base_pix_pos[1]] = (0, 0, 0)
                    pixels[base_pix_pos[0]-1, base_pix_pos[1]+1] = (0, 0, 0)
                if mazelist[x][y].walls['top'] == True:
                    pixels[base_pix_pos[0], base_pix_pos[1]-1] = (0, 0, 0)
                    pixels[base_pix_pos[0]+1, base_pix_pos[1]-1] = (0, 0, 0)
    maze_png.save("Maze_" + str(width) + "x" + str(height) + ".png", "PNG")

make_maze(width, height, maze)