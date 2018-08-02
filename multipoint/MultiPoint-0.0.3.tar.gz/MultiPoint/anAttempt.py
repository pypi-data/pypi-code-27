"""
hi there

.. math::
    x+y
     
     
buy
"""
def IAAAAresum(N,fa,lam0_1,lam_1,lam0_2,lam_2,lam0_3,lam_3,p1,p2,p3,K0cuttoff=10**-9):
    """
    
    .. math::
        \\underset{AAAA}{I_{1,2,3}^{\left(4\\right)}\left(Nf_{A}\\right)}= & -\sum_{l_{1},l_{2},l_{3}}R_{1}R_{2}R_{3}f3\left(2,\\epsilon_{1},\\epsilon_{2},\\epsilon_{3},Nf_{A}\\right) \\\\
        & +Nf_{A}\mathcal{G}_{3}\mathcal{G}_{2}\mathcal{G}_{1}+\mathcal{G}'_{3}\mathcal{G}{}_{2}\mathcal{G}_{1}+\mathcal{G}_{3}\mathcal{G}'_{2}\mathcal{G}_{1}+\mathcal{G}_{3}\mathcal{G}_{2}\mathcal{G}'_{1}
        
        
    Args:
        N (int): bla bla
    """
    if p2.K < K0cuttoff:
        return IAAAAresumK2is0(N,fa,lam0_1,lam_1, lam0_2,lam_2, lam0_3,lam_3,p1,p3)
    out=0.0+0.0j
    tol = 10**-15
    for l1 in range(abs(p1.mu),p1.ORDEig):
        e1=p1.eig[l1]
        R1=p1.res[l1][lam0_1,lam_1]
        for l2 in range(abs(p2.mu),p2.ORDEig):
            e2=p2.eig[l2]
            R2=p2.res[l2][lam0_2,lam_2]
            for l3 in range(abs(p3.mu),p3.ORDEig):
                e3=p3.eig[l3]
                R3=p3.res[l3][lam0_3,lam_3]
                #if abs(e2)<10**-7:
                # print('epsilon of zero incountered')
                # print('e1',e1,'e2',e2,'e3',e3)
                # print('l1',l1,'l2',l2,'l3',l3)
                temp= - R1*R2*R3*sp.f3(2,e1,e2,e3,N*fa)
                out=out+temp
                if abs(temp/(out+tol))<tol and l3>max(lam0_3,lam_3):
                    break
    
    G1=p1.G0[lam0_1,lam_1]
    G2=p2.G0[lam0_2,lam_2]
    G3=p3.G0[lam0_3,lam_3]
    dG1=p1.dG0[lam0_1,lam_1]
    dG2=p2.dG0[lam0_2,lam_2]
    dG3=p3.dG0[lam0_3,lam_3]
    
    out = out + N*fa*G1*G2*G3 + dG1*G2*G3 + G1*dG2*G3 + G1*G2*dG3
    return out
