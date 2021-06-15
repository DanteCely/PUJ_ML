## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================

import numpy, sys

## -------------------------------------------------------------------------
'''
'''
class MSECost:

  '''
  '''
  def __init__( self, in_X, in_y ):
    assert isinstance( in_X, ( list, numpy.matrix ) ), "Invalid X type."
    assert isinstance( in_y, ( list, numpy.matrix ) ), "Invalid y type."
    
    if type( in_X ) is list:
      X = numpy.matrix( in_X )
    else:
      X = in_X
    # end if
    if type( in_y ) is list:
      y = numpy.matrix( in_y ).T
    else:
      y = in_y
    # end if
    assert X.shape[ 0 ] == y.shape[ 0 ], "Invalid X,y sizes."
    assert y.shape[ 1 ] == 1, "Invalid y size."

    self.m_M = X.shape[ 0 ]
    self.m_N = X.shape[ 1 ]

    self.m_XtX = ( X.T / float( self.m_M ) ) @ X
    self.m_Xby = ( numpy.array( X ) * numpy.array( y ) ).mean( axis = 0 )
    self.m_uX = X.mean( axis = 0 )
    self.m_uy = y.mean( )
    self.m_yty = ( y.T / float( self.m_M ) ) @ y
  # end def

  def NumberOfExamples( self ):
    return self.m_M
  # end def

  def VectorSize( self ):
    return self.m_N + 1
  # end def

  '''
  '''
  def AnalyticSolve( self ):
    x = numpy.append( numpy.array( [ self.m_uy ] ), self.m_Xby, axis = 0 )
    B = numpy.append( numpy.matrix( [ 1 ] ), self.m_uX, axis = 1 )
    A = numpy.append( self.m_uX.T, self.m_XtX, axis = 1 )
    return x @ numpy.linalg.inv( numpy.append( B, A, axis = 0 ) )
  # end def

  '''
  '''
  def CostAndDerivatives( self, theta ):
    b = theta[ : , 0 ]
    w = theta[ : , 1 : ]
    J = \
      ( w @ self.m_XtX @ w.T ) + \
      ( 2.0 * b * ( w @ self.m_uX.T ) ) + \
      ( b * b ) - \
      ( 2.0 * ( w @ self.m_Xby.T ) ) - \
      ( 2.0 * b * self.m_uy ) + \
      self.m_yty
    dw = 2.0 * ( ( w @ self.m_XtX ) + ( b * self.m_uX ) - self.m_Xby )
    db = 2.0 * ( ( w @ self.m_uX.T ) + b - self.m_uy )
    return [ J[ 0, 0 ], numpy.concatenate( ( db, dw ), axis = 1 ) ]
  # end def

# end class

## -------------------------------------------------------------------------
'''
'''
class MaximumLikelihoodCost:

  '''
  '''
  def __init__( self, in_X, in_y ):
    assert isinstance( in_X, ( list, numpy.matrix ) ), "Invalid X type."
    assert isinstance( in_y, ( list, numpy.matrix ) ), "Invalid y type."
    
    if type( in_X ) is list:
      self.m_X = numpy.matrix( in_X )
    else:
      self.m_X = in_X
    # end if
    if type( in_y ) is list:
      self.m_y = numpy.matrix( in_y ).T
    else:
      self.m_y = in_y
    # end if
    assert self.m_X.shape[ 0 ] == self.m_y.shape[ 0 ], "Invalid X,y sizes."
    assert self.m_y.shape[ 1 ] == 1, "Invalid y size."

    self.m_M = self.m_X.shape[ 0 ]
    self.m_N = self.m_X.shape[ 1 ]

    self.m_Xby = \
      ( numpy.array( self.m_X ) * numpy.array( self.m_y ) ).mean( axis = 0 )
    self.m_uy = self.m_y.mean( )
  # end def

  '''
  '''
  def NumberOfExamples( self ):
    return self.m_M
  # end def

  '''
  '''
  def VectorSize( self ):
    return self.m_N
  # end def

  '''
  '''
  def CostAndDerivatives( self, W, b ):
    Z = ( self.m_X @ W.T ) + b
    H = 1.0 / ( 1.0 + numpy.exp( -Z ) )
    m = float( self.m_M )

    e = sys.float_info.epsilon
    J  = numpy.log( 1.0 - H[ self.m_y[ :, 0 ] == 0 ] + e ).sum( ) / m
    J += numpy.log( H[ self.m_y[ :, 0 ] == 1 ] + e ).sum( ) / m

    dW = \
      ( numpy.array( self.m_X ) * numpy.array( H ) ).mean( axis = 0 ) - \
      self.m_Xby

    db = H.mean( axis = 0 ) - self.m_uy

    return [ -J, dW, db ]
  # end def

# end class

## eof - $RCSfile$
