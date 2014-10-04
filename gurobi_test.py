from gurobipy import *

try:

    # Create a new model
    m = Model("mip1")
    coe = [1, 1, 2]
    v = {}
    for i in range(3):
        # Create variables
        v[i] = m.addVar(vtype=GRB.BINARY, name=str(1))

    # Integrate new variables
    m.update()
    var = [v[i] for i in range(3)]
    #o = x + y + 2 * z
    # Set objective
    c_0 = [1, 2, 3];
    m.setObjective(LinExpr(coe, var) + LinExpr(c_0, var), GRB.MAXIMIZE)

    # Add constraint: x + 2 y + 3 z <= 4
    # c_1 = x + 2 * y + 3 * z
    # m.addConstr(c_1 <= 4, "c0")
    c_0 = [1, 2, 3];
    m.addConstr(LinExpr(c_0,var), "<=", 4, "c0")


    # Add constraint: x + y >= 1
    c_1 = [1, 1, 0];
    #m.addConstr(x + y >= 1, "c1")
    m.addConstr(LinExpr(c_0,var), ">=", 1, "c1")

    m.optimize()

    for v in m.getVars():
        print v.varName, v.x

    print 'Obj:', m.objVal

except GurobiError:
    print 'Error reported'
