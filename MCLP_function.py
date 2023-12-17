


class MCLP:

    def __init__(self,excel_file = "distance_matrix.xlsx") -> None:
        import pandas as pd
        import numpy as np 
       
        self.dfs = pd.read_excel(excel_file, index_col=0)

        self.df = self.dfs.copy()

        self.demand_i = np.random.rand(self.df.shape[1])*10000 #demand aslinya 
        self.demands = {city : demand for city, demand in zip(self.df.columns,self.demand_i)}
        

    def MCLP_function(self,k,max_coverage):
        import pulp
        import numpy as np 
        import json

        facilities = self.df.columns.tolist()  # Facility locations
        demand_points = self.df.index.tolist()  # Demand points

        #HYPER PARAMETER YANG DIPAKE (OTAK ATIK 2 VARIABLE DIBAWAH INI BUAT NAIKIN PERFORMANCENYA)
        k = k  # Number of facilities to open
        maximum_coverage = max_coverage 

        problem = pulp.LpProblem("MCLP", pulp.LpMaximize)

        #Defining Decision Variable yang dipake 
        # Define binary variables for facility opening decision
        x_facility_open = {j: pulp.LpVariable("x " + str(j), cat=pulp.LpBinary) for j in facilities}   #x
        y_demand_point = {i: pulp.LpVariable("y " + str(i), cat=pulp.LpBinary) for i in demand_points}  #y


        # Define the objective function (maximize coverage)
        problem += pulp.lpSum([self.demands[d] * y_demand_point[d] for d in y_demand_point])

        # Constraints Declaration

    # Set up constraints K (maximal SPKLU YANG DIBANGUN)
        problem += pulp.lpSum([x_facility_open[f] for f in facilities]) == k

    #set up constraint lokasi yang tercover 

    #subset kota yang tercover 
        N = {i:[j for j in facilities if self.df[i][j] <= maximum_coverage] for i in demand_points}
        for i in demand_points:
            problem += pulp.lpSum([x_facility_open[j] for j in N[i]]) >= y_demand_point[i]

        problem.solve()
        
        x_soln = np.array([x_facility_open[j].varValue for j in facilities])

        y_soln = np.array([y_demand_point[j].varValue for j in demand_points])
        # And print some output
        # print (("Status:"), pulp.LpStatus[problem.status])
        # print ("Population Served is = ", pulp.value(problem.objective))
        # print("total demand : ", sum(list(self.demands.values())))
        # print ("x = ", x_soln)
        # print("y = ", y_soln)

        #Import data to Textfiles 
        facilities_opened=[]
        cities_covered = []
        cities_not_covered = []
        for i in range(len(x_soln)):
            if x_soln[i] == 1:
                facilities_opened.append(self.df.columns[i])

        for i in range(len(y_soln)):
            if y_soln[i] == 1:
                cities_covered.append(self.df.columns[i])
            else:
                cities_not_covered.append(self.df.columns[i])

        final_res={
            'f_open':facilities_opened,
            'c_cover':cities_covered,
            'c_not_cover':cities_not_covered,
            'pop_served': pulp.value(problem.objective),
            'all_demand': sum(list(self.demands.values())),
            'performance':f'{pulp.value(problem.objective)/sum(list(self.demands.values()))} dari seluruh demand tercover'  
              }

        

        return final_res['performance']

        