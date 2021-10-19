// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ__Optimizer__Base__hxx__
#define __PUJ__Optimizer__Base__hxx__

#include <boost/program_options.hpp>

// -------------------------------------------------------------------------
template< class _TModel >
PUJ::Optimizer::Base< _TModel >::
Base( )
  : m_Cost( nullptr )
{
  this->m_Debug =
    []( unsigned long long, TScalar, TScalar, bool ) -> bool
    { return( false ); };
}

// -------------------------------------------------------------------------
template< class _TModel >
void PUJ::Optimizer::Base< _TModel >::
SetCost( TCost* cost )
{
  this->m_Cost = cost;
}

// -------------------------------------------------------------------------
template< class _TModel >
void PUJ::Optimizer::Base< _TModel >::
AddArguments( boost::program_options::options_description* o )
{
  o->add_options( )
    (
      "lambda",
      boost::program_options::value< TScalar >( &this->m_Lambda )->
      default_value( this->m_Lambda ),
      "regularization"
      )
    (
      "epsilon",
      boost::program_options::value< TScalar >( &this->m_Epsilon )->
      default_value( this->m_Epsilon ),
      "smallest real value"
      )
    (
      "max_iter",
      boost::program_options::value< unsigned long long >(
        &this->m_MaximumNumberOfIterations
        )->
      default_value( this->m_MaximumNumberOfIterations ),
      "maximum iterations"
      )
    (
      "deb_iter",
      boost::program_options::value< unsigned long long >(
        &this->m_DebugIterations
        )->
      default_value( this->m_DebugIterations ),
      "iterations for debug"
      )
    ;
}

// -------------------------------------------------------------------------
template< class _TModel >
void PUJ::Optimizer::Base< _TModel >::
SetRegularizationTypeToRidge( )
{
  this->SetRegularizationType( Self::RidgeRegType );
}

// -------------------------------------------------------------------------
template< class _TModel >
void PUJ::Optimizer::Base< _TModel >::
SetRegularizationTypeToLASSO( )
{
  this->SetRegularizationType( Self::LASSORegType );
}

// -------------------------------------------------------------------------
template< class _TModel >
const unsigned long long& PUJ::Optimizer::Base< _TModel >::
GetIterations( ) const
{
  return( this->m_Iterations );
}

// -------------------------------------------------------------------------
template< class _TModel >
void PUJ::Optimizer::Base< _TModel >::
SetDebug( TDebug d )
{
  this->m_Debug = d;
}

// -------------------------------------------------------------------------
template< class _TModel >
void PUJ::Optimizer::Base< _TModel >::
_Regularize( TScalar& J, TRow& g )
{
  if( this->m_Lambda != TScalar( 0 ) )
  {
    const TRow& t = this->m_Cost->GetParameters( );
    if( this->m_RegularizationType == Self::RidgeRegType )
    {
      J += t.squaredNorm( ) * this->m_Lambda;
      g += t * TScalar( 2 ) * this->m_Lambda;
    }
    else if( this->m_RegularizationType == Self::LASSORegType )
    {
      J += t.array( ).abs( ).sum( ) * this->m_Lambda;
      // TODO:
    } // end if
  } // end if
}

#endif // __PUJ__Optimizer__Base__hxx__

// eof - $RCSfile$