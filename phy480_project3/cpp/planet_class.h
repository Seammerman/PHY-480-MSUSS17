#ifndef PLANET_H
#define PLANET_H
#define _USE_MATH_DEFINES
#include <cmath>
#include <vector>
using std::vector;


class planet
{
public:
	// Properties
	double mass;
	double position[3];
	double velocity[3];
	double PE;
	double KE;
	double G;
	double epsilon;

	// Initializers
	planet();
	planet(double M, double x, double y, double z, double vx, double vy, double vz);

	// Functions
	vector<double> distance(planet otherPlanet) {
		double x = position[0], y = position[1], z = position[2];
		double xx = otherPlanet.position[0], yy = otherPlanet.position[1], zz = otherPlanet.position[2];
		double separation[3] = [xx - x, yy - y, zz - z];
		return separation;
	}
	vector<double> GravitationalForce(planet otherPlanet) {
		double dist = distance(otherPlanet);
		double force[3];
		for (i = 0, i < 3; i++) {
			force[i] = (G * mass * otherPlanet.mass) / dist[i];
		}
		return force;
	}
	vector<double> Acceleration(planet otherPlanet) {
		double a[3];
		double force[3] = GraviatonalForce(otherPlanet);
		for (i = 0; i < 3; i++) {
			a[i] = force[i] / mass;
		}
		return a;
	}
	void KineticEnergy() {
		double velsquared = (velocity[0] ^ 2 + velocity[1] ^ 2 + velocity[2] ^ 2);
		KE = 1 / 2 * mass * velsquared;
	}

	void PotentialEnergy(planet &otherPlanet) {
		double pi = M_PI;
		double U = (-G*otherPlanet.mass * mass) / distance(otherPlanet);
		
	}

};

#endif // PLANET_H
