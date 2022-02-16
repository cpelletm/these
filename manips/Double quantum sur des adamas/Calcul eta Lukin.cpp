#include <iostream>
#include <string> // C'est chaud t'as rien de base en cpp
#include <cmath>
#include <eigen3/Eigen/Dense>

using namespace std;
using namespace Eigen;

double const pi(acos(-1));
Matrix3d classe1,classe2,classe3,classe4,classe5,classe6,classe7,classe8;

void init_rotation_matrix(){
	Matrix3d rot;

	classe1 <<
		1/sqrt(2), -1/sqrt(2), 0,
		1/sqrt(6), 1/sqrt(6), -2/sqrt(6),
		1/sqrt(3), 1/sqrt(3), 1/sqrt(3);

	rot << 
		-1,0,0,
		0,-1,0,
		0,0,1;
	classe2=rot*classe1;

	rot << 
		-1,0,0,
		0,1,0,
		0,0,-1;
	classe3=rot*classe1;

	rot << 
		1,0,0,
		0,-1,0,
		0,0,-1;
	classe4=rot*classe1;

	rot << 
		0,1,0,
		-1,0,0,
		0,0,1;
	classe5=rot*classe1;

	rot << 
		1,0,0,
		0,0,1,
		0,-1,0;
	classe6=rot*classe1;

	rot << 
		0,0,-1,
		0,1,0,
		1,0,0;
	classe7=rot*classe1;

	rot << 
		0,-1,0,
		-1,0,0,
		0,0,-1;
	classe8=rot*classe1;
}

Matrix3d rotated_basis(Matrix3d basis, double angle){
	Matrix3d m;
	Vector3d x,y,z;
	x=basis.row(0)*cos(angle)+basis.row(1)*sin(angle);
	y=basis.row(1)*cos(angle)-basis.row(0)*sin(angle);
	z=basis.row(2);
	m.row(0)=x;
	m.row(1)=y;
	m.row(2)=z;
	return m;
}

double x(double theta,double phi){
	double res=sin(theta)*cos(phi);
	return res;
}
double y(double theta,double phi){
	double res=sin(theta)*sin(phi);
	return res;
}
double z(double theta,double phi){
	double res=cos(theta);
	return res;
}

//Techniquement je pourrai définir x1,y1,z1 etc en dehors pour pas occuper trop de mémoire, mais c'est chiant quand je voudrais intégrer sur toutes les variables
double gp_diff_noC(double theta, double phi, double angle1=0, double angle2=0, Matrix3d c1=classe1, Matrix3d c2=classe1){
	Vector3d x1,y1,z1,x2,y2,z2,r;
	Matrix3d m;
	double gp,hm,integrande;
	r << x(theta,phi), y(theta,phi), z(theta,phi);
	m=rotated_basis(c1,angle1);
	x1=m.row(0);
	y1=m.row(1);
	z1=m.row(2);
	m=rotated_basis(c2,angle2);
	x2=m.row(0);
	y2=m.row(1);
	z2=m.row(2);
	gp=0.5*(3*x1.dot(r)*x2.dot(r)-x1.dot(x2)+3*y1.dot(r)*y2.dot(r)-y1.dot(y2));
	hm=0.5*(3*x1.dot(r)*y2.dot(r)-x1.dot(y2)-3*y1.dot(r)*x2.dot(r)+y1.dot(x2));
	/*cout << r << endl << y1 << endl << 3*y1.dot(r)*y2.dot(r) << endl;*/
	integrande=1/(4*pi)*sqrt(pow(gp,2)+pow(hm,2))*sin(theta);// /(2*pi)/(2*pi)
	return integrande;

}

int main()
{
	init_rotation_matrix();
   	Matrix3d m;
	Vector3d x,y,z;
	double a,b,c;
   	a=gp_diff_noC(0,0);
   	cout << "a=" << a << endl;
   	return 0;
}

