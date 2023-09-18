from pyxdsm.XDSM import XDSM, OPT, SOLVER, FUNC, LEFT

x = XDSM(use_sfmath=True)

x.add_system("opt", OPT, r"\text{Optimizer}")
x.add_system("geo", FUNC, r"\text{Geometry}")
x.add_system("mech", FUNC, r"\text{Mechanical Feasibility}")

x.connect("opt", "geo", "x")
x.connect("geo", "mech", "x")

# x.connect("geo", "opt", "x^*")
x.connect("mech", "opt", "x^*")

x.add_input("opt", "x^{(0)}")
x.add_output("opt", "x^*", side=LEFT)
x.add_output("geo", "L_m", side=LEFT)
# x.add_output("mech", "\sigma_{fibre}", side=LEFT)

x.write("mdf", outdir="./XDSM")