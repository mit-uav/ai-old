class PathPlanner(object):

    def __init__(self):
        super(PathPlanner, self).__init__()

    def step(self, world):
    	quad = []
    	roomba_target = []
    	roomba_avoid = []
    	output = {}
    	length = 200
    	width = 200
    	tick = 1

    	for key in world:
    		if key == 'quad':
    			quad.append(world[key])
    		else if key == "roomba" and world[key][spike]:
    			roomba_avoid.append(world[key])
    		else:
    			roomba_target.append(world[key])

    	difference = roomba_target['position'].sub(quad['position'])
    	t = path.magnitude()/quad['maxvelocity'] 
    	bayesian_t = t * quad['maxvelocity']/roomba_target['velocity'].magnitude()

    	path_o = roomba_target['position'] + roomba_target['velocity'].scale(bayesian_t / 2)
    	path = roomba_target['position'] + roomba_target['velocity'].scale(bayesian_t)

    	output['move_%d' % tick] = (path[0], path[1], quad['position'][2])
    	tick += 1
    	output['descend_%d' % tick] = path
    	tick += 1

    	if path[1] < length/2:
    		if roomba_target['velocity'].quadrant() == 1:
    			output['move_%d' % tick] = path.add(roomba_target['velocity'].scale(-1))
    			tick += 1
    			path.add(roomba_target['velocity'].scale(-1))
    			output['ascend_%d' % tick] = (path[0], path[1], 0.7)
    			tick += 1
    			output['descend_%d' % tick] = path.add(roomba_target['velocity'].scale(0.3))
    			tick += 1
    		else if roomba_target['velocity'].quadrant() == 3:
    			output['descend_%d' % (tick - 1)] = path_o
    	else:
    		if roomba_target['velocity'].quadrant() == 1:
    			output['descend_%d' % (tick - 1)] = path_o
    		else if roomba_target['velocity'].quadrant() == 3:
    			output['move_%d' % tick] = path.add(roomba_target['velocity'].scale(-1))
    			tick += 1
    			path.add(roomba_target['velocity'].scale(-1))
    			output['ascend_%d' % tick] = (path[0], path[1], 0.7)
    			tick += 1
    			output['descend_%d' % tick] = path.add(roomba_target['velocity'].scale(0.3))
    			tick += 1
        return output





