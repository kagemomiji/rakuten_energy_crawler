def least_square(map):
    xs = map["x"] 
    ys = map["y"]
    mx = sum(xs)*1.0/len(xs)
    my = sum(ys)*1.0/len(ys)
    sum_xy = 0
    sum_xx = 0

    for i in range(len(xs)):
        sum_xy = sum_xy + xs[i]*ys[i]
        sum_xx = sum_xx + xs[i]*xs[i]

    a = (sum_xy*1.0/len(xs) - mx * my)/(sum_xx*1.0/len(xs) - mx * mx)       
    b = - a * mx + my
    return (a,b)

