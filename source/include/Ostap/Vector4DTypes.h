// ==========================================================================
#ifndef OSTAP_VECTOR4DTYPES_H 
#define OSTAP_VECTOR4DTYPES_H 1
// ==========================================================================
// Include files
// ==========================================================================
// ROOT 
// ==========================================================================
#include "Math/Vector4D.h"
// ==========================================================================
/** @file Vector4DTypes.h
 *
 *  4 vector typedefs
 *
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
}
// ============================================================================
//                                                                      The END 
// ============================================================================
#endif // OSTAP_VECTOR4DTYPES_H
// ============================================================================


