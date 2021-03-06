// ==========================================================================
#ifndef OSTAP_VECTOR4DTYPES_H 
#define OSTAP_VECTOR4DTYPES_H 1
// ==========================================================================
// Include files
// ==========================================================================
// STD& STL
// ==========================================================================
#include <cmath>
#include <complex>
// ==========================================================================
// ROOT 
// ==========================================================================
#include "Math/Vector4D.h"
// ==========================================================================
/** @file Ostap/Vector4DTypes.h
 *  4 vector typedefs
 *  @author Juan PALACIOS
 *  @date   2005-11-21
 */
namespace Ostap
{
  // ==========================================================================
  typedef ROOT::Math::PxPyPzEVector     XYZTVector      ; ///< Cartesian 4 Vector
  typedef ROOT::Math::PxPyPzEVector     LorentzVector   ; ///< Cartesian 4 Vector
  typedef ROOT::Math::PtEtaPhiEVector   PtEtaPhiEVector ; ///< Polar 4 Vector
  // ==========================================================================
  typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<std::complex<double> > > 
  ComplexLorentzVector ;
  // ==========================================================================
}
// ============================================================================
//                                                                      The END 
// ============================================================================
#endif // OSTAP_VECTOR4DTYPES_H
// ============================================================================



