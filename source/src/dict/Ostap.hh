// ============================================================================
#ifndef OSTAP_OSTAP_HH 
#define OSTAP_OSTAP_HH 1
// ============================================================================
// Include files
// ============================================================================
#include "Ostap/BSpline.h"
#include "Ostap/Bernstein.h"
#include "Ostap/Binomial.h"
#include "Ostap/Bit.h"
#include "Ostap/Chi2Fit.h"
#include "Ostap/Chi2Solution.h"
#include "Ostap/Choose.h"
#include "Ostap/Clenshaw.h"
#include "Ostap/Combine.h"
#include "Ostap/Digit.h"
#include "Ostap/EigenSystem.h"
#include "Ostap/Formula.h"
#include "Ostap/GenericMatrixTypes.h"
#include "Ostap/GenericVectorTypes.h"
#include "Ostap/GeomFun.h"
#include "Ostap/GSL_utils.h"
#include "Ostap/Hesse.h"
#include "Ostap/HistoDump.h"
#include "Ostap/HistoInterpolation.h"
#include "Ostap/HistoMake.h"
#include "Ostap/HistoProject.h"
#include "Ostap/HistoStat.h"
#include "Ostap/Interpolation.h"
#include "Ostap/Line.h"
#include "Ostap/LineTypes.h"
#include "Ostap/Lomont.h"
#include "Ostap/LorentzVectorWithError.h"
#include "Ostap/Kinematics.h"
#include "Ostap/Math.h"
#include "Ostap/MatrixUtils.h"
#include "Ostap/MatrixTransforms.h"
#include "Ostap/Models.h"
#include "Ostap/MoreMath.h"
#include "Ostap/Mute.h"
#include "Ostap/NSphere.h"
#include "Ostap/NStatEntity.h"
#include "Ostap/Plane3DTypes.h"
#include "Ostap/PDFs.h"
#include "Ostap/Point3DTypes.h"
#include "Ostap/Point3DWithError.h"
#include "Ostap/Polynomials.h"
#include "Ostap/Power.h"
#include "Ostap/PyIterator.h"
#include "Ostap/PySelector.h"
#include "Ostap/PySelectorWithCuts.h"
#include "Ostap/SFactor.h"
#include "Ostap/StatEntity.h"
#include "Ostap/StatVar.h"
#include "Ostap/StatusCode.h"
#include "Ostap/SVectorWithError.h"
#include "Ostap/SymmetricMatrixTypes.h"
#include "Ostap/Tee.h"
#include "Ostap/ToStream.h"
#include "Ostap/TypeWrapper.h"
#include "Ostap/ValueWithError.h"
#include "Ostap/Vector3DTypes.h"
#include "Ostap/Vector3DWithError.h"
#include "Ostap/Vector4DTypes.h"
#include "Ostap/UStat.h"
#include "Ostap/WStatEntity.h"
// ============================================================================

namespace Ostap
{
  // ==========================================================================
  namespace Math
  {
    // ========================================================================
    template <typename aPoint, typename aLine, typename aPlane>
    struct GF
    {
      static bool intersection( const aLine&  line      ,
                                const aPlane& plane     ,
                                aPoint&       intersect ,
                                double&       mu        )
      { return Ostap::Math::intersection<aLine, aPlane, aPoint>(line,
                                                                plane,
                                                                intersect,
                                                                mu); }
      static bool intersection( const aPlane& plane0    ,
                                const aPlane& plane1    ,
                                aLine&        intersect )
      { return Ostap::Math::intersection<aLine, aPlane>(plane0,
                                                        plane1,
                                                        intersect); }
      static  bool intersection( const aPlane& plane0    ,
                                 const aPlane& plane1    ,
                                 const aPlane& plane2    ,
                                 aPoint&       intersect )
      { return Ostap::Math::intersection<aPoint, aPlane>(plane0,
                                                         plane1,
                                                         plane2,
                                                         intersect); }
      static double impactParameter(const aPoint&  point ,
                                    const aLine&   line  )
      { return Ostap::Math::impactParameter<aPoint,aLine>(point, line); }
      
      static double distance( const aLine& line0 ,
                              const aLine& line1 )
      { return Ostap::Math::distance<aLine, aLine>(line0, line1); }
      
      static  bool closestPoints( const aLine& line0 ,
                                  const aLine& line1 ,
                                  aPoint&      p0    ,
                                  aPoint&      p1    )
      { return Ostap::Math::closestPoints<aLine, aLine, aPoint>(line0,
                                                                line1,
                                                                p0,
                                                                p1); }
      static double closestPointParam( const aPoint&  point ,
                                       const aLine&   line  )
      { return Ostap::Math::closestPointParam<aLine, aPoint>(point, line); }
      
      static aPoint closestPoint(const aPoint&  point ,
                                 const aLine& line)
      { return Ostap::Math::closestPoint<aLine, aPoint>(point, line); }
      
