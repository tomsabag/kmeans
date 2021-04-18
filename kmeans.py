import sys
test_input = input()
file = open(test_input, "r")


class Cluster:
    def __init__(self, centroid):
        self.centroid = centroid
        self.sum_vector = [0 for item in centroid.lst]
        self.size = 0


class Centroid:
    def __init__(self, lst):
        self.lst = lst
        self.size = len(lst)


def process_data(data):
    for word in data:
        i = data.index(word)
        word = float(word.replace("\n", ""))
        data[i] = float(word)
    return data


def initialize_clusters(file):
    k = int(sys.argv[1])
    clusters = []
    for i in range(k):
        data = file.readline()
        data = data.split(",")
        data = process_data(data)
        centroid = Centroid(data)
        clusters.append(Cluster(centroid))
    return clusters


def sum_lists(lst1, lst2):
    return [lst1[i] + lst2[i] for i in range(len(lst1))]


def k_mean(file, max_iter=200):
    file_length = get_file_length(file)
    file = open(test_input, "r")
    clusters = initialize_clusters(file)
    iterations = 0
    centroids_changed = 0
    first = True
    while iterations < max_iter and (centroids_changed > 0 or first):
        file = open(test_input, "r")
        first = False
        iterations += 1
        for i in range(file_length):
            data = file.readline()
            if data == "":
                break
            data = data.split(",")
            data = process_data(data)
            min_distance = 2147483648
            m = -1
            for j in range(len(clusters)):
                distance = euclidean(data, clusters[j].centroid)
                if distance < min_distance:
                    min_distance = distance
                    m = j
            clusters[m].sum_vector = sum_lists(clusters[m].sum_vector, data)
            clusters[m].size += 1
            #print("m=",m, "sumvector=", clusters[m].sum_vector)
        #print("sizes=", [cluster.size for cluster in clusters])
        #print(iterations)
        centroids_changed = update_centroids(clusters)
    return clusters


def update_centroids(clusters):
    counter = 0
    for cluster in clusters:
        prev_centroid = cluster.centroid

        for i in range(len(cluster.centroid.lst)):
            if cluster.size != 0:
                cluster.centroid.lst[i] = cluster.sum_vector[i] / cluster.size
        cluster.sum_vector = [0 for item in cluster.sum_vector]
        cluster.size = 0
        counter += 1 if prev_centroid == cluster.centroid else 0
    return counter


def euclidean(dp, centroid):
    distance = 0
    for i in range(centroid.size):
        distance += (centroid.lst[i] - dp[i]) ** 2
    return distance


def get_file_length(file):
    length = 0
    while True:
        my_str = file.readline()
        if my_str == "":
            break
        length += 1
    return length


iterations = 200
if len(sys.argv) == 3:
    iterations = int(sys.argv[-1])
clusters = k_mean(file, iterations)
for cluster in clusters:
    for i in range(len(cluster.centroid.lst)):
        cluster.centroid.lst[i] = round(cluster.centroid.lst[i], 4)

for cluster in clusters:
    print(cluster.centroid.lst)


