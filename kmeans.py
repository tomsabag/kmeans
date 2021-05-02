import sys
test_input = "input_1.txt"
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


def read_file():
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    return lines


lines = read_file()


def process_data(data):
    for word in data:
        i = data.index(word)
        word = float(word.replace("\n", ""))
        data[i] = float(word)
    return data


def initialize_clusters(lines):
    k = int(sys.argv[1])
    clusters = []
    for i in range(k):
        data = lines[i]
        data = data.split(",")
        data = process_data(data)
        centroid = Centroid(data)
        clusters.append(Cluster(centroid))
    return clusters


def sum_lists(lst1, lst2):
    return [lst1[i] + lst2[i] for i in range(len(lst1))]


def k_mean(lines, max_iter=200):
    file_length = len(lines)
    clusters = initialize_clusters(lines)
    iterations = 0
    centroids_changed = 0
    first = True
    while iterations < max_iter and (centroids_changed > 0 or first):
        first = False
        iterations += 1
        for i in range(file_length):
            data = lines[i]
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



iterations = 200
if len(sys.argv) == 3:
    iterations = int(sys.argv[-1])
clusters = k_mean(lines, iterations)
for cluster in clusters:
    for i in range(len(cluster.centroid.lst)):
        cluster.centroid.lst[i] = round(cluster.centroid.lst[i], 4)

for cluster in clusters:
    for i in range(len(cluster.centroid.lst)):
        print(cluster.centroid.lst[i], end=", ") if i != len(cluster.centroid.lst) - 1 else print(cluster.centroid.lst[i])
