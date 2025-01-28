import os, datetime
import re

class TimeoutException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self,*args,**kwargs)

def det(Pcr,CR,ps):                     # output function
    f=(1-(2.718281828)*(-ps/CR))*100    #   weibull distribution , probability of failure
    PE = (Pcr - CR) * 100 / Pcr         # percentage error
    if PE < 0: PE = -1
    print("""Solution:
    Non-linear critical Buckling Load = """ + str(round(CR, 3)) + """ N
    Linear critical buckling load = """ + str(round(Pcr, 3)) + """ N
    Percentage error = """ + str(round(PE, 3)) + """ %
    Probability of failure at front end due to buckling: """+str(round(f,3))+""" %""")
    exit()                              #end program

def main():
    fname=input("Enter the path of the para-geometry file: ")
    while not os.path.exists(fname):
        print("The file does not exist.")
        fname=input("Enter the path of the para-geometry file: ")
    print("Enter the following dimensions in meters.")
    l = input("Enter the Length of the Aircraft's body: ")
    z = input("Enter the Height of the Aircraft's body: ")
    y = input("Enter the Width of the Aircraft's body: ")

    # ratio of lateral and longitudinal strain
    u = input("Enter the poisson's ratio of material: ")
    e = input("Enter the young's modulus of the material: ")    # stress over strain
    
    # how many divisions for analysis
    ediv = input("Enter the number of element divisions in meshing: ")

    p=input("input air density (Kg/m^3): ")
    v=input("input top airspeed (km/h): ")                      # max speed
    cd=input("Input coefficient of drag: ")                     # friction coefficient

    prop_stress=float(p)*float(cd)*(float(v)**2)/2              #drag equation,   drag stress
    MI = [(float(l) ** 3 + float(z)) / 12, (float(z) ** 3 + float(l)) / 12, (float(l) ** 3 + float(y)) / 12, (float(y) ** 3 + float(l)) / 12]
    I = min(MI)                                                 #minimum moment of inertia
    Leq = 2 * float(l)                                          #equivalent length = 2 x length
    Pcr = (3.141593 * I * float(e)) / (Leq ** 2)                #linear critical load
    l = str(float(l) * 1000)                                    #changing to mm as standard format
    z = str(float(z) * 1000)
    y = str(float(y) * 1000)

    filehandle = open('Buckling analysis.inp', 'w')             #opening .inp file for write

    text="""!                               INP file for non-linear buckling of geometry
/CLEAR
/input,start,ans,'"""+fname+"""'
finish  
~PARAIN,'"""+fname+"""','x_t',,SURFACES,0,0  !input geometry
/NOPR   
/GO/CLEAR 

e_div=""" + ediv + """          !setting element divisions
length=""" + l + """            !setting length
Y_M=""" + e + """               !setting youngs modulus
P_R=""" + u + """               !setting poisons ratio
Z_=""" + z + """                !setting height
Y_=""" + y + """                !setting width

/PREP7                          !preprocessor
et,1,beam188                    !element type: structural, linear, elastic, isotropic
keyopt,1,3,2                    !keypoint definition, defining 2
sectype,1,beam,rect,rect1       !section id
secoffset,cent                  !defining the section offset for cross sections
secdata,Z_,Y_,                  !defining height and width respectively
mp,ex,1,Y_M                     !youngs modulus of aircraft material
mp,nuxy,1,P_R                   !poison's ratio of aircraft material

k,1,0,0                 !first node: end of aircraft
k,2,0,length            !last node, defining length: front of aircraft
l,1,2                   !define body
lesize,1,,,e_div        !element divisions
lmesh,1                 !mesh the body

/eshape,1,1             !establish solid
eplo                    !element plot
finish

/SOLU                   !solu processor
antype,static           !static analysis type
pstress,on              !pre stress effects on
dk,1,all,0              !apply boundary conditions, restricting displacement in all axis
fk,2,fy,-1              !applying compressive load
solve                   !solve static analysis
finish                  !end analysis

/SOLU                   !solu processor
antype,buckle           !Eigen-buckling analysis type
bucopt,lanb,2           !extract reading from 2 ends
mxpand,2,,,yes          !expand reading from both ends
solve                   !solve eigen-buckling analysis
finish                  !end analysis

/POST1                  !post processor
set,first               !read first set of results
pldisp,1                !plot results
set,next                !read next set of results
pldisp,1                !plot results
finish

/SOLU                   !solu processor
antype,static           !static analysis type
nlgeom,on               !non linear geometry on
neqit,150               !setting number of equilibrium iterations
outpr,all,all           !print out solution
outres,all,all          !write data to database

autots,on               !automatic time stepping on
deltim,5,1,10           !time steps from 1 to 10 in 5 units

dk,1,all,0              !apply boundary conditions, restricting displacement in all axis

fcr=-""" + str(Pcr) + """  !linear critical load

fk,2,fx,1       ! apply compressive load

fv=fcr1.02     !adjust load
fk,2,fy,fv      !apply load
time,-fv        !measure displacement readings
solve

fkdel,2,fx      !delete previous load
fv=fcr1.1      !adjust load
fk,2,fy,fv      !apply load
time,-fv        !measure displacement readings
solve

fv=fcr1.2      !adjust load
fk,2,fy,fv      !apply load
time,-fv        !measure displacement readings
solve

fv=fcr1.3      !adjust load
fk,2,fy,fv      !apply load
time,-fv        !measure displacement readings
solve
finish

/POST1          !post processor
set,,,,,800     !read all sets
pldisp,1        !plot results

fini

/POST26             !time-history post processor
nsol,2,2,u,x,ux     !plot displacement differences

/grid,1             !in graphical format
/axlab,x,DISP       !display displacements
/axlab,y,LOAD       !display loads
xvar,2
plvar,1             !in graphical format
fini 
"""
    filehandle.write(text)
    filehandle.close()

    print('.inp file created, waiting for .inp file to be executed...\n')

    while not os.path.exists("buckling analysis.out"):0
    print("Analysis Report file found, loading results...\n")
    
    CR = 0
    time_start = datetime.datetime.now()                     #storing starting time
    try:
        while (CR == 0):
            with open('buckling analysis.out', 'r') as file: #opening .out file for read
                for line in file:
                    if "2 NSOL" in line:
                        line=line.rstrip()
                        terms = line.split(" ")
                        line = terms[len(terms) - 1]
                        if "E+" in line:
                            Val = line.split("E+")
                            CR = float(Val[0]) * 10 + float(Val[1])
                        else:
                            CR = float(line)
                        det(Pcr,CR,prop_stress)             # output function
            file.close()
            time_elapsed = datetime.datetime.now() - time_start
            if time_elapsed > datetime.timedelta(seconds=30):
                raise TimeoutException()
    except TimeoutException:                                # in case of error
        time_start = datetime.datetime.now()
        try:
            while(CR==0):
                force=0
                with open('buckling analysis.out', 'r') as file:
                    for line in file:
                        if " REACTION SOLUTION " in line:
                            line=re.sub("[ REACTIONSLUM=]", "", line)
                            if "+" in line:
                                Val = line.split("+")
                                force = float(Val[0]) * 10 + float(Val[1])
                            else:
                                force = float(line)
                CR=force
                file.close()
                time_elapsed = datetime.datetime.now() - time_start
                if time_elapsed > datetime.timedelta(seconds=30):
                    raise TimeoutException()
        except TimeoutException:                            # in case of error
            print("""No Eigenvalues were converged, an error has occured
Linear critical buckling load = """ + str(round(Pcr, 3)) + """ N
        """)
            with open('buckling analysis.out', 'r') as file:
                for line in file:
                    if ' ERROR ' in line:                   # print all errors
                        for _ in range(1):
                            line = file.readline()
                        print("Error: " + line)
            exit()
    det(Pcr,CR,prop_stress)

if __name__=='__main__':
    if os.name=='nt':
        os.system('cls')
    else:                                                   # os.name = 'posix'
        os.system('clear')
    main()