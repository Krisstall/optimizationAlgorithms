import argparse

import numpy as np

from src.whale_optimization import WhaleOptimization

def parse_cl_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-nsols", type=int, default=50, dest='nsols', help='number of solutions per generation') 
    parser.add_argument("-ngens", type=int, default=30, dest='ngens', help='number of generations') 
    parser.add_argument("-a", type=float, default=2.0, dest='a', help='woa algorithm specific parameter, controls search spread') 
    parser.add_argument("-b", type=float, default=0.5, dest='b', help='woa algorithm specific parameter, controls spiral,') 
    parser.add_argument("-c", type=float, default=None, dest='c', help='absolute solution constraint value') 
    parser.add_argument("-func", type=str, default='goldstein', dest='func', help='function to be optimized, options: ackley, levi, beale, goldstein') 
    parser.add_argument("-r", type=float, default=0.25, dest='r', help='resolution of function meshgrid') 
    parser.add_argument("-t", type=float, default=0.1, dest='t', help='animate sleep time, lower values increase animation speed, default: 0.1') 
    parser.add_argument("-max", default=False, dest='max', action='store_true', help='enable for maximization, default: False (minimization)') 

    args = parser.parse_args()
    return args

    # yukarıdaki kısım algoritmamıza çalışması gereken parametreleri gönderiyor (whale algoritmasına özel parametreler ve optimize edilicek olan fonksiyonu)

def levi(X, Y):
    A = np.sin(3.0*np.pi*X)**2
    B = ((X-1)**2)*(1+np.sin(3.0*np.pi*Y)**2)
    C = ((Y-1)**2)*(1+np.sin(2.0*np.pi*Y)**2)
    return A + B + C

def ackley(X, Y):
    
    A = -20*np.exp(-0.2*np.sqrt(0.5*(X*X + Y*Y))) - np.exp(0.5*(np.cos(2*np.pi*X)+np.cos(2*np.pi*Y))) + np.e + 20
    
    return A 

def beale(X, Y):
    
    A = (1.5 - X + X * Y)**2 + (2.25 - X + X * (Y**2))**2 + (2.625 - X + X * (Y**3))**2
    
    return A 

def goldstein(X, Y):
    
    A = 1 + (X + Y + 1)**2 * (19 - 14*X + 3*(X**2) - 14*Y + 6*X*Y + 3*(Y**2))
    B = 30 + (2*X - 3*Y)**2 * (18 - 32*X + 12*(X**2) + 48*Y - 36*X*Y + 27*(Y**2))
    
    return A * B

    # fonksiyonlarımızı burada tanımlıyoruz
    
def main():
    args = parse_cl_args()  # methodu çapırarak parametrelerimizi alıyoruz

    nsols = args.nsols  #aldığımız parametleri yerel değişkenlere atıyoruz
    ngens = args.ngens  #aldığımız parametleri yerel değişkenlere atıyoruz

    funcs = {'levi':levi, 'ackley':ackley, 'beale':beale, 'goldstein':goldstein} #optimize edeceğimiz fonksiyonları çağırıyoruz
    func_constraints = {'levi':10.0,'ackley':5.0, 'beale':4.5, 'goldstein':2.0 } #fonksiyonların uç değerlerini belirliyoruz

    if args.func in funcs:
        func = funcs[args.func] 
    else:
        print('Missing supplied function '+args.func+' definition. Ensure function defintion exists or use command line options.')
        return
    #fonksiyonumuz tanımlanmış mı ? kontrolünü yapıyoruz
    if args.c is None:
        if args.func in func_constraints:
            args.c = func_constraints[args.func]
        else:
            print('Missing constraints for supplied function '+args.func+'. Define constraints before use or supply via command line.')
            return
        #parametrelerimizde eksik var mı ? kontrolümüzü yapıyoruz
    C = args.c 
    constraints = [[-C, C], [-C, C]] 
    #uç değerleri yerel değişkene alıyoruz
    opt_func = func
    #optimize edilcek fonksiyonu yerel değişkene alıyoruz
    b = args.b
    a = args.a
    a_step = a/ngens

    maximize = args.max
    #aldığımız parametleri yerel değişkenlere atıyoruz
    opt_alg = WhaleOptimization(opt_func, constraints, nsols, b, a, a_step, maximize) #istediğimiz fonksiyon ile whale algoritmasını çalıştırıyoruz
    #solutions = opt_alg.get_solutions() #sonuçlarımızı alıyoruz
    

    for _ in range(ngens):
        opt_alg.optimize()
        #solutions = opt_alg.get_solutions() #sonuçlarımızı alıyoruz
        

    opt_alg.print_best_solutions() #konsola çıktı olarak en iyi sonucu veriyoruz

if __name__ == '__main__':
    main()
