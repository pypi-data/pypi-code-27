from hwaves import hwf_plot

def test_density_isosurface():
    #for n in range(1,4):
    for n in [2]:
        #for l in range(0,n):
        for l in [1]:
            #for m in range(-l,l+1):
            for m in [1]:
                print('n={}, l={}, m={}'.format(n,l,m))
                hwf_plot.plot_isosurface(1,n,l,m)


test_density_isosurface()

