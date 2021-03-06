import numpy as np

class WhaleOptimization():
    def __init__(self, opt_func, constraints, nsols, b, a, a_step, maximize=False):
        self._opt_func = opt_func
        self._constraints = constraints
        self._sols = self._init_solutions(nsols) 
        self._b = b
        self._a = a
        self._a_step = a_step
        self._maximize = maximize
        self._best_solutions = []
        
    def get_solutions(self):
        return self._sols
                                                                  
    def optimize(self):
        ranked_sol = self._rank_solutions()
        best_sol = ranked_sol[0] 
        #include best solution in next generation solutions
        new_sols = [best_sol]
                                                                 
        for s in ranked_sol[1:]:
            if np.random.uniform(0.0, 1.0) > 0.5:                                      
                A = self._compute_A() #sonraki pozisyonu hesaplamak için WAO ya özel değişkeni hesaplıyoruz                                            
                norm_A = np.linalg.norm(A)    #sonuca göre rastgele vaktör üretiyoruz                                            
                if norm_A < 1.0:                                                 
                    new_s = self._encircle(s, best_sol, A)#sonuç tatmin edici ise alanımızı daraltıyoruz                           
                else:                                                                     
                    random_sol = self._sols[np.random.randint(self._sols.shape[0])]    #sonuçların arasından rastgele seçiyoruz   
                    new_s = self._search(s, random_sol, A)    #sonuç tatmin edici değil ise başka bir sonuç seçip aramaya devam ediyoruz                            
            else:                                                                         
                new_s = self._attack(s, best_sol)      #spiral çizerek hedefe yaklaşır                                   
            new_sols.append(self._constrain_solution(new_s)) # mesafeyi diziye kaydediyoruz

        self._sols = np.stack(new_sols) #oluşan yeni sonuçları bir sonraki iterasyonda kullanmak için sols a ekliyoruz
        self._a -= self._a_step

    def _init_solutions(self, nsols):
        sols = []
        for c in self._constraints:
            sols.append(np.random.uniform(c[0], c[1], size=nsols))
                                                                            
        sols = np.stack(sols, axis=-1)
        return sols

    def _constrain_solution(self, sol):
        constrain_s = []
        for c, s in zip(self._constraints, sol):
            if c[0] > s:
                s = c[0]
            elif c[1] < s:
                s = c[1]
            constrain_s.append(s)
        return constrain_s

    def _rank_solutions(self):
        fitness = self._opt_func(self._sols[:, 0], self._sols[:, 1])
        sol_fitness = [(f, s) for f, s in zip(fitness, self._sols)]
   
        #best solution is at the front of the list
        ranked_sol = list(sorted(sol_fitness, key=lambda x:x[0], reverse=self._maximize))
        self._best_solutions.append(ranked_sol[0])

        return [ s[1] for s in ranked_sol] 

    def print_best_solutions(self):
        print('generation best solution history')
        print('([fitness], [solution])')
        for s in self._best_solutions:
            print(s)
        print('\n')
        print('best solution')
        print('([fitness], [solution])')
        print(sorted(self._best_solutions, key=lambda x:x[0], reverse=self._maximize)[0])

    def _compute_A(self):
        r = np.random.uniform(0.0, 1.0, size=2)
        return (2.0*np.multiply(self._a, r))-self._a

    def _compute_C(self):
        return 2.0*np.random.uniform(0.0, 1.0, size=2)
                                                                 
    def _encircle(self, sol, best_sol, A):
        D = self._encircle_D(sol, best_sol) # D parametramize ihtiyacımız var
        return best_sol - np.multiply(A, D)
                                                                 
    def _encircle_D(self, sol, best_sol):
        C = self._compute_C() # C parametremize ihtiyacımız var
        D = np.linalg.norm(np.multiply(C, best_sol)  - sol)
        return D

    def _search(self, sol, rand_sol, A):
        D = self._search_D(sol, rand_sol)
        return rand_sol - np.multiply(A, D)

    def _search_D(self, sol, rand_sol):
        C = self._compute_C()
        return np.linalg.norm(np.multiply(C, rand_sol) - sol)    

    def _attack(self, sol, best_sol):
        D = np.linalg.norm(best_sol - sol)
        L = np.random.uniform(-1.0, 1.0, size=2)
        return np.multiply(np.multiply(D,np.exp(self._b*L)), np.cos(2.0*np.pi*L))+best_sol
