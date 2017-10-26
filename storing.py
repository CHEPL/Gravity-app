def save_sys(ps):

    f = open("test.gr", "w")

    for p in ps:

        f.write(str(p[0]) + " " +
                str(p[1]) + " " +
                str(p[2]) + " " +
                str(p[3]) + " " +
                str(p[4]) + " " +
                str(p[5]) + " " +
                str(p[6]) + " " +
                str(p[7][0]) + " " +
                str(p[7][1]) + " " +
                str(p[7][2]) + " " +
                str(p[8]) +
                "\n")

    f.close()

def load_sys():

    ps = []

    f = open("test.gr", "r")

    for line in f:

        p = line.split()

        for i in range(7):

            p[i] = float(p[i])

        R = p.pop(7)
        G = p.pop(7)
        B = p.pop(7)

        radius = p.pop(7)

        p.append((int(R), int(G), int(B)))
        p.append(float(radius))

        ps.append(p)
        
    f.close()

    return ps
