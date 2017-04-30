#ifndef solar
#define solar
#include <vector>
#include <fstream>
#include "planet_class.h"
using std::vector;

class solar
{
public:
    friend class planet;

    // properties
    double radius,total_mass,G;
    int total_planets;
    vector<planet> planets;
    double totalKinetic;
    double totalPotential;
	double dt;

    // constants

    // initializers
    solver();
    solver(double radi);

    // functions
	void add(planet newplanet) {
		planets.push_back(newplanet);
	}
	void update_pos() {
		for (j = 0; j < planets.size; j++) {
			planets.at(j).position +=  dt*planets.at(j).velocity + dt*dt/2 * planets.at(j).acceleration
		}
	}
	void update_velocity();
	void update_accel();
	//need work
	void KineticEnergySystem() {
		double total_KE;
		planet current_planet;
		for (i = 0; i < planets.size; i++) {
			current_planet = planets.at(i);
			for (j = 0; j < planets.size; j++) {
				if (j < i && j > i) { current_planet.KineticEnergy() };
			}
			total_PE += current_planet.PE
		}
	}
	//needs work
	void PotentialEnergySystem(double epsilon) {
		double total_PE;
		planet current_planet;
		for (i = 0; i < planets.size; i++) {
			current_planet = planets.at(i);
			for (j = 0; j < planets.size; j++) {
				if (j < i && j > i) { current_planet.PotentialEnergy(planets.at(j)) };
			}
			total_PE += current_planet.PE
		}
	}
    double EnergyLoss();
    bool Bound(planet OnePlanet);

};

#endif // SOLVER_H
