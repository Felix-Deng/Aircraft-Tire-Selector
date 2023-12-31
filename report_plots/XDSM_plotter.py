from pyxdsm.XDSM import XDSM, OPT, SOLVER, FUNC, LEFT

x = XDSM(use_sfmath=True)

x.add_system("opt", OPT, r"\text{Optimizer}")
x.add_system("solver", SOLVER, r"\text{Geometry}")
x.add_system("load", FUNC, "L_m(x)")
x.add_system("mass", FUNC, r"m_{tire}(x)")
x.add_system("mech", FUNC, r"\text{Mechanical Feasibility}")

x.connect("opt", "solver", "x")
x.connect("solver", "load", "x")
x.connect("solver", "mass", "x")
x.connect("solver", "mech", "x")

x.connect("load", "opt", "L_m")
x.connect("mass", "opt", "m_{tire}")
x.connect("mech", "opt", "\sigma_{cord}")

x.add_input("opt", "x^{(0)}")
# x.add_input("mech", "I_{speed}")
x.add_output("opt", "x^*", side=LEFT)

x.write("mdf", outdir="./report_plots")
