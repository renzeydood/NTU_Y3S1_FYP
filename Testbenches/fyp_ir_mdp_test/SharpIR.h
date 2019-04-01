/*
	SharpIR

	Arduino library for retrieving distance (in cm) from the analog GP2Y0A21Y and GP2Y0A02YK

	From an original version of Dr. Marcal Casas-Cartagena (marcal.casas@gmail.com)     
	
    Version : 1.0 : Guillaume Rico

	https://github.com/guillaume-rico/SharpIR

*/

#ifndef SharpIR_h
#define SharpIR_h

#define NB_SAMPLE 101

#ifdef ARDUINO
#include "Arduino.h"
#endif

class SharpIR
{
public:
  SharpIR(int irPin, long sensorModel, double grad, double intercept);
  int distance();
  void setModel(long model);
  void SharpIR::setGrad(double gradient);
  void SharpIR::setIncpt(double intercept);

private:
  void sort(int a[], int size);

  int _irPin;
  long _model;
  double _grad;
  double _intercept;
};

#endif
