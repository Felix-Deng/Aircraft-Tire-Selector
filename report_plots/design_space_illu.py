import numpy as np 
import matplotlib.pyplot as plt 

def f(x1,x2):
    a=np.sqrt(np.fabs(x2+x1/2+20))
    b=np.sqrt(np.fabs(x1-(x2+20)))
    c=-(x2+20)*np.sin(a)-x1*np.sin(b)
    return c
x1=np.linspace(-256,256,50)
x2=np.linspace(-256,256,50)
X1,X2=np.meshgrid(x1,x2)

fig=plt.figure(figsize=[10, 8])
ax=plt.axes(projection='3d')
ax.plot_surface(X1,X2,f(X1,X2), alpha=1)
# ax.plot_wireframe(X1,X2,f(X1,X2),ccount=2,rcount=2, color='black',alpha=0.8)  
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.set_xlabel(r"$param_1$")
ax.set_ylabel(r"$param_2$")
ax.set_zlabel(r"$Obj(param_1, param_2)$")
plt.tight_layout()
plt.show()
# plt.savefig("eggholder.png")
