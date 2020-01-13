import csv
import time
import pathlib


# checks if two lists have same Nodes
def are_equal(list1, list2):

	if len(list1) != len(list2):
		return False

	list1_sorted = sorted(list1,key=lambda l:(l.coords[0], l.coords[1]))
	list2_sorted = sorted(list2,key=lambda l:(l.coords[0], l.coords[1]))

	for i in range(0, len(list1_sorted)):
		if list1_sorted[i].coords != list2_sorted[i].coords:
			print(list1_sorted[i].coords)
			print(list2_sorted[i].coords)
			return False
	
	return True

# brute force range search for checking answer
def bruteforce_range_search(root, range_coords):
	nodes_list = []
	if root:
		if is_in_range(root.coords, range_coords):
			nodes_list.append(root)
		
		
		nodes_list += bruteforce_range_search(root.left, range_coords)
		nodes_list += bruteforce_range_search(root.right, range_coords)
	
	return nodes_list

def pre_order(root, string=""):
    if root:
        print(string + str(root.coords) + "|data:" + str(root.data))

        pre_order(root.left, "\t" + string + "-left-")
        pre_order(root.right, "\t" + string + "-right-")

def print_nodes(nodes_list):
	for node in nodes_list:
		print(str(node.coords) + "\t|\tdata:" + str(node.data))

def print_options():
    print("\n//////////// MENU ////////////")
    print("0 - Print Tree")
    print("1 - Search Node")
    print("2 - Range Search")
    print("3 - Insert Node")
    print("4 - Delete Node")
    print("5 - Update Node")
    print("-1 - Exit Program")
    print("//////////////////////////////")


# File to import selection

choice = int(input("0 - KD\n1 - Range\n2 - Range with Fractional Cascading\n-> "))

if choice == 0:
    from kd_tree.kd_tree import *
elif choice == 1:
    from range_tree.range_tree import *
else:
    from range_tree.range_tree_fractional_cascading import *


filename = 'airports.csv'
fn = pathlib.Path(__file__).parent / 'datasets' / filename


my_nodes = []

with open(fn, mode='r', encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count > 0 and (row["type"] == "medium_airport" or row["type"] == "large_airport"):
            my_nodes.append(Node([float(row["latitude_deg"]), float(row["longitude_deg"])], row["name"]))
        line_count += 1
    print('Processed ' + str(line_count) + ' lines')


# Build Start
start = time.time()

if choice == 0:
    my_sorted_nodes = []
    for i in range(0, DIMENSIONS):
        my_sorted_nodes.append(sorted(my_nodes, key=lambda l:l.coords[i]))

    my_root = create_tree(my_sorted_nodes)

else:
    x_sorted_nodes = sorted(my_nodes, key=lambda l:(l.coords[0], l.coords[1]))
    my_root, _ = create_tree(x_sorted_nodes)

end = time.time()
print("Build Time: " + str(end - start))
# Build End



print_options()
choice = int(input())

while choice != -1:
    print('-----------------------')
    start = time.time()

    if choice == 0:
        pre_order(my_root)
    elif choice == 1:
        coords = []
        for d in range(DIMENSIONS):
            print("Give coordinate for dimension " + str(d))
            coords.append(float(input()))
        res_list = search(my_root, coords)
        if len(res_list) == 0:
            print("Not Found!")
        else:
            print_nodes(res_list)
    elif choice == 2:
        my_range = []
        for d in range(DIMENSIONS):
            dth_range = []
            print("Give left coordinate for dimension " + str(d))
            dth_range.append(float(input()))
            print("Give right coordinate for dimension " + str(d))
            dth_range.append(float(input()))
            my_range.append(dth_range)
        res_list = range_search(my_root, my_range)
        if len(res_list) == 0:
            print("Not Found!")
        else:
            print_nodes(res_list)
    elif choice == 3:
        coords = []
        for d in range(DIMENSIONS):
            print("Give coordinate for dimension " + str(d))
            coords.append(float(input()))
        data = input("Give your node's data: ")
        my_root = insert(my_root, Node(coords, data))
    elif choice == 4:
        coords = []
        for d in range(DIMENSIONS):
            print("Give coordinate for dimension " + str(d))
            coords.append(float(input()))
        my_root = delete(my_root, coords)
    elif choice == 5:
        my_root = update(my_root)
        
    end = time.time()
    print('-----------------------')
    print("Action Time: " + str(end - start))
    print('-----------------------')
    print_options()
    choice = int(input())


# brute_list = bruteforce_range_search(my_root, my_range)
# if are_equal(brute_list, res_list):
#     print("Lists are equal!")
# else:
#     print("Lists are NOT equal!")