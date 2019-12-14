DIMENSIONS = 3


class Node:
    def __init__(self, coords = [DIMENSIONS]):
        self.left = None
        self.right = None
        self.coords = coords


#insert node
def insert(root, node, depth=0):
    if root is None:
        return node
    else:
        axis = depth % DIMENSIONS # axis = 0 or 1 or 2
        if node.coords[axis] <= root.coords[axis]: #= x_nodes[mid][0]
            root.left = insert(root.left, node, depth+1)
        else:
            root.right = insert(root.right, node, depth+1)
        return root


def print_nodes(nodes):
    for node in nodes:
        print(node.coords)


# wrapper
def create_tree(nodes):
    return create(None, nodes, 0)


#create kd tree
def create(root, nodes, depth):

    axis = depth % DIMENSIONS

    if len(nodes[axis]) == 0:
        return None

    if len(nodes[axis]) == 1:
        return nodes[axis][0]

    mid = int(len(nodes[axis])/2)

    middle_node = nodes[axis][mid]

    left = []
    right = []


    for i in range (0,DIMENSIONS):
        l = []
        r = []
        for node in nodes[i]:
            if node.coords[axis] < middle_node.coords[axis]:
                l.append(node)
            elif node.coords[axis] > middle_node.coords[axis]:
                r.append(node)

        left.append(l)
        right.append(r)


    middle_node.left = create(root, left, depth+1)
    middle_node.right = create(root, right, depth+1)

    return middle_node


def pre_order(root, string):
    if root:
        print(string + str(root.coords))
        pre_order(root.left, string + "-left-")
        pre_order(root.right, string + "-right-")


#search node
def search(root, coords = [DIMENSIONS]):
	depth = 0
	while root and root.coords != coords:
		axis = depth % DIMENSIONS # axis = 0 or 1
		if coords[axis] <= root.coords[axis]:
			root = root.left
			print("left")
		else:
			root = root.right
			print("right")
		depth = depth + 1

	if root:
		print("Found!")
		return root.coords
	else:
		print("Not Found!")
		return None


def rangesearch(root, bounds, depth=0):
	if root is None:
		return

	axis = depth % DIMENSIONS # axis = 0 or 1


	if bounds[axis][1] < root.coords[axis]:
    	# proon rightchild
		rangesearch(root.left, bounds, depth+1)

	elif bounds[axis][0] > root.coords[axis]:
    	# proon leftchild
		rangesearch(root.right, bounds, depth+1)

	elif bounds[axis][0] <= root.coords[axis] and root.coords[axis] <= bounds[axis][1]:
		# inside bounds
		flag = 0
		for axis in range (0, DIMENSIONS):
			if bounds[axis][0] > root.coords[axis] or root.coords[axis] > bounds[axis][1]:
				flag = 1
				break
		if flag == 0:
			print(str(root.coords) + " is in range "+str(bounds))

		rangesearch(root.left, bounds, depth+1)
		rangesearch(root.right, bounds, depth+1)


# find node to replace
def findMinimum(root, depth, target_axis):

    if root is None:
        return None

    axis = depth % DIMENSIONS  # axis = 0 or 1


    if axis == target_axis:
        left = findMinimum(root.left, depth+1, target_axis)
        if left is not None and left.coords[axis] < root.coords[axis]:
            return left
        else:
            return root
    else:
        left = findMinimum(root.left, depth+1, target_axis)
        right = findMinimum(root.right, depth+1, target_axis)

        if left is not None and left.coords[axis] < root.coords[axis] and (right is None or left.coords[axis] < right.coords[axis]):
            return left
        elif right is not None and right.coords[axis] < root.coords[axis] and (left is None or right.coords[axis] < left.coords[axis]):
            return right
        else:
            return root


def findMaximum(root, depth, target_axis):

    if root is None:
        return None

    axis = depth % DIMENSIONS  # axis = 0 or 1


    if axis == target_axis:
        right = findMaximum(root.right, depth+1, target_axis)
        if right is not None and right.coords[target_axis] > root.coords[target_axis]:
            return right
        else:
            return root
    else:
        left = findMaximum(root.left, depth+1, target_axis)
        right = findMaximum(root.right, depth+1, target_axis)
        if left is not None and left.coords[target_axis] > root.coords[target_axis] and (right is None or left.coords[target_axis] > right.coords[target_axis]):
            return left
        elif right is not None and right.coords[target_axis] > root.coords[target_axis] and (left is None or right.coords[target_axis] > left.coords[target_axis]):
            return right
        else:
            return root


# deleteNode
def delete(root, coords, depth=0):
    if root is None:
        return None

    axis = depth % DIMENSIONS  # axis = 0 or 1
    if root.coords == coords:
        if root.left is None and root.right is None:  # leaf
            del root
            return None
        elif root.left is None:
            temp = findMinimum(root.right, depth+1, depth % DIMENSIONS)
            delete(root, temp.coords, depth)
            root.coords = temp.coords
        else:
            temp = findMaximum(root.left, depth+1, depth % DIMENSIONS)
            delete(root, temp.coords, depth)
            root.coords = temp.coords

    elif coords[axis] <= root.coords[axis]:
        root.left = delete(root.left, coords, depth + 1)
    else:  # coords[axis] > root.coords[axis]
        root.right = delete(root.right, coords, depth + 1)

    return root

	#main





my_nodes = [
    Node([2,5,7]),
    Node([3,4,8]),
    Node([6,8,1]),
    Node([1,9,3]),
    Node([5,7,4])
]    #3d points

my_sorted_nodes = []
for i in range(0, DIMENSIONS):
    my_sorted_nodes.append(sorted(my_nodes,key=lambda l:l.coords[i]))

for i in range(0,DIMENSIONS):            #check if nodes are sorted ok
    for j in range(0,len(my_nodes)):
        print(my_sorted_nodes[i][j].coords)
    print("----------")



my_root = create_tree(my_sorted_nodes)


insert(my_root, Node([1.5, 10,6])) #3d
insert(my_root, Node([1.7, 11,2]))#3d

rangesearch(my_root,[[0,10],[0,8],[0,1]])
print("=============================================\n")

pre_order(my_root, "")

print("=============================================\n")

delete(my_root, [3, 4, 8])

print("=============================================\n")

pre_order(my_root, "")

	