import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
# %matplotlib notebook
PATH = "4uif1.pdb"
# plt.ion()
"""
INFO: HEAVY CHAIN G, I, K
      LIGHT CHAIN H, J, L
      ENVELOPE PROTEIN A, C, E
      MEMBRANE PROTEIN B, D, F
"""


# Goal: Compare the different chains and see how they interact with one another
class Protein():
    def __init__(self, PATH):
        self.read = open(PATH, "r+").read().split("\n")
        self.fig = plt.figure()
        self.ax = plt.axes(projection="3d")
    def split_by(self, NAME=""):
        self.NAME = NAME
        if not NAME == "":
            self.info = {}
        else:
            self.info = []
        for i in self.read:
            k = i.split(" ")
            if k[0] == "ATOM":
                # Read full info, 30, 38, 46, 54 if we're splitting by chain
                # print(list(i)[30:38])
                inf = list(i)
                fullInf = {
                    "CHAIN": inf[21],
                    "POSITION": {
                        "x": float(i[30:38]),
                        "y": float(i[38:46]),
                        "z": float(i[46:54])
                    },
                    "RESID": "".join(inf[17:20])
                }
                if NAME == "CHAIN":
                    # If we have already initialized CHAIN, add to it, else initialize + add
                    # print(self.items())
                    if inf[21] in self.info:
                        # Export chain name, 
                        self.info[inf[21]].append(fullInf)
                    else:
                        self.info[inf[21]] = [fullInf]
                if NAME == "RESID":
                    if "".join(inf[17:20]) in self.info:
                        # Export chain name, 
                        self.info["".join(inf[17:20])].append(fullInf)
                    else:
                        # print("".join(inf[17:20]))
                        self.info["".join(inf[17:20])] = [fullInf]
                if NAME == "":
                    self.info.append(fullInf)
        return self.info
    def compare(self, comp1, comp2):
        print(self.info[comp1])
        # For loop in comp1, then compare comp2
        # Timing o(n^2)
        mapDis = []
        for i in self.info[comp1]:
            # mapD = []
            minA = [float("inf"), 0, 0]
            for ii in self.info[comp2]:
                # print(i["POSITION"])
                dis = ((i["POSITION"]["x"] - ii["POSITION"]["x"])**2 + (i["POSITION"]["y"] - ii["POSITION"]["y"])**2 + (i["POSITION"]["z"] - ii["POSITION"]["z"])**2)**1/2
                # mapD.append(dis)
                if dis < minA[0]:
                    minA = [dis, [i["POSITION"], i["RESID"]], [ii["POSITION"], ii["RESID"]]]
            mapDis.append(minA)
        for i in mapDis:
            print([round(i[0]), *i[1:]])
    def add_to_plot(self, name, color):
        # Given name, plot
        # Extract all positions
        pos_list = [
            [], # x-values
            [], # y-values
            []  # z-values
        ]
        for i in self.info[name]:
            pos_list[0].append(i["POSITION"]["x"])
            pos_list[1].append(i["POSITION"]["y"])
            pos_list[2].append(i["POSITION"]["z"])
        pos_list = np.array(pos_list)
        self.ax.scatter3D(pos_list[0], pos_list[1], pos_list[2], c=color)
    def translate(self, name, trans):
        for i in range(len(self.info[name])):
            self.info[name][i]["POSITION"]["x"] += trans[0]
            self.info[name][i]["POSITION"]["y"] += trans[1]
            self.info[name][i]["POSITION"]["z"] += trans[2]
    def rand_rotation_matrix(self, name):
        # Okay, now we're going to randomly rotate the antibody
        # Let's try this out. This could go very badly.
        # Create a random A [3 x 1]
        A = np.random.rand(3, 1)
        # Check if |A distance vector| < 1
        dis = (A[0]**2 + A[1]**2 + A[2]**2)**1/2
        while abs(dis) > 1:
            print(F"Dis: {dis}, trying again")
            dis = (A[0]**2 + A[1]**2 + A[2]**2)**1/2
            A = np.random.rand(3, 1)
        # x1x2 + y1y2 + z1z2 = 0
j = Protein(PATH)
j.split_by("CHAIN")
# Now calculate distance from each
# We'll initially try out chains A and B
# j.compare("A", "B")
j.rand_rotation_matrix("A")
"""
      HEAVY CHAIN G, I, K
      LIGHT CHAIN H, J, L
      ENVELOPE PROTEIN A, C, E
      MEMBRANE PROTEIN B, D, F
"""
j.add_to_plot("G", "red")
j.add_to_plot("I", "red")
j.add_to_plot("K", "red")
j.add_to_plot("H", "red")
j.add_to_plot("J", "red")
j.add_to_plot("L", "red")

# j.translate("A", [200, 0, 0])
j.add_to_plot("B", "green")
j.add_to_plot("D", "green")
j.add_to_plot("F", "green")
j.add_to_plot("A", "green")
j.add_to_plot("C", "green")
j.add_to_plot("E", "green")

# while True:
#     j.add_to_plot("B", "green")
#     j.translate("B", [10, 10, 10])
#     plt.pause(0.001)

# j.add_to_plot("B", "blue")
plt.show()