      static bool closestPointParams( const aLine& line0 ,
                                      const aLine& line1 ,
                                      double&      mu0   ,
                                      double&      mu1   )
      { return Ostap::Math::closestPointParams<aLine, aLine>(line0,
                                                             line1,
                                                             mu0,
                                                             mu1);
        
      }
      static bool parallel( const aLine& line0 ,
                            const aLine& line1 )
      { return Ostap::Math::parallel<aLine, aLine>(line0, line1); }
      
    };
    typedef GF<XYZPoint, XYZLine, Plane3D> XYZGeomFun;
    // ========================================================================
    class EigenSystems
    {
      // ======================================================================
    public : // eigen values
      // ======================================================================
      // 2x2
      static Ostap::Vector2 eigenValues
      ( const Ostap::SymMatrix2x2& mtrx          ,
        const bool                 sorted = true )
      {
        Ostap::Math::GSL::EigenSystem system ;
        return system.eigenValues ( mtrx , sorted ) ;
      }
      // 3x3
      static Ostap::Vector3 eigenValues
      ( const Ostap::SymMatrix3x3& mtrx          ,
        const bool                 sorted = true )
      {
        Ostap::Math::GSL::EigenSystem system ;
        return system.eigenValues ( mtrx , sorted ) ;
      }
      // 4x4
      static Ostap::Vector4 eigenValues
      ( const Ostap::SymMatrix4x4& mtrx          ,
        const bool                 sorted = true )
      {
        Ostap::Math::GSL::EigenSystem system ;
        return system.eigenValues ( mtrx , sorted ) ;
      }
      // ======================================================================
    public: // eigen vectors
      // ======================================================================

    public: // eigen vectors
      // ======================================================================
      // 2x2
      static StatusCode eigenVectors
      ( const Ostap::SymMatrix2x2&   mtrx          ,
        Ostap::Vector2&              vals          ,
        std::vector<Ostap::Vector2>& vecs          ,
        const bool                   sorted = true )
      {
        Ostap::Math::GSL::EigenSystem system ;
        return system.eigenVectors ( mtrx , vals , vecs , sorted ) ;
      }
      // 3x3
      static StatusCode eigenVectors
      ( const Ostap::SymMatrix3x3&   mtrx          ,
        Ostap::Vector3&              vals          ,
        std::vector<Ostap::Vector3>& vecs          ,
        const bool                   sorted = true )
      {
        Ostap::Math::GSL::EigenSystem system ;
        return system.eigenVectors ( mtrx , vals , vecs , sorted ) ;
      }
      // 4x4
      static StatusCode eigenVectors
      ( const Ostap::SymMatrix4x4&   mtrx          ,
        Ostap::Vector4&              vals          ,
        std::vector<Ostap::Vector4>& vecs          ,
        const bool                   sorted = true )
      {
        Ostap::Math::GSL::EigenSystem system ;
        return system.eigenVectors ( mtrx , vals , vecs , sorted ) ;
      }
      // ======================================================================
    } ;
    // ========================================================================
  } //                                             end of namespace Ostap::Math
  // ==========================================================================
} //                                                     end of namespace Ostap
// ============================================================================

namespace
{
  // ==========================================================================
  struct Ostap_Instantiations
  {
    Ostap_Instantiations();
    //
    Ostap::Math::XYZLine       __lineXYZ;
    //
    Ostap::Math::XYZGeomFun __geomFunXYZ;
    //
    Ostap::Math::SVectorWithError<2,double> __sv2 ;
    Ostap::Math::SVectorWithError<3,double> __sv3 ;
    Ostap::Math::SVectorWithError<4,double> __sv4 ;
    Ostap::Math::SVectorWithError<5,double> __sv5 ;
    Ostap::Math::SVectorWithError<6,double> __sv6 ;
    Ostap::Math::SVectorWithError<8,double> __sv8 ;
    //
    std::vector<Ostap::Math::ValueWithError>  _dver ;
    std::vector<std::vector<Ostap::Math::ValueWithError> > _dver2 ;
    //
    std::vector<Ostap::Vector2>  _vct_2 ;
    std::vector<Ostap::Vector3>  _vct_3 ;
    std::vector<Ostap::Vector3>  _vct_4 ;
    //
    Ostap::Math::Chi2Solution<4,2>          __cs11 ;
    Ostap::Math::Chi2Solution<4,2>::DATA    __cs21 ;
    Ostap::Math::Chi2Solution<4,2>::COV2    __cs31 ;
    Ostap::Math::Chi2Solution<4,2>::CMTRX2  __cs41 ;
    Ostap::Math::Chi2Solution<4,2>::COFF    __cs51 ;
    Ostap::Math::Chi2Solution<4,2>::VECT    __cs61 ;

    Ostap::Math::Chi2Solution<6,2>          __cs12 ;
    Ostap::Math::Chi2Solution<6,2>::DATA    __cs22 ;
    Ostap::Math::Chi2Solution<6,2>::COV2    __cs32 ;
    Ostap::Math::Chi2Solution<6,2>::CMTRX2  __cs42 ;
    Ostap::Math::Chi2Solution<6,2>::COFF    __cs52 ;
    Ostap::Math::Chi2Solution<6,2>::VECT    __cs62 ;
    
    Ostap::Math::Equal_To<double>               __eq_1 ;
    Ostap::Math::Equal_To<std::vector<double> > __eq_2 ;
    Ostap::Math::Zero<double>                   __eq_3 ;
    Ostap::Math::Zero<std::vector<double> >     __eq_4 ;
    Ostap::Math::NotZero<double>                __eq_5 ;
    Ostap::Math::NotZero<std::vector<double> >  __eq_6 ;
    //
    Ostap::Math::LessOrEqual<double>     __eq_7 ;
    Ostap::Math::GreaterOrEqual<double>  __eq_8 ;
    //
  };
  // ==========================================================================
}

// ============================================================================
#endif // OSTAP_OSTAP_HH
// ============================================================================